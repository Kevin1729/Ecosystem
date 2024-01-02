#include "Board.h"
#include "Body.h"
#include "Creature.h"
#include "Genome.h"
#include "device_util.cuh"
#include "testing/test.h"
#include "util.h"
#include <algorithm>

int main()
{
    // initialize board
    Board* board;
    cudaMallocManaged((void**)&board, sizeof(Board));
    *board = Board();

    // initialize bodies
    int num_creatures = 100;
    Body* bodies;
    cudaMallocManaged((void**)&bodies, sizeof(Body) * num_creatures);
    vector<Creature> creatures;
    for (int i = 0; i < num_creatures; i++) {
        int x = random_int(0, BOARD_WIDTH - 1);
        int y = random_int(0, BOARD_HEIGHT - 1);
        Genome g(1000);
        creatures.emplace_back(Creature(x, y, 100, i, 0, bodies + i, g));
    }
    ll n = 1000;
    dim3 grass_block(32, 32);
    dim3 grass_grid((BOARD_WIDTH + grass_block.x - 1) / grass_block.x, (BOARD_HEIGHT + grass_block.y - 1) / grass_block.y);
    // run a few cycles
    while (true) {
        grow_grass<<<grass_grid, grass_block>>>(board);
        cudaDeviceSynchronize();
        int dimx = 32;
        dim3 block(dimx);
        dim3 grid((num_creatures + block.x - 1) / block.x);
        get_inputs<<<grid, block>>>(board, bodies, num_creatures);
        cudaDeviceSynchronize();
        think_and_act<<<grid, block>>>(bodies, num_creatures);
        cudaDeviceSynchronize();

        vector<double> x_vec;
        vector<double> y_vec;
        for (int i = 0; i < num_creatures; i++) {
            x_vec.pb(bodies[i].m_x);
            y_vec.pb(bodies[i].m_y);
        }
        print(x_vec);
        print(y_vec);
        // print(-1);
        // cerr << n << endl;
        // sleep(1);
    }
}