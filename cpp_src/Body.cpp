#include "Body.h"
#include "Genome.h"

Body::Body(int x, int y, int health, int energy, const Genome& genome)
    : m_x { x }
    , m_y { y }
    , m_health { health }
    , m_energy { energy }
{
    m_base_energy_use = COST_BRAIN_CONNECTION * genome.fill_brain(this);
    m_max_energy = genome.get_max_energy();
    m_base_energy_use += COST_MAX_ENERGY * m_max_energy;
    m_max_health = genome.get_max_health();
    m_base_energy_use += COST_MAX_HEALTH * m_max_health;
    m_speed = genome.get_max_speed();
    m_base_energy_use += COST_MAX_SPEED * m_speed;
}