#include "Body.h"
#include "Genome.h"

Body::Body(int x, int y, int health, const Genome& genome)
    : m_x { x }
    , m_y { y }
    , m_health { health }
{
    genome.fill_brain(this);
    m_energy = m_max_energy = genome.get_max_energy();
    m_max_health = genome.get_max_health();
    m_speed = genome.get_max_speed();
}