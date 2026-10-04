# READ MEEE
# THIS IS MY FIRST PROJECT IN HIGH SCHOOL AS A FRESHMEN
#I FEEL LIKE THIS WAS A QUICK AND FUN LIL PROJECT 
#HOW TO RUN THE CODE
#in the terminal paste python main.py and the game will pop up

#AI discloser
#I used ai to help me pick out a visual python system in for this case it helped me pick out pygame which is new to me, but i figured it out in the end.






import pygame
import random

pygame.init()

clock = pygame.time.Clock()

WIDTH = 1000
HEIGHT = 600
ROWS = 10
COLS = 10
CELL_SIZE = 60

font = pygame.font.SysFont(None, 40)

bird_x = 800
bird_y = 300
bird_size = 20
bird_velocity = 0
gravity = 0.5
jump_strength = -10

pipe_x = 1000
pipe_width = 60
pipe_gap = 180
pipe_speed = 1.5
pipe_top = random.randint(100, 300)

score = 0
pipe_passed = False
bird_started = False

board = []
numbers = []
revealed = []
flags = []

for row in range(ROWS):
    board_row = []
    numbers_row = []
    revealed_row = []
    flags_row = []

    for col in range(COLS):
        board_row.append(0)
        numbers_row.append(0)
        revealed_row.append(False)
        flags_row.append(False)

    board.append(board_row)
    numbers.append(numbers_row)
    revealed.append(revealed_row)
    flags.append(flags_row)

MINES = 15

for i in range(MINES):
    while True:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        if board[row][col] == 0:
            board[row][col] = 1
            break

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")


def count_mines():
    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == 1:
                continue

            count = 0

            for row_change in [-1, 0, 1]:
                for col_change in [-1, 0, 1]:

                    new_row = row + row_change
                    new_col = col + col_change

                    if 0 <= new_row < ROWS and 0 <= new_col < COLS:

                        if board[new_row][new_col] == 1:
                            count += 1

            numbers[row][col] = count


def draw_grid():

    for row in range(ROWS):
        for col in range(COLS):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if revealed[row][col] == False:

                pygame.draw.rect(
                    screen,
                    (180, 180, 180),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

            else:

                pygame.draw.rect(
                    screen,
                    (220, 220, 220),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

                if board[row][col] == 1:

                    pygame.draw.rect(
                        screen,
                        (0, 0, 0),
                        (x, y, CELL_SIZE, CELL_SIZE)
                    )

                else:

                    number = numbers[row][col]

                    text = font.render(
                        str(number),
                        True,
                        (0, 0, 0)
                    )

                    screen.blit(
                        text,
                        (x + 20, y + 15)
                    )

            if flags[row][col]:

                pygame.draw.polygon(
                    screen,
                    (255, 0, 0),
                    [
                        (x + 20, y + 15),
                        (x + 20, y + 35),
                        (x + 40, y + 25)
                    ]
                )

                pygame.draw.line(
                    screen,
                    (0, 0, 0),
                    (x + 20, y + 15),
                    (x + 20, y + 50),
                    3
                )

            pygame.draw.rect(
                screen,
                (50, 50, 50),
                (x, y, CELL_SIZE, CELL_SIZE),
                2
            )


count_mines()

running = True
game_over = False
you_win = False

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            col = mouse_x // CELL_SIZE
            row = mouse_y // CELL_SIZE

            if col < COLS and row < ROWS:

                if event.button == 3:

                    if revealed[row][col] == False:
                        flags[row][col] = not flags[row][col]

                if event.button == 1:

                    if flags[row][col] == False:

                        if board[row][col] == 1:
                            game_over = True

                        else:
                            revealed[row][col] = True

            if event.button == 1:

                if mouse_x >= 600:
                    bird_started = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and bird_started:
                bird_velocity = jump_strength

    if all(
        revealed[row][col] or board[row][col] == 1
        for row in range(ROWS)
        for col in range(COLS)
    ):
        you_win = True

    if bird_started:

        bird_velocity += gravity
        bird_y += bird_velocity
        pipe_x -= pipe_speed

    if bird_y > HEIGHT - 20:

        bird_y = HEIGHT - 20
        bird_velocity = 0

    if bird_y < 20:

        bird_y = 20
        bird_velocity = 0

    if pipe_x < 600 - pipe_width:

        pipe_x = 1000
        pipe_top = random.randint(100, 300)
        pipe_passed = False

    if pipe_x + pipe_width < bird_x and pipe_passed == False:

        score += 1
        pipe_passed = True

    bird_rect = pygame.Rect(
        bird_x - bird_size,
        bird_y - bird_size,
        bird_size * 2,
        bird_size * 2
    )

    top_pipe = pygame.Rect(
        pipe_x,
        0,
        pipe_width,
        pipe_top
    )

    bottom_pipe = pygame.Rect(
        pipe_x,
        pipe_top + pipe_gap,
        pipe_width,
        HEIGHT - pipe_top - pipe_gap
    )

    if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):

        game_over = True

    if bird_y <= 0 or bird_y >= HEIGHT:

        game_over = True

    screen.fill((150, 200, 255))

    draw_grid()

    pygame.draw.line(
        screen,
        (0, 0, 0),
        (600, 0),
        (600, 600),
        5
    )

    pygame.draw.circle(
        screen,
        (255, 200, 0),
        (bird_x, int(bird_y)),
        bird_size
    )

    if bird_started == False:

        start_text = font.render(
            "click to start",
            True,
            (0, 0, 0)
        )

        screen.blit(
            start_text,
            (680, 270)
        )

    if pipe_x >= 600:

        pygame.draw.rect(
            screen,
            (0, 180, 0),
            (pipe_x, 0, pipe_width, pipe_top)
        )

        pygame.draw.rect(
            screen,
            (0, 180, 0),
            (
                pipe_x,
                pipe_top + pipe_gap,
                pipe_width,
                HEIGHT - pipe_top - pipe_gap
            )
        )

    score_text = font.render(
        "score:" + str(score),
        True,
        (0, 0, 0)
    )

    screen.blit(
        score_text,
        (700, 30)
    )

    pygame.display.flip()

    clock.tick(30)

    if game_over or you_win:

        screen.fill((200, 200, 200))

        if you_win:

            text = font.render(
                "YOU WIN!",
                True,
                (0, 0, 0)
            )

        else:

            text = font.render(
                "GAME OVER",
                True,
                (0, 0, 0)
            )

        screen.blit(
            text,
            (200, 200)
        )

        pygame.draw.rect(
            screen,
            (100, 200, 100),
            (200, 300, 200, 70)
        )

        replay_text = font.render(
            "REPLAY",
            True,
            (0, 0, 0)
        )

        screen.blit(
            replay_text,
            (245, 320)
        )

        pygame.display.flip()

        waiting = True

        while waiting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False
                    waiting = False

                if event.type == pygame.MOUSEBUTTONDOWN:

                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if 200 <= mouse_x <= 400 and 300 <= mouse_y <= 370:

                        game_over = False
                        you_win = False

                        bird_started = False
                        bird_y = 300
                        bird_velocity = 0

                        pipe_x = 1000
                        pipe_top = random.randint(100, 300)

                        score = 0
                        pipe_passed = False

                        board = []
                        numbers = []
                        revealed = []
                        flags = []

                        for row in range(ROWS):

                            board_row = []
                            numbers_row = []
                            revealed_row = []
                            flags_row = []

                            for col in range(COLS):

                                board_row.append(0)
                                numbers_row.append(0)
                                revealed_row.append(False)
                                flags_row.append(False)

                            board.append(board_row)
                            numbers.append(numbers_row)
                            revealed.append(revealed_row)
                            flags.append(flags_row)

                        for i in range(MINES):

                            while True:

                                row = random.randint(0, ROWS - 1)
                                col = random.randint(0, COLS - 1)

                                if board[row][col] == 0:

                                    board[row][col] = 1
                                    break

                        count_mines()

                        waiting = False

            clock.tick(30)

pygame.quit()