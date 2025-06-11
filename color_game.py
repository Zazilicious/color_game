import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings (updated resolution)
WIDTH, HEIGHT = 1280, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Guessing Game")

# Fonts
FONT = pygame.font.SysFont(None, 36)
BIG_FONT = pygame.font.SysFont(None, 48)

# Colors dictionary
COLOR_OPTIONS = {
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Purple': (128, 0, 128),
    'Cyan': (0, 255, 255),
    'Orange': (255, 165, 0),
    'Pink': (255, 192, 203)
}

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = (200, 200, 200)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        text_surf = FONT.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def new_round():
    correct_color = random.choice(list(COLOR_OPTIONS.keys()))
    color_value = COLOR_OPTIONS[correct_color]
    options = random.sample([c for c in COLOR_OPTIONS if c != correct_color], 3)
    options.append(correct_color)
    random.shuffle(options)
    return correct_color, color_value, options

def draw_screen(color_value, buttons, score, rounds, max_rounds):
    SCREEN.fill((255, 255, 255))

    # Bigger color square (300x300)
    square_size = 300
    square_x = WIDTH // 2 - square_size // 2
    square_y = 100
    pygame.draw.rect(SCREEN, color_value, (square_x, square_y, square_size, square_size))
    pygame.draw.rect(SCREEN, (0, 0, 0), (square_x, square_y, square_size, square_size), 2)

    for btn in buttons:
        btn.draw(SCREEN)

    text = f"Score: {score} | Round: {rounds}/{max_rounds}"
    SCREEN.blit(FONT.render(text, True, (0, 0, 0)), (20, 20))
    pygame.display.flip()

def show_feedback(message):
    SCREEN.fill((255, 255, 255))
    msg = BIG_FONT.render(message, True, (0, 0, 0))
    SCREEN.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(1500)

def game_over_screen(score):
    SCREEN.fill((255, 255, 255))
    msg = BIG_FONT.render(f"Game Over! Final Score: {score}", True, (0, 0, 0))
    SCREEN.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    score, rounds = 0, 0
    max_rounds = 10
    running = True

    while running and rounds < max_rounds:
        correct_color, color_value, options = new_round()
        rounds += 1

        # Spread buttons further apart on larger screen
        start_y = 450
        button_height = 50
        spacing = 60
        buttons = [
            Button(WIDTH // 2 - 150, start_y + i * spacing, 300, button_height, text)
            for i, text in enumerate(options)
        ]

        guessed = False
        feedback_message = ""

        while not guessed:
            draw_screen(color_value, buttons, score, rounds, max_rounds)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked_button = next((btn for btn in buttons if btn.is_clicked(event.pos)), None)
                    if clicked_button:
                        if clicked_button.text == correct_color:
                            score += 1
                            feedback_message = "Correct!"
                        else:
                            feedback_message = f"Wrong! Correct answer was {correct_color}"
                        guessed = True

        show_feedback(feedback_message)

    game_over_screen(score)
    pygame.quit()

if __name__ == "__main__":
    main()
