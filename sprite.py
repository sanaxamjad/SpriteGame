import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FPS = 60

# Classes
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.Surface((10, 100))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_y = 0
        self.speed = speed

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, 5])

    def update(self):
        global player_score, computer_score  # Declare as global variables
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ball collision with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1

        # Ball collision with paddles
        if pygame.sprite.spritecollideany(self, paddles):
            self.speed_x *= -1
            # Increase ball speed
            self.speed_x += 0.1 * self.speed_x / abs(self.speed_x)
            self.speed_y += 0.1 * self.speed_y / abs(self.speed_y)

        # Ball leaving the screen
        if self.rect.left <= 0:
            self.reset()
            # Increase computer score
            computer_score += 1
        elif self.rect.right >= SCREEN_WIDTH:
            self.reset()
            # Increase player score
            player_score += 1

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tennis Game")

# Create sprite groups
all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()

# Create paddles
player_paddle = Paddle(20, SCREEN_HEIGHT // 2, 8)  # Increased speed to 8
computer_paddle = Paddle(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2, 5)  # Default speed is 5
all_sprites.add(player_paddle, computer_paddle)
paddles.add(player_paddle, computer_paddle)

# Create ball
ball = Ball()
all_sprites.add(ball)

# Game variables
player_score = 0
computer_score = 0
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player paddle control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_paddle.speed_y = -player_paddle.speed
    elif keys[pygame.K_DOWN]:
        player_paddle.speed_y = player_paddle.speed
    else:
        player_paddle.speed_y = 0

    # Computer paddle AI
    if ball.rect.centery < computer_paddle.rect.centery:
        computer_paddle.speed_y = -computer_paddle.speed
    elif ball.rect.centery > computer_paddle.rect.centery:
        computer_paddle.speed_y = computer_paddle.speed
    else:
        computer_paddle.speed_y = 0

    # Update
    all_sprites.update()

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw scores
    player_score_text = font.render("Player: " + str(player_score), True, WHITE)
    screen.blit(player_score_text, (50, 20))
    computer_score_text = font.render("Computer: " + str(computer_score), True, WHITE)
    screen.blit(computer_score_text, (SCREEN_WIDTH - 200, 20))

    # Update display
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
