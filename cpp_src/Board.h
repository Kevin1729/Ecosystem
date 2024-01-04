#ifndef BOARD_H_
#define BOARD_H_

#include "util.h"

struct Board {
    int* grass;
    int* grass_stage;
    Board(int* _grass, int* _grass_stage);
};

#endif // BOARD_H_