from cell import Cell
import random


class Board:
    def __init__(self, height, width, mode, colors):
        self.height = height
        self.width = width
        self.mode = mode
        self.colors = colors
        self.last_moved = 1
        self.player_colors = ["P0", "P1"]
        self.player_counts = [1, 1]
        self.state = [[Cell() for x in range(width)] for y in range(height)]

    def fill_with_color(self):
        self.state[0][0].color = random.choice(self.colors)


        for y in range(self.height):
            for x in range(self.width):
                if y == 0 and x == 0: 
                    continue
                else:
                    banned = []
                    if y - 1 >= 0:
                        banned.append(self.state[y -1][x].color)
                    if x - 1 >= 0:
                        banned.append(self.state[y][x - 1].color)
                    a = [x for x in self.colors if x not in banned]
                    self.state[y][x].color = random.choice(a)

        # Then, set bottom left corner and top right corner to p0, p1.
        self.state[-1][0].player = 0
        self.state[0][-1].player = 1

        self.player_colors[0] = self.state[-1][0].color
        self.player_colors[1] = self.state[0][-1].color

    def output(self):
        return self.state
    
    def fill(self, player, color):
        current = []

        # Check to make sure we aren't breaking any rules.
        if player == self.last_moved or color in self.player_colors:
            return False

        self.last_moved = player

        if player == 0:
            current.append([0, self.height - 1])
        else:
            current.append([self.width - 1, 0])

        seen = set()
        
        while current:
            next_current = []
            for c in current:
                # This block is visited.
                seen.add((c[0], c[1]))
                self.state[c[1]][c[0]].player = player
                self.state[c[1]][c[0]].color = color

                # If the neighboring block belongs to this player OR it is the next color, then add it
                for direction in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                    next_x = c[0] + direction[0]
                    next_y = c[1] + direction[1]
                    if next_x >= 0 and next_x < self.width:
                        if next_y >= 0 and next_y < self.height:
                            if (next_x, next_y) in seen:
                                continue
                            elif self.state[next_y][next_x].color == color or self.state[next_y][next_x].player == player:
                                next_current.append([next_x, next_y]) 

            # Next set of squares to look at.
            current = next_current

        self.player_counts[player] = len(seen)
        self.last_moved = player
        self.player_colors[player] = color

        print(len(seen))








