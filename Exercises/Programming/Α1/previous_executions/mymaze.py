import numpy as np
from queue import LifoQueue
import random
import matplotlib.pyplot as plt
import sys

class grid:

    def __init__(self, N, S, F, p):        
        ## Make sure start and end are within the grid
        assert N > 2
        assert S[0] < N
        assert S[1] < N
        assert F[0] < N
        assert F[1] < N

        assert S[0] > 0
        assert S[1] > 0
        assert F[0] > 0
        assert F[1] > 0

        self.N = N

        self.grid = np.ones((N, N), dtype=np.int32)
        
        ## Surround the grid with obstacles
        # self.grid[0, :] = 1
        # self.grid[N - 1, :] = 1
        # self.grid[:, 0] = 1
        # self.grid[:, N - 1] = 1

        obstacle_free_points = {S, F}

        ### Fill the grid with obstacles. 
        ### An obstacle at position (x,y) -> grid[x,y]=1
        ### Ensure there is a path from S to F
        ### Your code here ###

        self.start_game(N,S,F)

    def old_start_game(self, N, S, F):
        # for i in range(N):
        #   for n in range(N): 
        #       self.grid[n,i]=1
        cx = S[0]
        cy = S[1]
        self.grid[cx,cy] = 0
        frontier_stack = [] # empty stack
        frontier_stack = self.frontier(S,N)
        print("starting")

        counter = 0

        while not not frontier_stack:
            neighbour_stack = [] # empty stack
            print("     in while before random frontier",counter)
            counter += 1
            next_front = random.choice(frontier_stack)
            print(next_front)
            print("     in while before neighbours ",counter)
            neighbour_stack = self.neighbours(next_front, N)
            print("     in while before random neighbours ",counter)
            random_neighbour = random.choice(neighbour_stack)
            print("     in while before set_between ",counter)
            self.set_between(N,next_front,random_neighbour)
            print("     in while before new frontier ",counter)
            temp_frontier_stack = self.frontier(S,N)
            frontier_stack.remove(next_front)
            for i in temp_frontier_stack:
                frontier_stack.append(i)
            if counter == 10:
                break

        if self.grid[F[0],F[1]] == 1:
            self.grid[F[0],F[1]] = 0

    ##################################################################

    def start_game(self, N, S, F):
        self._N = N
        self._S = S
        self._F = F
        x = S[0]
        y = S[1]
        self.grid[x,y] = 0 # open the first path

        s = set()
        fs = self.__frontier(x,y)
        for f in fs:
            s.add(f)
        
        while s:
            x,y = random.choice(tuple(s))
            s.remove((x,y))
            ns = self.__neighbours(x,y)
            if ns: 
                nx, ny = random.choice(tuple(ns))
                self.__connect(x, y, nx, ny)
            fs = self.__frontier(x,y)
            for f in fs:
                s.add(f)
        if self.grid[F[0],F[1]] == 1:
            self.grid[F[0],F[1]] = 0
        
        ### Surround the grid with obstacles
        # self.grid[0, :] = 1
        # self.grid[N - 1, :] = 1
        # self.grid[:, 0] = 1
        # self.grid[:, N - 1] = 1
    
    def __neighbours(self, x, y):
        """
        Returns the neighbours of cell (x, y)
                The neighbours of a cell are all passages with exact distance two,
                diagonals excluded.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: set of all neighbours
        """
        n = set()
        if x >= 0 and x < N and y >= 0 and y < N:
            if x > 1 and self.grid[x-2, y] == 0:
                n.add((x-2, y))
            if x + 2 < N and self.grid[x+2, y] == 0:
                n.add((x+2, y))
            if y > 1 and self.grid[x][y-2] == 0:
                n.add((x, y-2))
            if y + 2 < N and self.grid[x, y+2] == 0:
                n.add((x, y+2))
        return n


    def __frontier(self, x, y):
        """
        Returns the frontier of cell (x, y)
            The frontier of a cell are all walls with exact distance two,
            diagonals excluded.
        :param x: x coordinate of the cell
        :param y: y coordinate of the cell
        :return: set of all frontier cells
        """
        f = set()
        
        if x >= 0 and x < N and y >= 0 and y < N:
            if x > 1 and self.grid[x-2,y] == 1:
                f.add((x-2,y))
            if x + 2 < N and self.grid[x+2, y] == 1:
                f.add((x+2, y))
            if y > 1 and self.grid[x, y-2] == 1:
                f.add((x, y-2))
            if y + 2 < N and self.grid[x, y+2] == 1:
                f.add((x, y+2))

        return f

    def __connect(self, x1, y1, x2, y2):
        """
        Connects wall (x1, x2) with passage (x2 , x2), who
        are assumed to be of distance two from each other
            Connecting a wall to a passage implies converting
            that wall and the wall between them to passages
        :param x1: x coordinate of the wall
        :param y1: y coordinate of the wall
        :param x2: x coordinate of the passage
        :param y2: y coordinate of the passage
        """
        x = (x1 + x2) // 2
        y = (y1 + y2) // 2
        self.grid[x1, y1] = 0
        self.grid[x, y] = 0

    ###################################################################

    def adjacent(self, node):
        adjacent_nodes = []
        for n in (node[0] - 1, node[1]), (node[0] + 1, node[1]), (node[0], node[1] - 1), (node[0], node[1] + 1):
            if self.grid[n] == 0:
                adjacent_nodes.append(n)

        return adjacent_nodes      

    def draw_map(self, S=None, F=None, path=None):

        image = np.zeros((self.N, self.N, 3), dtype=int)

        image[self.grid == 0] = [255, 255, 255]
        image[self.grid == 1] = [0, 0, 0]
        if S:
            image[S] = [50, 168, 64]
        if F:
            image[F] = [168, 50, 50]
        if path:
            for n in path[1:-1]:
                image[n] = [66, 221, 245]

        plt.imshow(image)
        plt.xticks([])
        plt.yticks([])
        plt.show()


# show different grid sizes with different obstacle densities

for N, S, F, p in (10, (2, 3), (7, 8), .3), (25, (2, 7), (23, 19), .5), (50, (10, 2), (42, 42), .8):
    map = grid(N, S, F, p)
    map.draw_map(S, F)
    # , (10, (2, 3), (7, 8), .3)
    # , (25, (2, 7), (23, 19), .5)
    # , (50, (10, 2), (42, 42), .8)