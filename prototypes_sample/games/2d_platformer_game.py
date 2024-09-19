import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Player properties
player_radius = 20
player_x = WIDTH // 2
player_y = HEIGHT - player_radius
player_speed = 5
jump_speed = 15
gravity = 0.8

# Player physics
player_velocity_y = 0
is_jumping = False

# Platform
platform_width = 200
platform_height = 20
platform_x = WIDTH // 2 - platform_width // 2
platform_y = HEIGHT - 100

# Game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    # Player movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    
    # Jumping
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = -jump_speed
        is_jumping = True

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Collision detection with platform
    if (player_y + player_radius > platform_y and
        player_y + player_radius < platform_y + platform_height and
        player_x > platform_x and
        player_x < platform_x + platform_width):
        player_y = platform_y - player_radius
        player_velocity_y = 0
        is_jumping = False

    # Collision detection with ground
    if player_y + player_radius > HEIGHT:
        player_y = HEIGHT - player_radius
        player_velocity_y = 0
        is_jumping = False

    # Keep player within screen bounds
    player_x = max(player_radius, min(player_x, WIDTH - player_radius))

    # Clear the screen
    screen.fill(WHITE)

    # Draw the platform
    pygame.draw.rect(screen, BLACK, (platform_x, platform_y, platform_width, platform_height))

    # Draw the player
    pygame.draw.circle(screen, RED, (int(player_x), int(player_y)), player_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)