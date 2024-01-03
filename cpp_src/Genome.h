#ifndef GENOME_H_
#define GENOME_H_

#include "util.h"
#include <vector>

#define MAX_ENERGY 0
#define MAX_ENERGY_LENGTH 8
#define MAX_HEALTH MAX_ENERGY + MAX_ENERGY_LENGTH
#define MAX_HEALTH_LENGTH 8
#define MAX_SPEED MAX_HEALTH + MAX_HEALTH_LENGTH
#define MAX_SPEED_LENGTH 3
#define MAX_LITTER MAX_SPEED + MAX_SPEED_LENGTH
#define MAX_LITTER_LENGTH 3
#define WEIGHTS MAX_LITTER + MAX_LITTER_LENGTH

struct Body;

struct Genome {
    std::vector<bool> m_bitstring;
    Genome(std::vector<bool> bitstring);
    Genome(int length);
    // getters
    int get_max_energy() const;
    int get_max_health() const;
    int get_max_speed() const;
    int get_litter_size() const;
    int fill_brain(Body* body) const;
    std::vector<Genome> get_mutations(int num) const; // returns a vector of num mutated genomes
};

#endif // GENOME_H_