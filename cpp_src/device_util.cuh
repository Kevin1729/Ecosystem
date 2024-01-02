#ifndef DEVICE_UTIL_H_
#define DEVICE_UTIL_H_

struct Board;
struct Body;

__device__ int get_delta(int t, int s, int axis);
__global__ void get_inputs(Board* board, Body* bodies, int num_bodies);
__global__ void think_and_act(Body* bodies, int num_bodies);
__global__ void grow_grass(Board* board);

#endif // DEVICE_UTIL_H_