#include "../Body.h"
#include "../Genome.h"
#include "../util.h"
#include "test.h"

int main()
{
    vector<bool> s(30);
    rep(i, 0, len(s))
    {
        s[i] = mutate_roll(0.5);
    }
    print(s);
    Genome g(s);
    print(g.get_max_energy());
    print(g.get_max_health());
    print(g.get_max_speed());
    print(g.get_litter_size());

    Body* body = (Body*)malloc(sizeof(Body));
    g.fill_brain(body);
    // for (int i = 0; i < SIZE_HIDDEN_LAYER; i++) {
    //     for (int j = 0; j < SIZE_INPUT_LAYER; j++) {
    //         cout << body->m_hidden_weights[i][j] << " ";
    //     }
    //     cout << endl;
    // }
    auto vs = g.get_mutations(5);
    foreach (_, vs) {
        print(_.m_bitstring);
    }
}