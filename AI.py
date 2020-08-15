from snake import NORTH, SOUTH, EAST, WEST

def get_best_direction(snake, food):
    if snake.headY == food.pos[1]:
        if not snake.collision_upon_move(WEST):
            return WEST
        else:
            if not snake.collision_upon_move(NORTH):
                return NORTH
            elif not snake.collision_upon_move(SOUTH):
                return SOUTH
            elif not snake.collision_upon_move(EAST):
                return EAST

    else:
        if not snake.collision_upon_move(NORTH):
            return NORTH
        else:
            if not snake.collision_upon_move(WEST):
                return WEST
            elif not snake.collision_upon_move(EAST):
                return EAST
            elif not snake.collision_upon_move(SOUTH):
                return SOUTH