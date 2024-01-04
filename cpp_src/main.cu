#include "Board.h"
#include "Body.h"
#include "Creature.h"
#include "Genome.h"
#include "device_util.cuh"
#include "host_util.h"
#include "testing/test.h"
#include "util.h"
#include <algorithm>
#include <stack>

int main()
{
    read_in_settings();
    print(BOARD_WIDTH, BOARD_HEIGHT);
    // initialize board
    Board* board;
    cudaMallocManaged((void**)&board, sizeof(Board));
    int* grass;
    int* grass_stage;
    cudaMallocManaged((void**)&grass, sizeof(int) * BOARD_WIDTH * BOARD_HEIGHT);
    cudaMallocManaged((void**)&grass_stage, sizeof(int) * BOARD_WIDTH * BOARD_HEIGHT);
    *board = Board(grass, grass_stage);
    int id_gen = 0;
    // int MAX_CREATURES = 10000;
    stack<int> available_idx;

    // initialize bodies
    int num_creatures = INIT_CREATURES;
    Body* bodies;
    cudaMallocManaged((void**)&bodies, sizeof(Body) * MAX_CREATURES);
    vector<Creature> creatures;
    for (int i = 0; i < num_creatures; i++) {
        int x = random_int(0, BOARD_WIDTH - 1);
        int y = random_int(0, BOARD_HEIGHT - 1);
        Genome g(random_int(WEIGHTS, 1000));
        creatures.emplace_back(Creature(x, y, -1, -1, id_gen, 0, bodies + i, g));
        id_gen++;
    }
    for (int i = MAX_CREATURES - 1; i >= num_creatures; i--) {
        bodies[i].m_alive = false;
        available_idx.push(i);
    }
    ll n = 0;
    dim3 grass_block(32, 32);
    dim3 grass_grid((BOARD_WIDTH + grass_block.x - 1) / grass_block.x, (BOARD_HEIGHT + grass_block.y - 1) / grass_block.y);
    // run a few cycles
    while (true) {
        using namespace chrono;
        auto g_start = high_resolution_clock::now();
        grow_grass<<<grass_grid, grass_block>>>(board, GRASS_MAX_HEIGHT, GRASS_PERIOD, BOARD_WIDTH, BOARD_HEIGHT);
        cudaDeviceSynchronize();
        int dimx = 1024;
        dim3 block(dimx);
        dim3 grid((MAX_CREATURES + block.x - 1) / block.x);
        get_inputs<<<grid, block>>>(board, bodies, MAX_CREATURES, BOARD_WIDTH, BOARD_HEIGHT);
        cudaDeviceSynchronize();
        think_and_act<<<grid, block>>>(bodies, MAX_CREATURES, COST_MOVEMENT, COEFF_BASE_ENERGY, STARVATION, HEALTH_TO_ENERGY_RATIO, ENERGY_TO_HEALTH, GRASS_MAX_HEIGHT, GRASS_PERIOD, BOARD_WIDTH, BOARD_HEIGHT);
        cudaDeviceSynchronize();
        auto g_end = high_resolution_clock::now();
        remove_dead(creatures, available_idx);
        eat_and_attack(board, bodies, MAX_CREATURES);
        remove_dead(creatures, available_idx);
        auto start = high_resolution_clock::now();
        birth(creatures, bodies, MAX_CREATURES, id_gen, available_idx);
        auto end = high_resolution_clock::now();
        remove_dead(creatures, available_idx);

        vector<double> x_vec;
        vector<double> y_vec;
        vector<int> c_vec;
        num_creatures = 0;
        int total_mass = 0;
        int total_energy = 0;
        int total_preds = 0;
        int total_preys = 0;
        int total_brain_size = 0;
        for (int i = 0; i < MAX_CREATURES; i++) {
            if (bodies[i].m_alive) {
                x_vec.pb(bodies[i].m_x);
                y_vec.pb(bodies[i].m_y);
                if (bodies[i].m_output_values[ATTACK] > 0) {
                    total_preds++;
                    c_vec.pb(1);
                } else {
                    total_preys++;
                    c_vec.pb(0);
                }
                // dprint(bodies[i].m_health, bodies[i].m_energy, bodies[i].m_base_energy_use, bodies[i].m_output_values[ATTACK]);
                num_creatures++;
                total_mass += bodies[i].m_health;
                total_energy += bodies[i].m_energy;
            }
            if (i < (int)creatures.size() && creatures[i].m_body->m_alive) {
                total_brain_size += creatures[i].m_genome.m_bitstring.size();
            }
        }
        // vector<int> grass_x;
        // vector<int> grass_y;
        // vector<int> grass_c;
        // for (int i = 0; i < BOARD_WIDTH; i++) {
        //     for (int j = 0; j < BOARD_HEIGHT; j++) {
        //         grass_x.pb(i);
        //         grass_y.pb(j);
        //         grass_c.pb(board->grass[i][j]);
        //     }
        // }
        print(n);
        print(total_mass);
        print(total_energy);
        print(total_preds);
        print(total_preys);
        print(total_brain_size);
        dprint(num_creatures);
        dprint("GPU took", duration_cast<milliseconds>(g_end - g_start).count());
        dprint("CPU took", duration_cast<milliseconds>(end - start).count());
        // print(grass_x);
        // print(grass_y);
        // print(grass_c);
        print(x_vec);
        print(y_vec);
        print(c_vec);
        n++;
        // cerr << n << endl;
        // sleep(1);
    }
}