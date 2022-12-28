import pygame
import random

# Initialize Pygame
pygame.init()

# Set the window size
WIDTH, HEIGHT = 1600, 900

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the title of the window
pygame.display.set_caption("JumpingPlayer")

# Set the frame rate
clock = pygame.time.Clock()
FRAME_RATE = 60

# Load the image
floor = pygame.image.load("floor.png")
player = pygame.image.load("player.png")
obstacle = pygame.image.load("obstacle.png")

# Set a flag to indicate if the game is running
running = True

#Set elements size
floor = pygame.transform.scale(floor, (WIDTH, HEIGHT / 10))
player = pygame.transform.scale(player, (WIDTH / 8, WIDTH / 8))
obstacle = pygame.transform.scale(obstacle, (WIDTH / 15, WIDTH / 15))

# Set the player's starting position
player_x = WIDTH / 5
player_y = HEIGHT - floor.get_height() - player.get_height()

# Set the player's jumping speed
jump_speed = 30

# Set the player's gravity
gravity = 0.6

# Set the player's current y velocity
y_velocity = 0

# Set the player's jump bounds
max_jump_height = HEIGHT * 0.2
on_floor_height = HEIGHT - floor.get_height() - player.get_height()

# Set a flag to indicate if the player is jumping
jumping = False

# Set a flag to indicate if the player is on the ground
on_ground = True

# Environment porperties
# There will be multiple floor and obstacle instances, 
# wich will be reused and moved on the screen from right to left
floor_positions = [(0, HEIGHT - floor.get_height()), (floor.get_width(), HEIGHT - floor.get_height())]

# Speed of the moving player
# The player will actually stai fixed, only the floor and obstacles will move
moving_speed = 5

# Create an empty list to store the cubes
obstacle_positions = []

# Main game loop
while running:
    # ====================================================================
    # Handle events
    # ====================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not jumping:
                    # Start jumping if the player is on the ground
                    jumping = True
                    y_velocity = -jump_speed
                    on_ground = False
    # ====================================================================


    # ====================================================================
    # Handle Player
    # ====================================================================
    # Apply gravity to player's y velocity
    y_velocity += gravity

    # Update player position
    player_y += y_velocity

    # Check if the player is on the ground
    if player_y >= on_floor_height:
        player_y = on_floor_height
        y_velocity = 0
        on_ground = True
        jumping = False
    
    # Check if the player has reached the maximum jump height
    if jumping:
        if player_y < max_jump_height:
            y_velocity = jump_speed
        else:
            jumping = False
    # ====================================================================


    # ====================================================================
    # Handle Moving floor and obstacles
    # ====================================================================
    # Move all floor elements
    for i, floor_pos in enumerate(floor_positions):
        x, y = floor_pos
        x -= moving_speed
        # if any floor is no longer visible, to the left, move again to the right
        if x < -WIDTH:
            x += 2 * WIDTH
        floor_positions[i] = (x, y)

    # Move and handle obstacles
    # Generate a new obstacle position randomly
    
    # Make sure there is aminimum distance between two obstacles
    # Get last obstacle pos
    generate_obstacle = True
    if len(obstacle_positions) > 0 and obstacle_positions[-1][0] >= WIDTH/2:
        generate_obstacle = False

    if generate_obstacle and random.random() < 0.02:
        # Choose a random starting position for the cube
        x = WIDTH
        y = HEIGHT - floor.get_height() - obstacle.get_height()
        # Create a new cube and add it to the list
        obstacle_positions.append((x, y))

    # Move all obstacles
    for i, obs_pos in enumerate(obstacle_positions):
        x, y = obs_pos
        x -= moving_speed
        obstacle_positions[i] = (x, y)

    # Remove any cubes that have moved off the screen
    obstacle_positions = [obstacle_positions for obstacle_positions in obstacle_positions if obstacle.get_width() + obstacle_positions[0] > 0]
    # ====================================================================

    # ====================================================================
    # Check collisions
    # ====================================================================
    # Create the player rectangle
    player_rect = pygame.Rect(player_x, player_y, player.get_width(), player.get_height())

    for i, obs_pos in enumerate(obstacle_positions):
        x, y = obs_pos 
        # Create the obs rectangle
        obs_rect = pygame.Rect(x, y, obstacle.get_width(), obstacle.get_height())

        if player_rect.colliderect(obs_rect):
            running = False

    # ====================================================================

    # ====================================================================
    # Render
    # ====================================================================
    # Clear the screen
    screen.fill((230, 230, 255))
    
    # Draw the floor elements
    for i, floor_pos in enumerate(floor_positions):
        x, y = floor_pos
        screen.blit(floor, (x, y))
    
    # Draw obstacles
    for i, obs_pos in enumerate(obstacle_positions):
        x, y = obs_pos
        screen.blit(obstacle, (x, y))

    # Draw the player
    screen.blit(player, (player_x, player_y))

    # # Draw collisions
    # pygame.draw.rect(screen, (1, 0, 0), player_rect, 5)
    # for i, obs_pos in enumerate(obstacle_positions):
    #     x, y = obs_pos 
    #     # Create the obs rectangle
    #     obs_rect = pygame.Rect(x, y, obstacle.get_width(), obstacle.get_height())
    #     pygame.draw.rect(screen, (1, 0, 0), obs_rect, 5)

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(FRAME_RATE)
    # ====================================================================

# Quit Pygame
pygame.quit()
