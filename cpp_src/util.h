#ifndef UTIL_H_
#define UTIL_H_

// Input nodes for a creature:
#define NEAREST_GRASS_X 0
#define NEAREST_GRASS_Y NEAREST_GRASS_X + 1
#define NEAREST_CREATURE_X NEAREST_GRASS_Y + 1
#define NEAREST_CREATURE_Y NEAREST_CREATURE_X + 1
#define NEAREST_CREATURE_HEALTH NEAREST_CREATURE_Y + 1
#define NEAREST_CREATURE_PROXIMITY NEAREST_CREATURE_HEALTH + 1
#define ENERGY NEAREST_CREATURE_PROXIMITY + 1
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
extern double MUTATION_DELETION_RATE;
extern double MUTATION_INSERTION_RATE;
extern double MUTATION_FLIP_RATE;
extern int BOARD_WIDTH;
extern int BOARD_HEIGHT;
extern int MAX_CREATURES;
extern int INIT_CREATURES;
extern int GRASS_PERIOD;
extern int GRASS_MAX_HEIGHT;
extern int GRASS_ENERGY;
extern int GRASS_HEALTH;

// Creature constants
extern int COST_BRAIN_CONNECTION;
extern int COST_MAX_HEALTH;
extern int COST_MAX_ENERGY;
extern int COST_MAX_SPEED;
extern int COST_MOVEMENT;
extern int STARVATION;
extern int COST_ATTACK;
// How much energy to regenerate one health
extern int ENERGY_TO_HEALTH;
// How much energy when spending one health
extern double HEALTH_TO_ENERGY_RATIO;
// Coefficient of how much energy gained per kill
extern double KILL_ENERGY_GAIN;
// Coefficient of how much health gained per kill
extern double KILL_HEALTH_GAIN;
// Coefficient of how much energy idling
extern double COEFF_BASE_ENERGY;
extern double BIRTH_THRESHOLD;
extern int BIRTH_SCATTER;

// Utility functions
bool mutate_roll(double probability); // rolls true with probability
int random_int(int lo, int hi); // returns a random int between lo and hi, inclusive
void read_in_settings();

#endif // UTIL_H_