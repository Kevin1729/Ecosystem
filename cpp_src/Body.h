#ifndef BODY_H_
#define BODY_H_

#include "util.h"
struct Genome;

// Keeps track of dynamic values of a creature instance
struct Body {
    bool m_alive { true };
    int m_x;
    int m_y;
    int m_energy;
    int m_health;
    int m_speed;
    int m_max_energy;
    int m_max_health;
    int m_base_energy_use;
    double m_sensory_input[SIZE_INPUT_LAYER] {};
    double m_hidden_values[SIZE_HIDDEN_LAYER] {}; // Important that this is adjacent to sensory input in device memory (no need for hstacking)
    double m_output_values[SIZE_OUTPUT_LAYER] {};
    double m_hidden_weights[SIZE_HIDDEN_LAYER][SIZE_INPUT_LAYER] {};
    double m_output_weights[SIZE_OUTPUT_LAYER][SIZE_INPUT_LAYER + SIZE_HIDDEN_LAYER] {};
    Body(int x, int y, int health, int energy, const Genome& genome);
};

#endif // BODY_H_