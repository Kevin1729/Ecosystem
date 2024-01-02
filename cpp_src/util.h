#ifndef UTIL_H_
#define UTIL_H_

// Input nodes for a creature:
#define NEAREST_GRASS_X 0
#define NEAREST_GRASS_Y NEAREST_GRASS_X + 1
#define NEAREST_CREATURE_X NEAREST_GRASS_Y + 1
#define NEAREST_CREATURE_Y NEAREST_CREATURE_X + 1
#define NEAREST_CREATURE_HEALTH NEAREST_CREATURE_Y + 1
#define ENERGY NEAREST_CREATURE_HEALTH + 1
#define HEALTH ENERGY + 1
#define RANDOM HEALTH + 1
#define BIAS RANDOM + 1
#define SIZE_INPUT_LAYER BIAS + 1

// Hidden nodes
#define SIZE_HIDDEN_LAYER 5

// Output nodes
#define MOVE_X 0
#define MOVE_Y MOVE_X + 1
#define ATTACK MOVE_Y + 1
#define BIRTH ATTACK + 1
#define SIZE_OUTPUT_LAYER BIRTH + 1

// Environment-specific constants
#define MUTATION_DELETION_RATE 0.1
#define MUTATION_INSERTION_RATE 0.1
#define MUTATION_FLIP_RATE 0.1
#define BOARD_WIDTH 100
#define BOARD_HEIGHT 100
#define GRASS_PERIOD 5
#define GRASS_MAX_HEIGHT 5

// Utility functions
bool mutate_roll(double probability); // rolls true with probability
int random_int(int lo, int hi); // returns a random int between lo and hi, inclusive
#endif // UTIL_H_