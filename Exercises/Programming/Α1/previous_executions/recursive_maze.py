# Random Maze Generator using Depth-first Search (Recursive Version)
# http://en.wikipedia.org/wiki/Maze_generation_algorithm
# FB - 20121205
import random
from PIL import Image
imgx = 512; imgy = 512
image = Image.new("RGB", (imgx, imgy))
pixels = image.load()
mx = 40; my = 40 # width and height of the maze
maze = [[0 for x in range(mx)] for y in range(my)]
dx = [0, 1, 0, -1]; dy = [-1, 0, 1, 0] # directions to move in the maze

def GenerateMaze(cx, cy):
    maze[cy][cx] = 1
    while True:
        # find a new cell to add
        nlst = [] # list of available neighbors
        for i in range(4):
            nx = cx + dx[i]; ny = cy + dy[i]
            if nx >= 0 and nx < mx and ny >= 0 and ny < my:
                if maze[ny][nx] == 0:
                    # of occupied neighbors of the candidate cell must be 1
                    ctr = 0
                    for j in range(4):
                        ex = nx + dx[j]; ey = ny + dy[j]
                        if ex >= 0 and ex < mx and ey >= 0 and ey < my:
                            if maze[ey][ex] == 1: ctr += 1
                    if ctr == 1: nlst.append(i)
        # if 1 or more available neighbors then randomly select one and add
        if len(nlst) > 0:
            ir = nlst[random.randint(0, len(nlst) - 1)]
            cx += dx[ir]; cy += dy[ir]
            GenerateMaze(cx, cy)
        else: break

GenerateMaze(0, 0)
# paint the maze
for ky in range(imgy):
    for kx in range(imgx):
        m = maze[int(my * ky / imgy)][int(mx * kx / imgx)] * 255
        pixels[kx, ky] = (m, m, m)
image.save("RecursiveMaze_" + str(mx) + "x" + str(my) + ".png", "PNG")


