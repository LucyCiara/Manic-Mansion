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

# "I denne oppgaven skal du utvikle et spill som vi har kalt PacTroll. Du bør sette av om lag to timer til denne oppgaven. 

# Spillet starter med et spillbrett (svart hovedboks), et troll (grønn boks merket T) og tre matbiter (gule bokser merket M). Trollet skal bevege seg på spillbrettet og spise så mange matbiter som mulig. Trollet har en konstant fart og kan ikke stoppes, men spilleren styrer retningen ved å bruke tastaturet. Hver gang en matbit spises, blir den gjort om til en hindring (grå boks merket H), og en ny matbit plasseres ut på spillbrettet.
# Hvis trollet treffer en av hindringene eller spillbrettets kanter, avsluttes spillet. 

# Funksjonelle krav: 

# Ved oppstart skal grensesnittet se ut omtrent som i illustrasjonen ovenfor til venstre. Spillet skal bestå av et spillbrett, et trollobjekt og tre matobjekter. (Du kan utelate bokstavene på boksene.) 

# Ved oppstart plasseres matobjektene på tre tilfeldige plasseringer på spillbrettet, og trollobjektet plasseres i sentrum. Ingen objekter skal være oppå hverandre. 

# Trollobjektet beveger seg i rolig hastighet i en retning, enten opp, ned, til venstre eller til høyre. Retningen trollobjektet beveger seg i, styres med piltaster (alternativt tastene W, S, A og D). 

# Når trollobjektet treffer et matobjekt, skal det følgende skje: 

# Spilleren får et poeng. 

# Matobjektet gjøres om til et hindringsobjekt som trollobjektet ikke skal treffe igjen. 

# Et nytt matobjekt opprettes et tilfeldig sted på spillbrettet, slik at det alltid er tre matobjekter på spillbrettet. Nye matobjekter skal ikke plasseres på allerede eksisterende objekter. 

# Farten til trollobjektet økes. 

# Antallet poeng spilleren har, skal hele tiden være synlig i grensesnittet. 

# Spillet avsluttes om trollobjektet treffer en av spillbrettets kanter eller et av hindringsobjektene."
# generer pygame kode for meg