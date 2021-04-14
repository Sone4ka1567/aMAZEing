import random


def get_neighbours_for_generator(i_pos, j_pos, maze, types):
    nei = []
    if i_pos > 1 and maze[i_pos - 2][j_pos] == '1' \
            and types[i_pos - 2][j_pos] == 'CELL':  # сверху
        nei.append((i_pos - 2, j_pos, 'up'))
    if i_pos < (len(maze) - 2) and maze[i_pos + 2][j_pos] == '1' \
            and types[i_pos + 2][j_pos] == 'CELL':  # снизу
        nei.append((i_pos + 2, j_pos, 'down'))
    if j_pos > 1 and maze[i_pos][j_pos - 2] == '1' \
            and types[i_pos][j_pos - 2] == 'CELL':  # слева
        nei.append((i_pos, j_pos - 2, 'left'))
    if j_pos < (len(maze[0]) - 2) and maze[i_pos][j_pos + 2] == '1'\
            and types[i_pos][j_pos + 2] == 'CELL':  # справа
        nei.append((i_pos, j_pos + 2, 'right'))
    return nei


def get_neighbours_for_solution(i_pos, j_pos, maze, used):
    nei = []
    if i_pos > 1 and maze[i_pos - 1][j_pos] == '.' \
            and used[i_pos - 2][j_pos] == 0:  # сверху
        nei.append((i_pos - 2, j_pos, 'up'))
    if i_pos < (len(maze) - 2) and maze[i_pos + 1][j_pos] == '.' \
            and used[i_pos + 2][j_pos] == 0:  # снизу
        nei.append((i_pos + 2, j_pos, 'down'))
    if j_pos > 1 and maze[i_pos][j_pos - 1] == '.' \
            and used[i_pos][j_pos - 2] == 0:  # слева
        nei.append((i_pos, j_pos - 2, 'left'))
    if j_pos < (len(maze[0]) - 2) and maze[i_pos][j_pos + 1] == '.'\
            and used[i_pos][j_pos + 2] == 0:  # справа
        nei.append((i_pos, j_pos + 2, 'right'))
    return nei


def map_generator(width, height):  # ПЕРЕДАВАТЬ ЧЕТНЫЕ ЗНАЧЕНИЯ
    maze = []  # изначально заполним все единичками
    types = []
    not_visited = set()
    for i in range(height + 1):
        line = []
        t = []
        for j in range(width + 1):
            line.append('1')
            if i == 0 or i == height or j == 0 or j == width:
                t.append('WALL')
            elif i % 2 == 0 or j % 2 == 0:
                t.append('WALL')
            else:
                t.append('CELL')
                not_visited.add((i, j))
        types.append(t)
        maze.append(line)

    maze[1][1] = 'S'  # старт
    now = (1, 1)
    not_visited.remove(now)
    stack = []

    while len(not_visited) > 0:
        nei = get_neighbours_for_generator(now[0], now[1], maze, types)
        if len(nei) > 0:
            stack.append(now)
            ind = random.randint(0, len(nei) - 1)
            next_cell = nei[ind]
            if next_cell[2] == 'up':
                maze[now[0] - 1][next_cell[1]] = '.'
            if next_cell[2] == 'down':
                maze[now[0] + 1][next_cell[1]] = '.'
            if next_cell[2] == 'left':
                maze[next_cell[0]][now[1] - 1] = '.'
            if next_cell[2] == 'right':
                maze[next_cell[0]][now[1] + 1] = '.'
            now = (next_cell[0], next_cell[1])
            maze[now[0]][now[1]] = '.'
            not_visited.remove(now)
        elif len(stack) > 0:
            now = stack.pop()

    used = [[0 for _ in range(len(maze[0]))] for __ in range(len(maze))]
    ans = solution_generator(maze, used)
    maze[height - 1][width - 1] = 'F'
    with open('map.txt', 'w') as f:
        for i in range(len(maze)):
            s = ''
            for j in range(len(maze[0])):
                s += maze[i][j]
            f.write(s + '\n')
        f.close()

    return ans


def solution_generator(maze, used):
    used[1][1] = 1
    now = (1, 1)
    end = (len(maze) - 2, len(maze[0]) - 2)
    stack = []

    while now != end:
        nei = get_neighbours_for_solution(now[0], now[1], maze, used)
        if len(nei) > 0:
            stack.append(now)
            ind = random.randint(0, len(nei) - 1)
            next_cell = nei[ind]
            if next_cell[2] == 'up':
                used[now[0] - 1][next_cell[1]] = 1
                used[next_cell[0]][next_cell[1]] = 1
            if next_cell[2] == 'down':
                used[now[0] + 1][next_cell[1]] = 1
                used[next_cell[0]][next_cell[1]] = 1
            if next_cell[2] == 'left':
                used[next_cell[0]][now[1] - 1] = 1
                used[next_cell[0]][next_cell[1]] = 1
            if next_cell[2] == 'right':
                used[next_cell[0]][now[1] + 1] = 1
                used[next_cell[0]][next_cell[1]] = 1
            now = (next_cell[0], next_cell[1])
        elif len(stack) > 0:
            now = stack.pop()
    return used


