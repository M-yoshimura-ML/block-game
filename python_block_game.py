import pygame
import sys
import time

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# color setting
black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

# font setting
font = pygame.font.Font(None, 36)

# Paddle object
paddle_width = 100
paddle_height = 10
paddle_speed = 10
paddle_acceleration = 5
left_passed_time = 0
right_passed_time = 0
paddle = pygame.Rect(screen_width//2 - paddle_width//2, screen_height - 30, paddle_width, paddle_height)

# ball object
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball_speed_increment = 0.05
ball = pygame.Rect(screen_width//2, screen_height//2, ball_radius * 2, ball_radius * 2)

# block setting
block_width = 60
block_height = 20
block_rows = 5
block_columns = 11
blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_columns):
        block_x = col * (block_width + 10) + 20
        block_y = row * (block_height + 10) + 35
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append(block)
    blocks.append(block_row)


# display count down
for i in range(3, 0, -1):
    screen.fill(black)
    countdown_text = font.render(f"Starting in {i}", True, white)
    screen.blit(countdown_text, (screen_width // 2 - countdown_text.get_width() // 2, screen_height // 2 - countdown_text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

running = True
score = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Manipulate Paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        left_passed_time += 1
        right_passed_time = 0
        paddle_speed = (10 + paddle_acceleration * left_passed_time)
        if paddle.left > 0:
            paddle.left -= paddle_speed
    elif keys[pygame.K_RIGHT]:
        right_passed_time += 1
        left_passed_time = 0
        paddle_speed = (10 + paddle_acceleration * right_passed_time)
        if paddle.right < screen_width:
            paddle.right += paddle_speed
    else:
        left_passed_time = 0
        right_passed_time = 0
        paddle_speed = 0

    # Move ball
    ball.left += ball_speed_x
    ball.top += ball_speed_y

    # Bounce at wall (collision detection)
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_y *= (1 + ball_speed_increment)
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y *= (1 + ball_speed_increment)
        ball_speed_y = -ball_speed_y
    if ball.bottom >= screen_height:
        running = False

    # Ball and Paddle collision detection
    if ball.colliderect(paddle):
        hit_position = (ball.left + ball.right) / 2 - (paddle.left + paddle.right) / 2
        ball_speed_x = hit_position * 0.3
        ball_speed_y = -ball_speed_y

    # Ball and Block collision detection
    for row in blocks:
        for block in row:
            if ball.colliderect(block):
                ball_speed_y = -ball_speed_y
                row.remove(block)
                score += 100
                break

    # Draw screen
    screen.fill(black)
    pygame.draw.rect(screen, blue, paddle)
    pygame.draw.ellipse(screen, white, ball)
    for row in blocks:
        for block in row:
            pygame.draw.rect(screen, green, block)

    # Display score
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    time.sleep(0.03)


# Display score after end of game
screen.fill(black)
final_score_text = font.render(f"Final Score: {score}", True, white)
exit_text = font.render("Press Enter to exit", True, white)
screen.blit(final_score_text,
            (screen_width // 2 - final_score_text.get_width() // 2,
             screen_height // 2 - final_score_text.get_height() // 2))
screen.blit(exit_text,
            (screen_width // 2 - exit_text.get_width() // 2,
             screen_height // 2 - exit_text.get_height() // 2 + 30))
pygame.display.flip()

waiting_for_exit = True
while waiting_for_exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting_for_exit = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            waiting_for_exit = False
            pygame.quit()
            sys.exit()


