import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bird Constants
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
GRAVITY = 0.25
FLAP_STRENGTH = -5

# Pipe Constants
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 2

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load Images
bird_image = pygame.image.load(os.path.join('bird.png'))
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))

background_image = pygame.image.load(os.path.join('background.png'))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect(center=(50, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += int(self.velocity)

    def flap(self):
        self.velocity = FLAP_STRENGTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted=False):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        if inverted:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

def create_pipe():
    gap_y = random.randint(200, SCREEN_HEIGHT - 200)
    top_pipe = Pipe(SCREEN_WIDTH, gap_y - PIPE_GAP // 2, inverted=True)
    bottom_pipe = Pipe(SCREEN_WIDTH, gap_y + PIPE_GAP // 2)
    return (top_pipe, bottom_pipe)

def show_game_over(screen, score):
    font = pygame.font.Font(None, 74)
    text = font.render('Game Over', True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    screen.blit(text, text_rect)

    score_font = pygame.font.Font(None, 50)
    score_text = score_font.render(f'Score: {score}', True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()
    pygame.time.wait(2000)  # 等待2秒

def main():
    bird = Bird()
    pipes = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(bird)

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 2000)

    score = 0
    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                elif event.key == pygame.K_SPACE and game_over:
                    # 重新开始游戏
                    return main()
            if event.type == SPAWNPIPE and not game_over:
                new_pipes = create_pipe()
                pipes.add(new_pipes)
                all_sprites.add(new_pipes)

        if not game_over:
            all_sprites.update()

            # Collision detection
            if pygame.sprite.spritecollide(bird, pipes, False) or bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
                game_over = True

            # Score update
            for pipe in pipes:
                if pipe.rect.right < bird.rect.left and not getattr(pipe, 'scored', False):
                    score += 0.5  # 每对管道得1分
                    pipe.scored = True

        # Draw background
        screen.blit(background_image, (0, 0))
        all_sprites.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {int(score)}', True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            show_game_over(screen, int(score))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
