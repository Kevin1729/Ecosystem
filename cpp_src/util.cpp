#include "util.h"
#include <iostream>
#include <random>
#include <sstream>
#include <string>
// Environment-specific constants
double MUTATION_DELETION_RATE;
double MUTATION_INSERTION_RATE;
double MUTATION_FLIP_RATE;
int MAX_CREATURES;
int INIT_CREATURES;
int GRASS_PERIOD;
int GRASS_MAX_HEIGHT;
int GRASS_ENERGY;
int GRASS_HEALTH;

// Creature constants
int COST_BRAIN_CONNECTION;
int COST_MAX_HEALTH;
int COST_MAX_ENERGY;
int COST_MAX_SPEED;
int COST_MOVEMENT;
int STARVATION;
int COST_ATTACK;
// How much energy to regenerate one health
int ENERGY_TO_HEALTH;
// How much energy when spending one health
double HEALTH_TO_ENERGY_RATIO;
// Coefficient of how much energy gained per kill
double KILL_ENERGY_GAIN;
// Coefficient of how much health gained per kill
double KILL_HEALTH_GAIN;
// Coefficient of how much energy idling
double COEFF_BASE_ENERGY;
double BIRTH_THRESHOLD;
int BIRTH_SCATTER;

std::random_device rd;
std::mt19937 gen(rd());

bool mutate_roll(double probability)
{
    std::bernoulli_distribution d(probability);
    return d(gen);
}

int random_int(int lo, int hi)
{
    std::uniform_int_distribution<int> d { lo, hi };
    return d(gen);
}

void read_in_settings()
{
    using namespace std;
    string s;
    int i = 0;
    stringstream oss;
    while (getline(cin, s)) {
        if (s.empty() || s[0] == '#')
            continue;
        istringstream iss(s);
        string _;
        double val;
        iss >> _ >> val;
        oss << val << " ";
    }
    oss >> MUTATION_DELETION_RATE;
    oss >> MUTATION_INSERTION_RATE;
    oss >> MUTATION_FLIP_RATE;
    oss >> MAX_CREATURES;
    oss >> INIT_CREATURES;
    oss >> GRASS_PERIOD;
    oss >> GRASS_MAX_HEIGHT;
    oss >> GRASS_ENERGY;
    oss >> GRASS_HEALTH;
    oss >> COST_BRAIN_CONNECTION;
    oss >> COST_MAX_HEALTH;
    oss >> COST_MAX_ENERGY;
    oss >> COST_MAX_SPEED;
    oss >> COST_MOVEMENT;
    oss >> STARVATION;
    oss >> COST_ATTACK;
    oss >> ENERGY_TO_HEALTH;
    oss >> HEALTH_TO_ENERGY_RATIO;
    oss >> KILL_ENERGY_GAIN;
    oss >> KILL_HEALTH_GAIN;
    oss >> COEFF_BASE_ENERGY;
    oss >> BIRTH_THRESHOLD;
    oss >> BIRTH_SCATTER;

    // cout << BIRTH_SCATTER << endl;
}