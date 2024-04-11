import pygame
import random

# Initial setup
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# Game variables
score = 0
speed = 5

# Game objects
troll = pygame.Rect(width//2 - 25, height//2 - 25, 50, 50)
foods = [pygame.Rect(random.randint(0, width-50), random.randint(0, height-50), 50, 50) for _ in range(3)]
obstacles = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle user input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        troll.y -= speed
    elif keys[pygame.K_DOWN]:
        troll.y += speed
    elif keys[pygame.K_LEFT]:
        troll.x -= speed
    elif keys[pygame.K_RIGHT]:
        troll.x += speed
    
    # Check for collision with foods
    for food in foods:
        if troll.colliderect(food):
            if food not in obstacles:  # Check if it is already an obstacle
                score += 1
                obstacles.append(food.copy())
                foods.remove(food)
                foods.append(pygame.Rect(random.randint(0, width-50), random.randint(0, height-50), 50, 50))
                speed += 1
    
    # Check for collision with obstacles or screen edges
    if troll.collidelist(obstacles) != -1 or not screen.get_rect().contains(troll):
        running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw game objects
    pygame.draw.rect(screen, GREEN, troll)
    for food in foods:
        pygame.draw.rect(screen, YELLOW, food)
    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, obstacle)
    
    # Draw score
    score_text = font.render("Score: " + str(score), True, GREEN)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()



# LEDERTEKST:

# kan du legge til kode som forsikrer at trollet ikke dør rett etter den kolliderer med mat siden den blir til hinder imens den rører trollet?