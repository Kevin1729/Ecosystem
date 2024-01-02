#include "util.h"
#include <random>

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