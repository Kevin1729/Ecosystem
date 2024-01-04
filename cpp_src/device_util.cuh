#ifndef DEVICE_UTIL_H_
#define DEVICE_UTIL_H_

struct Board;
struct Body;

__device__ int get_delta(int t, int s, int axis);
__global__ void get_inputs(Board* board, Body* bodies, int num_bodies, int BOARD_WIDTH, int BOARD_HEIGHT);
__global__ void think_and_act(Body* bodies, int num_bodies, int COST_MOVEMENT, double COEFF_BASE_ENERGY, int STARVATION, double HEALTH_TO_ENERGY_RATIO, int ENERGY_TO_HEALTH, int GRASS_MAX_HEIGHT, int GRASS_PERIOD, int BOARD_WIDTH, int BOARD_HEIGHT);
__global__ void grow_grass(Board* board, int GRASS_MAX_HEIGHT, int GRASS_PERIOD, int BOARD_WIDTH, int BOARD_HEIGHT);

#endif // DEVICE_UTIL_H_