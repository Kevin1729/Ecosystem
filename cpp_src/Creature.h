#ifndef CREATURE_H_
#define CREATURE_H_

#include "Genome.h"

struct Body;

struct Creature {
    int m_id; // identifies creature, and which body it uses (body is not part of instance vars because of GPU)
    int m_pid; // parent id
    int m_litter_size;
    Body* m_body;
    Genome m_genome;
    Creature(int x, int y, int health, int energy, int id, int pid, Body* body, const Genome& genome);
};

#endif // CREATURE_H_