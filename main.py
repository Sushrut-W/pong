import pygame
import random
import time


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PADDLE_WIDTH = 10
PADDLE_LENGTH = 75
RADIUS = 10

def main():
    # create window
    pygame.init()
    random.seed(time.time())
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong Game")
    
    clock = pygame.time.Clock()
    game_started = False

    # declare players, ball, movement attributes
    p1 = pygame.Rect(5, 5, PADDLE_WIDTH, PADDLE_LENGTH)
    p2 = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH - 5, 5, PADDLE_WIDTH, PADDLE_LENGTH)
    ball = pygame.Rect(SCREEN_WIDTH//2 - RADIUS, SCREEN_HEIGHT//2 - RADIUS, RADIUS*2, RADIUS*2)

    p1_dy = 0
    p2_dy = 0
    ball_dx = random.randint(1, 2) * 0.1 * (-1)**random.randint(0, 1)
    ball_dy = random.randint(1, 2) * 0.1 * (-1)**random.randint(0, 1)

    running = True
    while running:
        dt = clock.tick(60)
        screen.fill(BLACK)

        # start screen
        if not game_started:
            font = pygame.font.SysFont("Consolas", 30)
            text = font.render("Press SPACE to START", True, WHITE)
            text_box = text.get_rect()
            text_box.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(text, text_box)
            
            pygame.display.flip()
            clock.tick(60)
            for e in pygame.event.get():
                if e.type  == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        game_started = True
                        
        # ALWAYS check ball collisions with walls
        if (ball.left <= 0) or (ball.right >= SCREEN_WIDTH):
            return
        if ball.top < 0:
            ball_dy *= -1
            ball.top = 1
        if ball.bottom > SCREEN_HEIGHT:
            ball_dy *= -1
            ball.bottom = SCREEN_HEIGHT - 1

        # ALWAYS check collisions with players
        if (p1.colliderect(ball)) and (p1.left < ball.left):
            ball_dx *= -1
            ball.left = p1.right + 1
        if (p2.colliderect(ball)) and (p2.right > ball.right):
            ball_dx *= -1
            ball.right = p2.left - 1
        
        # ALWAYS check player movement and exit request
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # handle key presses
            if e.type == pygame.KEYDOWN:
                # player 1
                if e.key == pygame.K_w:
                    p1_dy = -0.5
                if e.key == pygame.K_s:
                    p1_dy = 0.5
                # player 2
                if e.key == pygame.K_UP:
                    p2_dy = -0.5
                if e.key == pygame.K_DOWN:
                    p2_dy = 0.5
            # handle key releases
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_w or e.key == pygame.K_s:
                    p1_dy = 0
                if e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                    p2_dy = 0

        # draw sprites on window
        if game_started:
            ball.x += ball_dx * dt
            ball.y += ball_dy * dt
            p1.y += p1_dy * dt
            p2.y += p2_dy * dt

            # stop players from going off screen
            if p1.top < 0:
                p1.top = 0
            if p1.bottom > SCREEN_HEIGHT:
                p1.bottom = SCREEN_HEIGHT
            if p2.top < 0:
                p2.top = 0
            if p2.bottom > SCREEN_HEIGHT:
                p2.bottom = SCREEN_HEIGHT

            pygame.draw.rect(screen, WHITE, p1)
            pygame.draw.rect(screen, WHITE, p2)
            pygame.draw.rect(screen, WHITE, ball, border_radius=7)
        
        # ALWAYS update the screen
        pygame.display.update()
    
    pygame.quit()






if __name__ == "__main__":
    main()