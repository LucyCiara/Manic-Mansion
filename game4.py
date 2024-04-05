import pygame
import random
import time

# Konstante verdier
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
BLINK_TIME = 2  # Blinking duration in seconds

# Oppsett
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Spillvariabler
score = 0
speed = 5

# Spillobjekter
troll = pygame.Rect(WIDTH // 2 - 25, HEIGHT // 2 - 25, 50, 50)
foods = [pygame.Rect(
    random.randint(0, WIDTH - 50),
    random.randint(0, HEIGHT - 50),
    50, 50
) for _ in range(3)]
obstacles = []

# Kovariabler for blinking av matobjekter
blink_start_time = time.time()
blink_period = True

# Spillloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Håndter brukerinndata
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        troll.y -= speed
    elif keys[pygame.K_DOWN]:
        troll.y += speed
    elif keys[pygame.K_LEFT]:
        troll.x -= speed
    elif keys[pygame.K_RIGHT]:
        troll.x += speed

    # Sjekk kollisjon med matobjekter
    for food in foods:
        if troll.colliderect(food):
            if food not in obstacles and time.time() - blink_start_time > BLINK_TIME:
                score += 1
                blink_start_time = time.time()
                
                obstacles.append(food.copy())
                foods.remove(food)
                foods.append(pygame.Rect(
                    random.randint(0, WIDTH - 50),
                    random.randint(0, HEIGHT - 50),
                    50, 50
                ))
                speed += 1
                
            else:
                troll.x -= troll.x % speed  # Tilbakestill posisjon for å unngå overlapping
        
        # Blinkende farge på matobjekter
        if time.time() - blink_start_time < BLINK_TIME:
            if blink_period:
                pygame.draw.rect(screen, YELLOW, food)
            else:
                pygame.draw.rect(screen, GRAY, food)
            blink_period = not blink_period
        else:
            pygame.draw.rect(screen, YELLOW, food)

    # Sjekk kollisjon med hindringer eller skjermkanter
    if troll.collidelist(obstacles) != -1 or not screen.get_rect().contains(troll):
        running = False

    # Tøm skjermen
    screen.fill(BLACK)

    # Tegn spillobjekter
    pygame.draw.rect(screen, GREEN, troll)
    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, obstacle)
    for food in foods:
        pygame.draw.rect(screen, YELLOW, food)

    # Tegn poengsum
    score_text = font.render("Poeng: " + str(score), True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()


# I denne versjonen av programmet har jeg endret slik at maten blir tegnet, og slik at blink time skjer før maten blir et hinder. det funker fortsatt ikke.