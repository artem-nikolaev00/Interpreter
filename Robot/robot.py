squares = {
    ' ': [],
    'E': ['EXIT'],
    'T': ['top'],
    'D': ['down'],
    'L': ['left'],
    'R': ['right'],
    'A': ['top', 'right', 'left', 'down'],
    'B': ['top', 'right', 'left'],
    'C': ['top', 'right', 'down'],
    'F': ['top', 'down', 'left'],
    'G': ['down', 'right', 'left'],
    'H': ['top', 'left'],
    'I': ['top', 'down'],
    'J': ['top', 'right'],
    'K': ['left', 'right'],
    'M': ['left', 'down'],
    'N': ['down', 'right']
}


class Robot:

    def __init__(self, x, y, map):
        self.x = x
        self.y = y
        self.map = map

    def __repr__(self):
        return f'x_coordinate = {self.x}, y_coordinate = {self.y}\n'

    def show(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if i == self.y and j == self.x:
                    print('X', end='')
                else:
                    if self.map[i][j].types == 'A':
                        print('A', end='')
                    elif self.map[i][j].types == 'EMPTY':
                        print(' ', end='')
                    elif self.map[i][j].types == 'EXIT':
                        print('E', end='')
                    elif self.map[i][j].types == 'T':
                        print('T', end='')
                    elif self.map[i][j].types == 'D':
                        print('D', end='')
                    elif self.map[i][j].types == 'L':
                        print('L', end='')
                    elif self.map[i][j].types == 'R':
                        print('R', end='')
                    elif self.map[i][j].types == 'B':
                        print('B', end='')
                    elif self.map[i][j].types == 'C':
                        print('C', end='')
                    elif self.map[i][j].types == 'F':
                        print('F', end='')
                    elif self.map[i][j].types == 'G':
                        print('G', end='')
                    elif self.map[i][j].types == 'H':
                        print('H', end='')
                    elif self.map[i][j].types == 'I':
                        print('I', end='')
                    elif self.map[i][j].types == 'J':
                        print('J', end='')
                    elif self.map[i][j].types == 'K':
                        print('K', end='')
                    elif self.map[i][j].types == 'M':
                        print('N', end='')
                    elif self.map[i][j].types == 'N':
                        print('N', end='')
            print()

    def move(self, direction):
        if (((self.y - 1) > -1) and ((self.y + 1) < len(self.map))) and \
                (((self.x - 1) > -1) and ((self.x + 1) < len(self.map[0]))):
            if direction == 'top' and \
                    (self.map[self.y - 1][self.x].down != True and \
                    self.map[self.y][self.x].top != True):
                self.y -= 1
                return 1
            elif direction == 'bottom' and \
                    (self.map[self.y + 1][self.x].top != True and \
                    self.map[self.y][self.x].down != True):
                self.y += 1
                return 1
            elif direction == 'left' and \
                    (self.map[self.y][self.x - 1].right != True and \
                    self.map[self.y][self.x].left != True):
                self.x -= 1
                return 1
            elif direction == 'right' and \
                    (self.map[self.y][self.x + 1].left != True and \
                    self.map[self.y][self.x].right != True):
                self.x += 1
                return 1
        else:
            if direction == 'top' and \
                    self.map[self.y][self.x].top != True:
                self.y -= 1
                return 1
            elif direction == 'bottom' and \
                    self.map[self.y][self.x].down != True:
                self.y += 1
                return 1
            elif direction == 'left' and \
                    self.map[self.y][self.x].left != True:
                self.x -= 1
                return 1
            elif direction == 'right' and \
                    self.map[self.y][self.x].right != True:
                self.x += 1
                return 1
        return 0

    def exit(self):
        if self.map[self.y][self.x].types == 'EXIT':
            return 1
        return 0