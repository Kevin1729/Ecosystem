#include "../Body.h"
#include "../Creature.h"
#include "../Genome.h"
#include "../util.h"
#include "test.h"

int main()
{
    constexpr int s_body = sizeof(Body);
    ll num_creatures = 5;
    Body* b = (Body*)calloc(num_creatures, s_body);

    vector<Creature> creatures;
    creatures.reserve(2 * num_creatures);
    for (int i = 0; i < num_creatures; i++) {
        int x = random_int(0, BOARD_WIDTH - 1);
        int y = random_int(0, BOARD_HEIGHT - 1);
        Genome g(1000);
        creatures.emplace_back(Creature(x, y, 100, 1, 0, b + i, g));
    }
    for (int idx = 0; idx < num_creatures; idx++) {
        print("CREATURE", idx, ":");
        for (int i = 0; i < SIZE_HIDDEN_LAYER; i++) {
            for (int j = 0; j < SIZE_INPUT_LAYER; j++) {
                cout << b[idx].m_hidden_weights[i][j] << " ";
            }
            cout << endl;
        }
    }
    free(b);
}