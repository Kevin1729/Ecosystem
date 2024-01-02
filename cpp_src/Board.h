#ifndef BOARD_H_
#define BOARD_H_

#include "util.h"

struct Board {
    int grass[BOARD_WIDTH][BOARD_HEIGHT];
    int grass_stage[BOARD_WIDTH][BOARD_HEIGHT] {};
    Board();
};

#endif // BOARD_H_