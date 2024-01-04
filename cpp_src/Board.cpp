#include "Board.h"
#include "util.h"
#include <algorithm>

Board::Board(int* _grass, int* _grass_stage)
    : grass { _grass }
    , grass_stage { _grass_stage }
{
    for (int i = 0; i < BOARD_WIDTH; i++) {
        for (int j = 0; j < BOARD_HEIGHT; j++) {
            // grass[i][j] = GRASS_MAX_HEIGHT / 2;
            int idx = i * BOARD_HEIGHT + j;
            grass[idx] = GRASS_MAX_HEIGHT;
            grass_stage[idx] = 0;
        }
    }
}