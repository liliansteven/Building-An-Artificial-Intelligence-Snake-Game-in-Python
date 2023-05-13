from pygame import display, time, draw, QUIT, init, KEYDOWN, K_a, K_s, K_d, K_w
from random import randint
import pygame
from numpy import sqrt
init()  # Initializes the pygame library

done = False  # A flag to indicate whether the game loop should continue or not

# Define some color constants in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

columns = 10  # Number of columns in the grid
rows = 10  # Number of rows in the grid

# Calculate the width and height of each cell in the grid
width = 600
height = 600
widthOfCell = width/columns
heightOfCell = height/rows

direction = 1  # The initial direction of the snake

# Create a screen surface with the specified width and height
screen = display.set_mode([width, height])

# Set the caption of the window
display.set_caption("A*_search_snake")

# Create a Clock object to keep track of time
clock = time.Clock()

# A* search with dynamic input parameters for both initial state and goal state

def finding_path(food1, snake1):
    # Initialize camefrom for the food and all segments of the snake
    food1.camefrom = []
    for s in snake1:
        s.camefrom = []
    # Initialize the open and closed sets and direction array
    openset = [snake1[-1]]
    closedset = []
    dir_array1 = []
    # Loop until the optimal path to the food is found
    while 1:
        # Get the segment with the lowest f score from the open set
        current1 = min(openset, key=lambda x: x.f)
        # Remove the current segment from the open set and add it to the closed set
        openset = [openset[i] for i in range(len(openset)) if not openset[i] == current1]
        closedset.append(current1)
        # Update the g, h, and f scores for each neighbor of the current segment
        for neighbor in current1.neighbors:
            # Only consider neighbors that are not obstacles, not in the closed set, and not part of the snake
            if neighbor not in closedset and not neighbor.obstrucle and neighbor not in snake1:
                tempg = neighbor.g + 1
                if neighbor in openset:
                    if tempg < neighbor.g:
                        neighbor.g = tempg
                else:
                    neighbor.g = tempg
                    openset.append(neighbor)
                neighbor.h = sqrt((neighbor.x - food1.x) ** 2 + (neighbor.y - food1.y) ** 2)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.camefrom = current1
        # If the food segment has been reached, break out of the loop
        if current1 == food1:
            break
    # Trace back the path from the food to the snake's head using the camefrom pointers
    while current1.camefrom:
        if current1.x == current1.camefrom.x and current1.y < current1.camefrom.y:
            dir_array1.append(2) # Up
        elif current1.x == current1.camefrom.x and current1.y > current1.camefrom.y:
            dir_array1.append(0) # Down
        elif current1.x < current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(3) # Left
        elif current1.x > current1.camefrom.x and current1.y == current1.camefrom.y:
            dir_array1.append(1) # Right
        current1 = current1.camefrom
    # Reset the camefrom, f, h, and g values for all segments of the grid
    for i in range(rows):
        for j in range(columns):
            grid[i][j].camefrom = []
            grid[i][j].f = 0
            grid[i][j].h = 0
            grid[i][j].g = 0
    # Return the direction array
    return dir_array1

# Spot Class to intialize some properties for each index in the grid 
class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # f : represents the sum of g and h. This value is used to determine the priority of the node in the open set,
        # which is the set of nodes that are currently being considered for expansion by the algorithm.
        self.f = 0
        # g: represents the cost of the path from the start node to the current node.
        self.g = 0
        # h: represents the estimated cost from the current node to the goal node.
        # This is typically calculated as the straight-line distance between the two nodes in Euclidean space
        # although other heuristics can be used as well.
        self.h = 0

        self.neighbors = []
        self.camefrom = []
        self.obstrucle = False
        if (self.x == 0 or self.y == 0 or self.x == (columns-1) or self.y == (rows-1)) :
            self.obstrucle = True

    def show(self, color):
        # Draws a rectangle on the screen representing the spot
        draw.rect(screen, color, [self.x*heightOfCell+2, self.y*widthOfCell+2, heightOfCell-4, widthOfCell-4])

    def add_neighbors(self):
        # Adds neighboring spots to the current spot
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < columns - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

def print_path(dir_path):
    dir_array = []
    for i in range(len(dir_path)):
        if dir_path[i] == 0:
            dir_array.append("Down")
        elif dir_path[i] == 1:
            dir_array.append("Right")
        elif dir_path[i] == 2:
            dir_array.append("Up")
        elif dir_path[i] == 3:
            dir_array.append("Left")
    dir_array.reverse
    print(dir_array)


# Create a 2D array of Spot objects representing the grid
grid = [[Spot(i, j) for j in range(columns)] for i in range(rows)]

# Add neighbors to each Spot object in the grid
for i in range(rows):
    for j in range(columns):
        grid[i][j].add_neighbors()

# Initialize the snake and food
snake = [grid[round(rows/2)][round(columns/2)]]
food = grid[randint(0, rows-1)][randint(0, columns-1)]
current = snake[-1]

# Get a path to the food using the A* algorithm and store it in an array
dir_array = finding_path(food, snake)
food_array = [food]
while not done:
    clock.tick(4)          # sets the maximum FPS
    screen.fill(BLACK)      # fills the screen with the color black
    print_path(dir_array)   # print the path of the snake
    direction = dir_array.pop(-1)   # gets the next direction from the list of directions

    
    # adds the next spot of the snake based on the chosen direction
    if direction == 0:    # down
        snake.append(grid[current.x][current.y + 1])
    elif direction == 1:  # right
        snake.append(grid[current.x + 1][current.y])
    elif direction == 2:  # up
        snake.append(grid[current.x][current.y - 1])
    elif direction == 3:  # left
        snake.append(grid[current.x - 1][current.y])
    current = snake[-1]     # updates the current spot to the last spot in the snake

    # checks if the snake is on top of the food
    if current.x == food.x and current.y == food.y:
        # if so, generate new food spot and find a new path
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, columns - 1)]
            if not (food.obstrucle or food in snake):
                break
        food_array.append(food)
        dir_array = finding_path(food, snake)

    else:
        # if not, remove the first spot in the snake
        snake.pop(0)

    # draws all the spots in the snake and obstacles on the screen
    for spot in snake:
        spot.show(WHITE)
    for i in range(rows):
        for j in range(columns):
            if grid[i][j].obstrucle:
                grid[i][j].show(RED)

    # draws the food and the head of the snake on the screen
    food.show(GREEN)
    snake[-1].show(BLUE)

    display.flip()   # updates the screen display

    # checks for user input events
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            # changes direction based on user input
            if event.key == K_w and not direction == 0:
                direction = 2
            elif event.key == K_a and not direction == 1:
                direction = 3
            elif event.key == K_s and not direction == 2:
                direction = 0
            elif event.key == K_d and not direction == 3:
                direction = 1
