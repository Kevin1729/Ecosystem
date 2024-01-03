#ifndef HOST_UTIL_H_
#define HOST_UTIL_H_

#include <stack>
#include <vector>

struct Board;
struct Body;
struct Creature;

int remove_dead(std::vector<Creature>& creatures, std::stack<int>& available_idx);
void eat_and_attack(Board* board, Body bodies[], int num_bodies);
int birth(std::vector<Creature>& creatures, Body bodies[], int& num_bodies, int& id_gen, std::stack<int>& available_idx);

#endif // HOST_UTIL_H_