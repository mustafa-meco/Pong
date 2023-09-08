import pygame
import random

pygame.init()

# INITIIALS
WIDTH, HEIGHT = 1000, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
run = True
score_left = 0
score_right = 0
direction = [0, 1]
angle = [0, 1, 2]

# colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# for the ball
radius = 15
ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius
ball_vel_x, ball_vel_y = 1, 1

# paddle dimensions
paddle_width, paddle_height = 20, 120
left_paddle_y = right_paddle_y = HEIGHT//2 - paddle_height//2
left_paddle_x, right_paddle_x = 100 - paddle_width//2, WIDTH - 100 - paddle_width//2
right_paddle_vel = left_paddle_vel = 0

# gadgets
left_gadget = right_gadget = 0
left_gadget_remaining = right_gadget_remaining = 5

# main loop
while run:
    wn.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_paddle_vel = -0.9
            if event.key == pygame.K_DOWN:
                right_paddle_vel = 0.9
            if event.key == pygame.K_RIGHT and right_gadget_remaining > 0:
                right_gadget = 1
            if event.key == pygame.K_w:
                left_paddle_vel = -0.9
            if event.key == pygame.K_s:
                left_paddle_vel = 0.9
            if event.key == pygame.K_d and left_gadget_remaining > 0:
                left_gadget = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_vel = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle_vel = 0
        
    
    # ball's movement controls
    if ball_y <= 0 + radius or ball_y >= HEIGHT - radius:
        ball_vel_y *= -1
    if ball_x >= WIDTH - radius:
        ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius
        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_x, ball_vel_y = 0.7, -1.4
            elif ang == 1:
                ball_vel_x, ball_vel_y = 0.7, -0.7
            elif ang == 2:
                ball_vel_x, ball_vel_y = 1.4, -0.7
        elif dir == 1:
            if ang == 0:
                ball_vel_x, ball_vel_y = 0.7, 1.4
            elif ang == 1:
                ball_vel_x, ball_vel_y = 0.7, 0.7
            elif ang == 2:
                ball_vel_x, ball_vel_y = 1.4, 0.7

        ball_vel_x *= -1
        
        score_left += 1

    if ball_x <= 0 + radius:
        ball_x, ball_y = WIDTH//2 - radius, HEIGHT//2 - radius

        dir = random.choice(direction)
        ang = random.choice(angle)
        if dir == 0:
            if ang == 0:
                ball_vel_x, ball_vel_y = 0.7, -1.4
            elif ang == 1:
                ball_vel_x, ball_vel_y = 0.7, -0.7
            elif ang == 2:
                ball_vel_x, ball_vel_y = 1.4, -0.7
        elif dir == 1:
            if ang == 0:
                ball_vel_x, ball_vel_y = 0.7, 1.4
            elif ang == 1:
                ball_vel_x, ball_vel_y = 0.7, 0.7
            elif ang == 2:
                ball_vel_x, ball_vel_y = 1.4, 0.7

        score_right += 1

    # paddle's movement controls
    if right_paddle_y <= 0:
        right_paddle_y = 0
    if right_paddle_y >= HEIGHT - paddle_height:
        right_paddle_y = HEIGHT - paddle_height
    if left_paddle_y <= 0:
        left_paddle_y = 0
    if left_paddle_y >= HEIGHT - paddle_height:
        left_paddle_y = HEIGHT - paddle_height
        
    # collision detection
    # left paddle
    #if ball_x <= left_paddle_x + paddle_width and ball_y >= left_paddle_y and ball_y <= left_paddle_y + paddle_height:
    if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
        if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
            ball_x = left_paddle_x + paddle_width + radius
            if left_gadget == 1:
                ball_vel_x *= -3.5
                left_gadget_remaining -= 1
            else:
                ball_vel_x *= -1
    # right paddle
    # if ball_x >= right_paddle_x and ball_y >= right_paddle_y and ball_y <= right_paddle_y + paddle_height:
    if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
        if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
            ball_x = right_paddle_x - radius 
            if right_gadget == 1:
                ball_vel_x *= -3.5
                right_gadget_remaining -= 1
            else:
                ball_vel_x *= -1

    # scores display
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{score_left} : {score_right}', True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (WIDTH//2, 50)
    wn.blit(text, textRect)


    # gadgets in action
    if left_gadget == 1:
        if left_paddle_x <= ball_x <= left_paddle_x + paddle_width:
            if left_paddle_y <= ball_y <= left_paddle_y + paddle_height:
                ball_x = left_paddle_x + paddle_width + radius
                ball_vel_x *= -3.5
                left_gadget = 0
                left_gadget_remaining -= 1
    if right_gadget == 1:
        if right_paddle_x <= ball_x <= right_paddle_x + paddle_width:
            if right_paddle_y <= ball_y <= right_paddle_y + paddle_height:
                ball_x = right_paddle_x - radius 
                ball_vel_x *= -3.5
                right_gadget = 0
                right_gadget_remaining -= 1
        

    # movements
    ball_x += ball_vel_x
    ball_y += ball_vel_y
    right_paddle_y += right_paddle_vel
    left_paddle_y += left_paddle_vel

    # show gadgets remaining
    # left
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{left_gadget_remaining}', True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (left_paddle_x + paddle_width//2, left_paddle_y + paddle_height + 50)
    wn.blit(text, textRect)
    # right
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f'{right_gadget_remaining}', True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (right_paddle_x + paddle_width//2, right_paddle_y + paddle_height + 50)
    wn.blit(text, textRect)


    # OBJECTS
    pygame.draw.circle(wn, BLUE, (ball_x, ball_y), radius)
    pygame.draw.rect(wn, RED, pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height))
    pygame.draw.rect(wn, RED, pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height))
    pygame.display.update()