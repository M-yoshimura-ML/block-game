import pygame
import sys
import time

pygame.init()

# screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("ball bounce")

# color setting
black = (0,0,0)
white = (255,255,255)

# ball setting
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
# 5 // 2 => 2, get integer value and centerize
ball = pygame.Rect(screen_width // 2, screen_height//2, ball_radius * 2, ball_radius * 2)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Bounce at wall
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y

    # Draw screen
    screen.fill(black)
    pygame.draw.ellipse(screen, white, ball)
    pygame.display.flip()

    time.sleep(0.01)
