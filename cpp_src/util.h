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
#define MUTATION_DELETION_RATE 0.0001
#define MUTATION_INSERTION_RATE 0.0001
#define MUTATION_FLIP_RATE 0.0001
#define BOARD_WIDTH 100
#define BOARD_HEIGHT 100
#define GRASS_PERIOD 10
#define GRASS_MAX_HEIGHT 5
#define GRASS_ENERGY 100
#define GRASS_HEALTH 5

// Creature constants
#define COST_BRAIN_CONNECTION 1
#define COST_MAX_HEALTH 3
#define COST_MAX_ENERGY 2
#define COST_MAX_SPEED 1
#define COST_MOVEMENT 1
#define STARVATION 1
#define COST_ATTACK 5
// How much energy to regenerate one health
#define ENERGY_TO_HEALTH 10
// How much energy when spending one health
#define HEALTH_TO_ENERGY_RATIO 0.2
// Coefficient of how much energy gained per kill
#define KILL_ENERGY_GAIN 1.0
// Coefficient of how much health gained per kill
#define KILL_HEALTH_GAIN 1.0
// Coefficient of how much energy idling
#define COEFF_BASE_ENERGY 1.0
#define BIRTH_THRESHOLD 0.0
#define BIRTH_SCATTER 1

// Utility functions
bool mutate_roll(double probability); // rolls true with probability
int random_int(int lo, int hi); // returns a random int between lo and hi, inclusive
#endif // UTIL_H_