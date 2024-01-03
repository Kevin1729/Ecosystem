#include "Board.h"
#include <algorithm>

Board::Board()
{
    for (int i = 0; i < BOARD_WIDTH; i++) {
        for (int j = 0; j < BOARD_HEIGHT; j++) {
            // grass[i][j] = GRASS_MAX_HEIGHT / 2;
            grass[i][j] = GRASS_MAX_HEIGHT;
        }
    }
}