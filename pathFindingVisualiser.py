import pygame
import math
from queue import PriorityQueue

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Path finding algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self,row,col,width,total_rows,colour) -> None:
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.width = width
        self.neighbours = []
        self.total_rows = total_rows
        self.colour = colour

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.colour == RED

    def isOpen(self):
        return self.colour == GREEN
    
    def isBarrier(self):
        return self.colour == BLACK

    def isStart(self):
        return self.colour == ORANGE

    def isPath(self):
        return self.colour == PURPLE

    def isEnd(self):
        return self.colour == TURQUOISE

    def reset(self):
        self.colour = WHITE

    def setClosed(self):
        self.colour = RED

    def setOpen(self):
        self.colour = GREEN
    
    def setBarrier(self):
        self.colour = BLACK

    def setStart(self):
        self.colour = ORANGE

    def setEnd(self):
        self.colour = TURQUOISE

    def setPath(self):
        self.colour = PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.colour, (self.x,self.y,self.width,self.width))
    

    def updateNeighbour(self,grid):
        self.neighbours = []

        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].isBarrier(): #DOWN
            self.neighbours.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].isBarrier(): #UP
            self.neighbours.append(grid[self.row-1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].isBarrier(): #RIGHT
            self.neighbours.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].isBarrier(): #LEFT
            self.neighbours.append(grid[self.row][self.col-1]) 


    def __lt__(self,other):
        return False


def h(p1, p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2)+abs(y1-y2)

class Algorithm:
    def __init__(self,draw,grid,start,end):
        self.draw = draw
        self.grid = grid
        self.start = start
        self.end = end
    
    def reconstruct(self,cameFrom, curr):
        while curr in cameFrom:
            curr = cameFrom[curr] 
            curr.setPath()
            self.draw()
        self.start.setStart()
    
    def aStarAlgorithm(self):
        count = 0
        openSet = PriorityQueue()
        openSet.put((0,count,self.start))
        cameFrom = {}
        gScore = {node: float("inf") for row in self.grid for node in row}
        gScore[self.start] = 0
        fScore = {node: float("inf") for row in self.grid for node in row}
        fScore[self.start] = h(self.start.getPos() , self.end.getPos())

        set = {self.start}

        while not openSet.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current = openSet.get()[2]
            set.remove(current)

            if current == self.end:
                self.reconstruct(cameFrom, self.end)
                self.end.setEnd()
                return True

            for neighbour in current.neighbours:
                temp = gScore[current] + 1
                if temp < gScore[neighbour]:
                    cameFrom[neighbour] = current
                    gScore[neighbour] = temp
                    fScore[neighbour] = temp + h(neighbour.getPos(),self.end.getPos())
                    if neighbour not in set:
                        count += 1
                        openSet.put((fScore[neighbour], count, neighbour))
                        set.add(neighbour)
                        neighbour.setOpen()
                        self.draw() 

            if current != self.start:
                current.setClosed()
            
        return False
    
    def dijkstra(self):
        count = 0
        cameFrom = {}
        openSet = PriorityQueue()
        openSet.put((0,count,self.start))
        set = {self.start}
        fScore = {node: float("inf") for row in self.grid for node in row}
        fScore[self.start] = 0
        while not openSet.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit
            
            current = openSet.get()[2]
            set.remove(current)

            if current == self.end:
                self.reconstruct(cameFrom,current)
                self.end.setEnd()
                return True
            
            for neighbour in current.neighbours:
                temp = fScore[current] + 1
                if temp < fScore[neighbour]:
                    cameFrom[neighbour] = current
                    fScore[neighbour] = temp
                    if neighbour not in set:
                        count += 1
                        openSet.put((fScore,count,neighbour))
                        set.add(neighbour)
                        neighbour.setOpen()
                        self.draw()
            if current != self.start:
                current.setClosed()
        return False


def makeGrid(rows,width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows,WHITE)
            grid[i].append(node)
    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win,GREY, (0,i*gap), (width,i*gap))
    for j in range(rows):
        pygame.draw.line(win,GREY, (j*gap, 0), (j*gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows,width):
    gap = width // rows
    y,x = pos

    row = y // gap 
    col = x // gap
    return row,col

def main(win, width):
    ROWS = 50
    grid = makeGrid(ROWS,width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #left
                pos = pygame.mouse.get_pos()
                row,col = getClickedPos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    node.setStart()
                elif not end and node != start:
                    end = node
                    node.setEnd()
                elif node != start and node != end:
                    node.setBarrier()

            elif pygame.mouse.get_pressed()[2]: #right
                pos = pygame.mouse.get_pos()
                row,col = getClickedPos(pos, ROWS, width)
                node = grid[row][col] 
                if node == start:
                    start = None
                elif node == end:
                    end = None
                node.reset()

            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbour(grid)

                    algorithm = Algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    algorithm.dijkstra()
                
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbour(grid)

                    algorithm = Algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    algorithm.aStarAlgorithm()

                if event.key == pygame.K_c:
                    start = None 
                    end = None
                    grid = makeGrid(ROWS, width)

                if event.key == pygame.K_r:
                    for row in grid:
                        for node in row:
                            if node.isOpen() or node.isClosed() or node.isPath():
                                node.reset()


    pygame.quit()

main(WIN, WIDTH)