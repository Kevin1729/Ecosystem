#include "Genome.h"
#include "Body.h"
#include "util.h"
#include <cstdint>
#include <iostream>

Genome::Genome(std::vector<bool> bitstring)
{
    m_bitstring = bitstring;
}
Genome::Genome(int length)
{
    for (int i = 0; i < length; i++) {
        m_bitstring.push_back(random_int(0, 1));
    }
}
int Genome::get_max_energy() const
{
    int max_energy = 0;
    for (int i = 0; i < MAX_ENERGY_LENGTH; i++) {
        max_energy |= m_bitstring[MAX_ENERGY + i] << i;
    }
    return max_energy;
}
int Genome::get_max_health() const
{
    int max_health = 0;
    for (int i = 0; i < MAX_HEALTH_LENGTH; i++) {
        max_health |= m_bitstring[MAX_HEALTH + i] << i;
    }
    return max_health;
}
int Genome::get_max_speed() const
{
    int max_speed = 0;
    for (int i = 0; i < MAX_SPEED_LENGTH; i++) {
        max_speed |= m_bitstring[MAX_SPEED + i] << i;
    }
    return max_speed;
}
int Genome::get_litter_size() const
{
    int max_litter_size = 0;
    for (int i = 0; i < MAX_LITTER_LENGTH; i++) {
        max_litter_size |= m_bitstring[MAX_LITTER + i] << i;
    }
    return max_litter_size;
}
int Genome::fill_brain(Body* body) const
{
    int idx = WEIGHTS;
    int num_connections = 0;
    while (idx <= (int)m_bitstring.size() - 16) {
        idx += 16;
        uint16_t bits;
        for (int i = 0; i < 16; i++) {
            bits |= m_bitstring[idx + i] << i;
        }
        // breakdown of bits:
        // 1 bit for whether the specified weight is for input to hidden, or hidden to output
        // 4 bit for src
        // 4 bit for dest
        // 7 bit for weight
        int weight_raw = bits & 0b0111'1111;
        double weight = (double)weight_raw / (1 << 7);
        bits >>= 7;
        int dest = bits & 0b1111;
        bits >>= 4;
        int src = bits & 0b1111;
        bits >>= 4;
        if (bits) {
            if (src >= SIZE_INPUT_LAYER)
                continue;
            if (dest >= SIZE_HIDDEN_LAYER)
                continue;
            // std::cerr << "dest " << dest << ", src " << src << ", weight " << weight << ", type: " << (bits ? "i2h" : "h2o") << '\n';
            body->m_hidden_weights[dest][src] = weight;
        } else {
            if (src >= SIZE_INPUT_LAYER + SIZE_HIDDEN_LAYER)
                continue;
            if (dest >= SIZE_OUTPUT_LAYER)
                continue;
            // std::cerr << "dest " << dest << ", src " << src << ", weight " << weight << ", type: " << (bits ? "i2h" : "h2o") << '\n';
            body->m_output_weights[dest][src] = weight;
        }
        num_connections++;
    }
    return num_connections;
}
std::vector<Genome> Genome::get_mutations(int num) const
{
    std::vector<Genome> ret;
    for (int i = 0; i < num; i++) {
        std::vector<bool> new_bitstring;
        for (bool b : m_bitstring) {
            if (mutate_roll(MUTATION_DELETION_RATE))
                continue;
            if (mutate_roll(MUTATION_FLIP_RATE))
                b ^= 1;
            new_bitstring.push_back(b);
            if (mutate_roll(MUTATION_INSERTION_RATE))
                new_bitstring.push_back(b);
        }
        ret.emplace_back(Genome(new_bitstring));
    }
    return ret;
}
