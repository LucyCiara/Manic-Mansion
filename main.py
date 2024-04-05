import pygame
import random

# Constont values
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
TRANSYELLOW = (255, 255, 0, 100)
GRAY = (128, 128, 128)

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
        self.coordinates = spaces.pop(random.randint(0, len(spaces)-1))
        occupiedSpaces.append(self.coordinates)
        self.x = self.coordinates[0]
        self.y = self.coordinates[1]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)   

# The player class
class Player(Entity):
    # Initiation where the player speed int, points int, and carries bool is set
    def __init__(self):
        super().__init__()
        self.points = 0
        self.carries = False

    # Function for movement check and execution
    def movement(self, spaces: list, occupiedSpaces: list, safetySpaces: list, xDirection: int, yDirection: int) -> list:
        if [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in spaces:
            print("test")
            spaces.append(self.coordinates)
            occupiedSpaces.remove(self.coordinates)
            self.coordinates = [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50]
            occupiedSpaces.append(self.coordinates)
        elif [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in safetySpaces:
            occupiedSpaces.remove(self.coordinates)
            self.coordinates = [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50]
            occupiedSpaces.append(self.coordinates)
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)

# The enemy class
class Ghost(Entity):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed

# The resource meant to be collected's class
class Sheep(Entity):
    def __init__(self):
        super().__init__()
        self.carried = False

# The obstacle class
class Wall(Entity):
    def __init__(self):
        super().__init__()

# Creates class objects
player = Player()
walls = [Wall() for i in range(10)]


# Game loop
run = True
counter = 0
while run:
    # Loop for checking if you're exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Handles player input
    if counter == 12:
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

    # Update
    

    # Draws the screen and its game objects
    screen.fill(BLACK)
    for tileCoordinate in safetySpaces:
        pygame.draw.rect(screen, GREEN, pygame.Rect(tileCoordinate[0], tileCoordinate[1], 50, 50))
    for wall in walls:
        pygame.draw.rect(screen, GRAY, wall.rect)
    pygame.draw.rect(screen, TRANSYELLOW, player.rect)

    # Updates the display
    pygame.display.flip()
    clock.tick(60)

