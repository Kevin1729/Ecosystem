#include "host_util.h"
#include "Board.h"
#include "Body.h"
#include "Creature.h"
#include "util.h"
#include <algorithm>
#include <iostream>

int remove_dead(std::vector<Creature>& creatures, std::stack<int>& available_idx)
{
    int num_dead = 0;
    for (int i = 0; i < (int)creatures.size(); i++) {
        Creature& c = creatures[i];
        if (c.m_body->m_alive && c.m_body->m_health <= 0) {
            c.m_body->m_alive = false;
            available_idx.push(i);
            num_dead++;
        }
    }
    return num_dead;
}
void eat_and_attack(Board* board, Body bodies[], int num_bodies)
{
    std::vector<Body*> grid[BOARD_WIDTH][BOARD_HEIGHT];
    // initialize grid
    for (int i = 0; i < num_bodies; i++) {
        if (bodies[i].m_alive) {
            grid[bodies[i].m_x][bodies[i].m_y].push_back(bodies + i);
        }
    }
    // eat grass
    for (int i = 0; i < BOARD_WIDTH; i++) {
        for (int j = 0; j < BOARD_HEIGHT; j++) {
            for (Body* b : grid[i][j]) {
                // if attacking, can't eat grass
                int idx = i * BOARD_HEIGHT + j;
                if (board->grass[idx] && b->m_output_values[ATTACK] <= 0) {
                    board->grass[idx]--;
                    b->m_energy = std::min(b->m_energy + GRASS_ENERGY, b->m_max_energy);
                    b->m_health = std::min(b->m_health + GRASS_HEALTH, b->m_max_health);
                    // std::cerr << random_int(0, 100) << "EAT\n";
                }
            }
        }
    }
    // attack
    for (int i = 0; i < BOARD_WIDTH; i++) {
        for (int j = 0; j < BOARD_HEIGHT; j++) {
            int num_occ = grid[i][j].size();
            for (int k = 0; k < num_occ; k++) {
                if (grid[i][j][k]->m_output_values[ATTACK] > 0 && grid[i][j][k]->m_health > 0 && grid[i][j][k]->m_energy >= COST_ATTACK) {
                    grid[i][j][k]->m_energy -= COST_ATTACK;
                    if (num_occ >= 2) {
                        // find a victim
                        int victim = random_int(0, num_occ - 1 - 1);
                        while (!grid[i][j][victim]->m_alive)
                            victim = random_int(0, num_occ - 1 - 1);
                        // victim can't be self
                        victim += (victim >= k);
                        int amount = grid[i][j][victim]->m_health;
                        // grid[i][j][victim]->m_health -= grid[i][j][k]->m_health; // TODO: implement a better attack system
                        grid[i][j][victim]->m_health = -1; // TODO: implement a better attack system
                        if (grid[i][j][victim]->m_health <= 0) {
                            // std::cerr << "KILLED AT " << i << " " << j << std::endl;
                            // if kill was successful
                            // fill energy
                            grid[i][j][k]->m_energy = std::min((int)(grid[i][j][victim]->m_energy * KILL_ENERGY_GAIN + grid[i][j][k]->m_energy), grid[i][j][k]->m_max_energy);
                            // fill some health
                            grid[i][j][k]->m_health = std::min((int)(grid[i][j][k]->m_health + amount * KILL_HEALTH_GAIN), grid[i][j][k]->m_max_health);
                        }
                    }
                }
            }
        }
    }
}
int birth(std::vector<Creature>& creatures, Body bodies[], int& num_bodies, int& id_gen, std::stack<int>& available_idx)
{
    int num_born = 0;
    // birthing full litter size takes half health
    // if below full health, the creature will die
    for (int i = 0; i < (int)creatures.size(); i++) {
        if (creatures[i].m_body->m_alive && creatures[i].m_body->m_output_values[BIRTH] > BIRTH_THRESHOLD) {
            int litter_size = creatures[i].m_litter_size;
            int& health = creatures[i].m_body->m_health;
            int& max_health = creatures[i].m_body->m_max_health;
            if (litter_size == 0)
                continue;
            int litter_health = (max_health / (2.0 * litter_size));
            if (health < max_health / 2.0) {
                if (litter_health != 0)
                    litter_size = health / litter_health;
                health = -1;
            } else {
                health -= max_health / 2.0;
            }
            if (litter_size == 0)
                continue;
            int litter_energy = (creatures[i].m_body->m_energy / litter_size);
            std::vector<Genome> genomes = creatures[i].m_genome.get_mutations(litter_size);
            for (int j = 0; j < litter_size; j++) {
                int idx;
                int x = creatures[i].m_body->m_x;
                int y = creatures[i].m_body->m_y;
                x += random_int(-BIRTH_SCATTER, BIRTH_SCATTER);
                y += random_int(-BIRTH_SCATTER, BIRTH_SCATTER);
                x = (x + BOARD_WIDTH) % BOARD_WIDTH;
                y = (y + BOARD_HEIGHT) % BOARD_HEIGHT;
                if (available_idx.empty()) {
                    return num_born;
                } else {
                    idx = available_idx.top();
                    available_idx.pop();
                    if (idx == (int)creatures.size()) {
                        creatures.emplace_back(Creature(x, y, litter_health, litter_energy, id_gen, creatures[i].m_id, bodies + idx, genomes[j]));
                        if (idx != creatures.size() - 1) {
                            std::cerr << "YOURE DUMB\n"
                                      << idx << " " << creatures.size() << '\n';
                        }
                    } else {
                        creatures[idx] = Creature(x, y, litter_health, litter_energy, id_gen, creatures[i].m_id, bodies + idx, genomes[j]);
                    }
                    num_born++;
                }
                creatures[i].m_body->m_energy -= litter_energy;
                id_gen++;
            }
        }
    }
    return num_born;
}