import pygame
import random

# Constont values
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (180, 180, 180)
RED = (255, 0, 0)

# Preparation of pygame related things
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Calculation of all possible spaces
spaces = []
occupiedSpaces = []
for y in range(0, HEIGHT, 50):
    for x in range(0, WIDTH, 50):
        spaces.append([x, y])

# Definition of safety space (the spaces where the safety zone is going to be) and then deletion of those spaces from the list of all possivle spaces
row1Y = 250
row2Y = row1Y+50
safetySpaces = [
    [0, row1Y], [50, row1Y], [700, row1Y], [750, row1Y],
    [0, row2Y], [50, row2Y], [700, row2Y], [750, row2Y]
    ]
for space in safetySpaces:
    spaces.remove(space)

# Super class
class Entity:
    # Initiation where the coordinate variables are set
    def __init__(self):
        self.coordinates = spaces[random.randint(0, len(spaces)-1)]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)   

# The player class
class Player(Entity):
    # Initiation where the player speed int, points int, and carries bool is set
    def __init__(self):
        super().__init__()
        self.speed = 1
    # Function for movement check and execution
    def movement(self, spaces: list, occupiedSpaces: list, safetySpaces: list, xDirection: int, yDirection: int) -> list:
        if [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in spaces or [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in safetySpaces:
            self.coordinates = [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    # A function to be called each update
    def update(self, sheepobjects):
        self.speed = 1
        for sheep in sheepobjects:
            if sheep.carried:
                self.speed = 0.5

# The enemy class
class Ghost(Entity):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.xDirection = [-1, 1][random.randint(0, 1)]
        self.yDirection = [-1, 1][random.randint(0, 1)]
    def movement(self, spaces: list, occupiedSpaces: list):
        if [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in spaces or [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in occupiedSpaces:
            self.coordinates = [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50]
        else:
            self.xDirection *= -1
            self. yDirection *= -1
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    def update(self, playerObject: object):
        global run
        # Checks whether the player is colliding with the ghost, and stops the game if it is.
        if self.coordinates == playerObject.coordinates:
            run = False

# The resource meant to be collected's class
class Sheep(Entity):
    # Initiates the object by inheriting from the entity superclass, and setting a variable for whether it's being carried or not.
    def __init__(self):
        super().__init__()
        self.carried = False
    # Function for movement check and execution
    def movement(self, spaces: list, ghosts: list, safetySpaces: list, xDirection: int, yDirection: int) -> list:
        global points
        if [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in safetySpaces:
            points += 1
            ghosts.append(Ghost(1))
            print(points)
            self.carried = False
            self.__init__()
        elif [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in spaces:
            self.coordinates = [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    # A function that checks things like whether it's within a square of the player.
    def update(self, playerobject: object, spaces: list, ghosts: list, safetySpaces: list):
        global run
        # If the player collides with a sheep that's not being carried while carrying a sheep, the game will stop.
        if playerobject.coordinates == self.coordinates and not self.carried:
            run = False
        # Checks if the player is within a square, and then sets its carried variable to True and remembers where the player is.
        if playerobject.coordinates[0] >= self.coordinates[0]-50 and playerobject.coordinates[0] <= self.coordinates[0]+50 and playerobject.coordinates[1] >= self.coordinates[1]-50 and playerobject.coordinates[1] <= self.coordinates[1]+50 and (True not in [sheepbit.carried for sheepbit in sheep] or self.carried):
            self.carried = True
            if playerobject.coordinates[0] > self.coordinates[0]:
                self.xDirection = 1
            elif playerobject.coordinates[0] < self.coordinates[0]:
                self.xDirection = -1
            else:
                self.xDirection = 0
            if playerobject.coordinates[1] > self.coordinates[1]:
                self.yDirection = 1
            elif playerobject.coordinates[1] < self.coordinates[1]:
                self.yDirection = -1
            else:
                self.yDirection = 0
        # If the if statement returns False, it checks whether it's being carried or not, and moves towards the player if it is.
        elif self.carried:
            self.movement(spaces, ghosts, safetySpaces, self.xDirection, self.yDirection)
            
# The obstacle class
class Wall(Entity):
    def __init__(self):
        super().__init__()
        spaces.remove(self.coordinates)
        occupiedSpaces.append(self.coordinates)

# Creates class objects
player = Player()
walls = [Wall() for i in range(3)]
sheep = [Sheep() for i in range(3)]
ghosts = []


# Game loop
run = True
counter = 0
counter2 = 0
counter3 = 0
points = 0
while run:
    # Loop for checking if you're exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # Handles player input
    if counter == 10//player.speed:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            player.movement(spaces, occupiedSpaces, safetySpaces, 0, 0)
            counter = 0
        elif keys[pygame.K_UP]:
            player.movement(spaces, occupiedSpaces, safetySpaces, 0, -1)
            counter = 0
        elif keys[pygame.K_DOWN]:
            player.movement(spaces, occupiedSpaces, safetySpaces, 0, 1)
            counter = 0
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            player.movement(spaces, occupiedSpaces, safetySpaces, 0, 0)
            counter = 0
        elif keys[pygame.K_LEFT]:
            player.movement(spaces, occupiedSpaces, safetySpaces, -1, 0)
            counter = 0
        elif keys[pygame.K_RIGHT]:
            player.movement(spaces, occupiedSpaces, safetySpaces, 1, 0)
            counter = 0
    else:
        counter += 1
    for ghost in ghosts:
        if counter3 == 10//ghost.speed:
            ghost.movement(spaces, occupiedSpaces)
            counter3 = 0
        else:
            counter3 += 1

    # Update
    player.update(sheep)
    for ghost in ghosts:
        ghost.update(player)
    for sheepbit in sheep:
        sheepbit.update(player, spaces, ghosts, safetySpaces)
    if counter2 < 12:
        counter2 += 1
    else:
        counter2 = 0
    # Draws the screen and its game objects
    screen.fill(BLACK)
    for tileCoordinate in safetySpaces:
        pygame.draw.rect(screen, GREEN, pygame.Rect(tileCoordinate[0], tileCoordinate[1], 50, 50))
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall.rect)
    if counter2 < 7:
        for sheepbit in sheep:
            pygame.draw.rect(screen, WHITE, sheepbit.rect)
    else:
        for sheepbit in sheep:
            pygame.draw.rect(screen, LIGHTGRAY, sheepbit.rect)
    for ghost in ghosts:
        pygame.draw.rect(screen, RED, ghost.rect)
    pygame.draw.rect(screen, YELLOW, player.rect)
    # Updates the display
    pygame.display.flip()
    clock.tick(60)

