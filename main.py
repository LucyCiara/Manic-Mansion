# Imports the required libraries
import pygame
import random

# Modification note: Instead of having the game board/display be its own class, I just handle everything before and during a game loop.
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

# Calculation of all possible spaces
spaces = []
occupiedSpaces = []
for y in range(0, HEIGHT, 50):
    for x in range(0, WIDTH, 50):
        spaces.append([x, y])

# Definition of safety space (the spaces where the safety zone is going to be) and then deletion of those spaces from the list of all possivle spaces
row1Y = 250
row2Y = row1Y+50
safetySpacesLeft = [
    [0, row1Y], [50, row1Y],
    [0, row2Y], [50, row2Y]
    ]
safetySpacesRight = [
    [700, row1Y], [750, row1Y],
    [700, row2Y], [750, row2Y]
    ]
safetySpaces = safetySpacesLeft+safetySpacesRight
for space in safetySpaces:
    spaces.remove(space)

# Modification note: I use a list for coordinates because i find it cleaner to work with. I also added a Pygame Rectangle variable because it's needed to display something in Pygame. I do placement in __init__(), as I didn't see a point to have it be its own function. I also didn't add a movement function because one of the classes inheriting this one doesn't move, and because movement works differently for the child classes that do move.
# Super class
class Entity:
    # Initiation where the coordinate variables are set
    def __init__(self):
        self.coordinates = spaces[random.randint(0, len(spaces)-1)]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)   

# Modification note: I've made the points a global variable handled by the sheep class. I didn't see a point in having two separate bools for if a sheep was carried, so I only kept it on the sheep side. I handle placing the playerObject in a zone to the left in __init__() instead of in its own function. Collision is handled by the other sibling classes. The sheep becoming carried is handled by the sheep class.
# The player class
class Player(Entity):
    # Initiation where the super class is inherited, the player speed int is set, and the coordinates are changed to the safety space to the left
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.coordinates = safetySpaces[0]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)

    # Function for movement check and execution
    def movement(self, xDirection: int, yDirection: int):
        if [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in spaces or [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50] in safetySpaces:
            self.coordinates = [self.coordinates[0]+xDirection*50, self.coordinates[1]+yDirection*50]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    
    # A function to be called each update that lowers the speed when carrying a sheep
    def update(self):
        self.speed = 1
        for sheepBit in sheep:
            if sheepBit.carried:
                self.speed = 0.5

# Modification note: I gave the ghost class variables for its movement direction, and a speed for reusability. Placement is handled completely by the parent. The movement and change in direction is handled by the movement class. An update class handles collition with the player class.
# The enemy class
class Ghost(Entity):
    # Initiation where the speed is set and the movement direction is randomized to each possible diagonal movement and the super class is inherited
    def __init__(self, speed: int):
        super().__init__()
        self.speed = speed
        self.xDirection = [-1, 1][random.randint(0, 1)]
        self.yDirection = [-1, 1][random.randint(0, 1)]
    
    # Handles movement and bouncing off of the map edges and safety spaces
    def movement(self):
        if [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in spaces or [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in occupiedSpaces:
            self.coordinates = [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50]
        elif [self.coordinates[0]-self.xDirection*50, self.coordinates[1]+self.yDirection*50] in spaces or [self.coordinates[0]-self.xDirection*50, self.coordinates[1]+self.yDirection*50] in occupiedSpaces:
            self.xDirection *= -1
        elif [self.coordinates[0]+self.xDirection*50, self.coordinates[1]-self.yDirection*50] in spaces or [self.coordinates[0]+self.xDirection*50, self.coordinates[1]-self.yDirection*50] in occupiedSpaces:
            self.yDirection *= -1
        else:
            self.xDirection *= -1
            self. yDirection *= -1
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    
    # Checks collision with player and stops the game loop if it happens
    def update(self, playerObject: object):
        global run
        if self.coordinates == playerObject.coordinates:
            run = False

# Modification note: I gave the sheep class a variable for it's original placement, such that I can add it to the available places for sheep to spawn to keep track of which of those spaces are available. The placement of the sheep is handed by the __init__() function just as with the player class. The handling of when the sheep is being carried is done by the movement function instead of its own function. This is because the movement and the being carried are too intertwined to be bothered to separate. The sheep is never properly removed, but is instead reused as the next sheep to spawn by executing the __init__() function. I added an update function for handling collision with the player object. Both in the sense of the player walking into the sheep object while carrying another (causing a game over) and in the sense of being within a tile of the player, causing its status as carried to activate, and causing it to execute its movement.
# The class of the resource meant to be collected
class Sheep(Entity):
    # Initiates the object by inheriting from the entity superclass, changing its position to a random position on the right safetyspaces, and setting a variable for whether it's being carried or not
    def __init__(self):
        super().__init__()
        self.carried = False
        self.coordinates = safetySpacesRight.pop(random.randint(0, len(safetySpacesRight)-1))
        self.originalSpace = self.coordinates
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    
    # Function for movement check and execution, and gives a point before returning to the right safe space and creating a wall and a ghost when reaching the left safe space
    def movement(self):
        global points
        if [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in safetySpacesLeft:
            points += 1
            ghosts.append(Ghost(1))
            walls.append(Wall())
            print(points)
            self.carried = False
            safetySpacesRight.append(self.originalSpace)
            self.__init__()
        elif [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in spaces or [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50] in safetySpaces:
            self.coordinates = [self.coordinates[0]+self.xDirection*50, self.coordinates[1]+self.yDirection*50]
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], 50, 50)
    
    # A function that checks things like whether it's within a square of the player
    def update(self, playerObject: object):
        global run
        # If the player collides with a sheep that's not being carried while carrying a sheep, the game will stop
        if playerObject.coordinates == self.coordinates and not self.carried:
            run = False
        # Checks if the player is within a square, and then sets its carried variable to True and remembers where the player is
        if playerObject.coordinates[0] >= self.coordinates[0]-50 and playerObject.coordinates[0] <= self.coordinates[0]+50 and playerObject.coordinates[1] >= self.coordinates[1]-50 and playerObject.coordinates[1] <= self.coordinates[1]+50 and (True not in [sheepbit.carried for sheepbit in sheep] or self.carried):
            self.carried = True
            if playerObject.coordinates[0] > self.coordinates[0]:
                self.xDirection = 1
            elif playerObject.coordinates[0] < self.coordinates[0]:
                self.xDirection = -1
            else:
                self.xDirection = 0
            if playerObject.coordinates[1] > self.coordinates[1]:
                self.yDirection = 1
            elif playerObject.coordinates[1] < self.coordinates[1]:
                self.yDirection = -1
            else:
                self.yDirection = 0
        # If the if statement returns False, it checks whether it's being carried or not, and moves towards the player if it is
        elif self.carried:
            self.movement()

# Modification note: Placement is handled completely by the parent class.
# The obstacle class
class Wall(Entity):
    # Initiates by inheriting the super class and removing its position from the available spaces for the player
    def __init__(self):
        super().__init__()
        spaces.remove(self.coordinates)
        occupiedSpaces.append(self.coordinates)

# Creates the class objects
player = Player()
walls = [Wall() for i in range(3)]
sheep = [Sheep() for i in range(3)]
ghosts = [Ghost(1)]


# Game loop variables get set
run = True
counter = 0
counter2 = 0
counter3 = 0
points = 0

# Game loop
while run:
    # Loop for checking if you're exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Handles player input and movement. The counter is there to get the player's movement to look clonky and retro
    if counter == 10//player.speed:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and keys[pygame.K_DOWN]:
            player.movement(0, 0)
            counter = 0
        elif keys[pygame.K_UP]:
            player.movement(0, -1)
            counter = 0
        elif keys[pygame.K_DOWN]:
            player.movement(0, 1)
            counter = 0
        if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
            player.movement(0, 0)
            counter = 0
        elif keys[pygame.K_LEFT]:
            player.movement(-1, 0)
            counter = 0
        elif keys[pygame.K_RIGHT]:
            player.movement(1, 0)
            counter = 0
    else:
        counter += 1
    
    # A for loop to handle the movement of the ghosts. The counter is there to do the same thing as with the player
    for ghost in ghosts:
        if counter3 == 10//ghost.speed:
            ghost.movement()
            counter3 = 0
        else:
            counter3 += 1
    
    # Executes the update functions of the various updates
    player.update()
    for ghost in ghosts:
        ghost.update(player)
    for sheepbit in sheep:
        sheepbit.update(player)
    
    # A counter for making the sheep flash white and light gray
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
    
    # Updates the display to show what's being drawn
    pygame.display.flip()
    
    # Caps the FPS at 60. I have found that 60 FPS works the best when it comes to responsiveness of movement.
    clock.tick(60)

