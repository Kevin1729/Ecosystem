#include "Board.h"
#include "Body.h"
#include "device_util.cuh"
#include "util.h"
#include <stdio.h>

__device__ int get_delta(int t, int s, int axis)
{
    int d = t - s;
    if (d > (axis / 2)) {
        d -= axis;
    } else if (d < (-axis / 2)) {
        d += axis;
    }
    return d;
}
// puts input vectors in-place into bodies
__global__ void get_inputs(Board* board, Body* bodies, int num_bodies)
{
    int ix = threadIdx.x + blockIdx.x * blockDim.x;

    if (ix < num_bodies && bodies[ix].m_alive) {
        int x = bodies[ix].m_x;
        int y = bodies[ix].m_y;
        // find closest grass
        int dist = BOARD_WIDTH + BOARD_HEIGHT;
        for (int i = 0; i < BOARD_WIDTH; i++) {
            for (int j = 0; j < BOARD_HEIGHT; j++) {
                if (board->grass[i][j]) {
                    int dx = get_delta(i, x, BOARD_WIDTH);
                    int dy = get_delta(j, y, BOARD_HEIGHT);
                    int cand_dist = abs(dx) + abs(dy);
                    if (cand_dist < dist) {
                        dist = cand_dist;
                        bodies[ix].m_sensory_input[NEAREST_GRASS_X] = dx;
                        bodies[ix].m_sensory_input[NEAREST_GRASS_X] = dy;
                    }
                }
            }
        }
        // find closest neighbor
        dist = BOARD_WIDTH + BOARD_HEIGHT;
        for (int i = 0; i < num_bodies; i++) {
            if (i == ix)
                continue;
            int t_i = bodies[i].m_x;
            int t_j = bodies[i].m_y;
            int dx = get_delta(t_i, x, BOARD_WIDTH);
            int dy = get_delta(t_j, y, BOARD_WIDTH);
            int cand_dist = abs(dx) + abs(dy);
            if (cand_dist < dist) {
                dist = cand_dist;
                bodies[ix].m_sensory_input[NEAREST_CREATURE_X] = dx;
                bodies[ix].m_sensory_input[NEAREST_CREATURE_Y] = dy;
                bodies[ix].m_sensory_input[NEAREST_CREATURE_HEALTH] = bodies[i].m_health;
            }
        }
        bodies[ix].m_sensory_input[HEALTH] = bodies[ix].m_health;
        bodies[ix].m_sensory_input[ENERGY] = bodies[ix].m_energy;
        bodies[ix].m_sensory_input[BIAS] = 1;
        // Random will be handled by the host
    }
}

// Does the matrix multiplication, then updates positions
__global__ void think_and_act(Body* bodies, int num_bodies)
{
    int ix = threadIdx.x + blockIdx.x * blockDim.x;
    if (ix < num_bodies && bodies[ix].m_alive) {
        Body& body = bodies[ix];
        double* actions = body.m_output_values;
        for (int i = 0; i < SIZE_HIDDEN_LAYER; i++) {
            for (int j = 0; j < SIZE_INPUT_LAYER; j++) {
                body.m_hidden_values[i] += body.m_hidden_weights[i][j] * body.m_sensory_input[j];
            }
            body.m_hidden_values[i] = atan(body.m_hidden_values[i]);
        }
        for (int i = 0; i < SIZE_OUTPUT_LAYER; i++) {
            for (int j = 0; j < SIZE_INPUT_LAYER + SIZE_HIDDEN_LAYER; j++) {
                body.m_output_values[i] += body.m_output_weights[i][j] * body.m_sensory_input[j];
            }
            body.m_output_values[i] = atan(body.m_output_values[i]);
        }
        // always allow a move
        body.m_x += actions[MOVE_X] * body.m_speed;
        body.m_x = (body.m_x + BOARD_WIDTH) % BOARD_WIDTH;
        body.m_y += actions[MOVE_Y] * body.m_speed;
        body.m_y = (body.m_y + BOARD_HEIGHT) % BOARD_HEIGHT;
        body.m_energy -= (abs(actions[MOVE_X]) + abs(actions[MOVE_Y])) * COST_MOVEMENT;
        body.m_energy -= ceil(body.m_base_energy_use * COEFF_BASE_ENERGY);
        if (body.m_energy < 0) {
            body.m_health -= STARVATION;
            body.m_energy = STARVATION * HEALTH_TO_ENERGY_RATIO * ENERGY_TO_HEALTH;
        }
        // // regenerate
        // else if (body.m_energy >= ENERGY_TO_HEALTH) {
        //     body.m_energy -= ENERGY_TO_HEALTH;
        //     body.m_health = min(body.m_health + 1, body.m_max_health);
        // }
        // grass eating, attacking, and splitting are handled host-side
    }
}

// Grows grass!
__global__ void grow_grass(Board* board)
{
    int ix = threadIdx.x + blockIdx.x * blockDim.x;
    int iy = threadIdx.y + blockIdx.y * blockDim.y;
    if (ix < BOARD_WIDTH && iy < BOARD_HEIGHT && board->grass[ix][iy] < GRASS_MAX_HEIGHT) {
        board->grass_stage[ix][iy]++;
        if (board->grass_stage[ix][iy] == GRASS_PERIOD) {
            board->grass_stage[ix][iy] = 0;
            board->grass[ix][iy]++;
            board->grass[ix][iy] = min(board->grass[ix][iy], GRASS_MAX_HEIGHT);
        }
    }
}