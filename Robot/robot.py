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
                    print('R', end='')
                else:
                    if self.map[i][j].type == 'WALL':
                        print('W', end='')
                    elif self.map[i][j].type == 'EMPTY':
                        print(' ', end='')
                    elif self.map[i][j].type == 'EXIT':
                        print('E', end='')
            print()



    def move(self, direction):
        if direction == 'UP' and self.map[self.y - 1][self.x].type != 'WALL':
            self.y -= 1
            return True
        elif direction == 'DOWN' and self.map[self.y + 1][self.x].type != 'WALL':
            self.y += 1
            return True
        elif direction == 'LEFT' and self.map[self.y][self.x - 1].type != 'WALL':
            self.x -= 1
            return True
        elif direction == 'RIGHT' and self.map[self.y][self.x + 1].type != 'WALL':
            self.x += 1
            return True
        return False



    def exit(self):
        if self.map[self.y][self.x].type == 'EXIT':
            return True
        return False