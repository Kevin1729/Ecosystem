#include "Creature.h"
#include "Body.h"
#include <algorithm>

Creature::Creature(int x, int y, int health, int energy, int id, int pid, Body* body, const Genome& genome)
    : m_id { id }
    , m_pid { pid }
    , m_body { body }
    , m_genome { genome }
{
    m_litter_size = genome.get_litter_size();
    if (energy == -1)
        energy = genome.get_max_energy();
    if (health == -1)
        health = genome.get_max_health();
    *m_body = Body(x, y, health, energy, genome);
}
