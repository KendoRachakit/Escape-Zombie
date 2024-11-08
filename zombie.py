import pygame
import random
import math

# Initialize pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie FPS Shooter")

# Load player image
player_img = pygame.Surface((50, 50))
player_img.fill(GREEN)
player_rect = player_img.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Bullet settings
bullet_img = pygame.Surface((10, 20))
bullet_img.fill(RED)
bullet_speed = 5
bullets = []

# Zombie settings
zombie_img = pygame.Surface((50, 50))
zombie_img.fill(BLUE)
zombie_speed = 2
zombies = []

# Font for score display
font = pygame.font.SysFont("Arial", 30)

# Game loop
running = True
clock = pygame.time.Clock()

def spawn_zombie():
    x = random.randint(0, SCREEN_WIDTH - 50)
    y = random.randint(0, SCREEN_HEIGHT - 50)
    zombie_rect = zombie_img.get_rect()
    zombie_rect.topleft = (x, y)
    zombies.append(zombie_rect)

def move_bullets():
    global zombies
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            for zombie in zombies[:]:
                if bullet.colliderect(zombie):
                    zombies.remove(zombie)
                    bullets.remove(bullet)
                    break

def move_zombies():
    global player_rect
    for zombie in zombies:
        zx, zy = zombie.center
        px, py = player_rect.center
        angle = math.atan2(py - zy, px - zx)
        zombie.x += int(zombie_speed * math.cos(angle))
        zombie.y += int(zombie_speed * math.sin(angle))

def draw():
    screen.fill(WHITE)
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for zombie in zombies:
        screen.blit(zombie_img, zombie)
    # Draw score
    score_text = font.render(f"Zombies: {len(zombies)}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

def game_over():
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)

# Main game loop
while running:
    clock.tick(FPS)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get key states
    keys = pygame.key.get_pressed()
    
    # Move player
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT] and player_rect.x < SCREEN_WIDTH - player_rect.width:
        player_rect.x += 5
    if keys[pygame.K_UP] and player_rect.y > 0:
        player_rect.y -= 5
    if keys[pygame.K_DOWN] and player_rect.y < SCREEN_HEIGHT - player_rect.height:
        player_rect.y += 5

    # Shoot bullet
    if keys[pygame.K_SPACE]:
        bullet_rect = bullet_img.get_rect()
        bullet_rect.center = player_rect.center
        bullets.append(bullet_rect)

    # Move bullets and check for collisions
    move_bullets()

    # Move zombies
    move_zombies()

    # Spawn zombies at random intervals
    if random.random() < 0.02:
        spawn_zombie()

    # Check game over (if any zombies hit the player)
    for zombie in zombies:
        if player_rect.colliderect(zombie):
            game_over()
            running = False
            break

    # Draw everything
    draw()

# Quit pygame
pygame.quit()