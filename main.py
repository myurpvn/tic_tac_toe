import pygame

pygame.init()
pygame.display.set_caption("The Tic-Tac-Toe Game")

screen_size = (400, 400)
half_width = screen_size[0] / 2
half_height = screen_size[1] / 2

screen_center = pygame.Vector2(half_width, half_height)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

font = pygame.font.Font("freesansbold.ttf", 32)
game_music = pygame.mixer.Sound("sound/hot_pursuit.mp3")
victory_music = pygame.mixer.Sound("sound/new_hero_in_town.mp3")
draw_music = pygame.mixer.Sound("sound/dark_star.mp3")

running = True
dt = 0

CENTERS = {
    "c_1": pygame.Vector2(half_width - 100, half_height + 100),
    "c_2": pygame.Vector2(half_width, half_height + 100),
    "c_3": pygame.Vector2(half_width + 100, half_height + 100),
    "c_4": pygame.Vector2(half_width - 100, half_height),
    "c_5": pygame.Vector2(half_width, half_height),
    "c_6": pygame.Vector2(half_width + 100, half_height),
    "c_7": pygame.Vector2(half_width - 100, half_height - 100),
    "c_8": pygame.Vector2(half_width, half_height - 100),
    "c_9": pygame.Vector2(half_width + 100, half_height - 100),
}


class Board:
    def __init__(self) -> None:
        self.state = {
            "c_1": False,
            "c_2": False,
            "c_3": False,
            "c_4": False,
            "c_5": False,
            "c_6": False,
            "c_7": False,
            "c_8": False,
            "c_9": False,
        }

    def update(self, center) -> str:
        if center != "" and (not self.state[center]):
            self.state[center] = True
        return center


class Game:
    def __init__(self) -> None:
        self.game_over = False
        self.draw = False
        self.winner = ""


class Player:
    def __init__(self) -> None:
        self.name = ""
        self.centers = []
        self.won = False
        self.turn = False

    def add_center(self, center) -> bool:
        if center != "":
            self.centers.append(center)
            return True


class Circle(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "circle"
        self.turn = True

    def draw(self, surface) -> None:
        for center in self.centers:
            pygame.draw.circle(
                surface, color="red", center=CENTERS[center], radius=40, width=5
            )


class Cross(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "cross"

    def draw(self, surface) -> None:
        for center in self.centers:

            line_1_start = pygame.Vector2(
                CENTERS[center].x + 40, CENTERS[center].y + 40
            )
            line_1_end = pygame.Vector2(CENTERS[center].x - 40, CENTERS[center].y - 40)
            line_2_start = pygame.Vector2(
                CENTERS[center].x + 40, CENTERS[center].y - 40
            )
            line_2_end = pygame.Vector2(CENTERS[center].x - 40, CENTERS[center].y + 40)

            lines = {
                "line_1": (line_1_start, line_1_end),
                "line_2": (line_2_start, line_2_end),
            }

            for line in lines:
                pygame.draw.line(
                    surface,
                    color="blue",
                    start_pos=lines[line][0],
                    end_pos=lines[line][1],
                    width=5,
                )


def generate_grid() -> None:
    lines = {
        "line_1_s": pygame.Vector2(half_width + 150, half_height - 50),
        "line_1_e": pygame.Vector2(half_width - 150, half_height - 50),
        "line_2_s": pygame.Vector2(half_width + 150, half_height + 50),
        "line_2_e": pygame.Vector2(half_width - 150, half_height + 50),
        "line_3_s": pygame.Vector2(half_width - 50, half_height + 150),
        "line_3_e": pygame.Vector2(half_width - 50, half_height - 150),
        "line_4_s": pygame.Vector2(half_width + 50, half_height + 150),
        "line_4_e": pygame.Vector2(half_width + 50, half_height - 150),
    }

    for i in range(4):
        pygame.draw.line(
            screen,
            "black",
            lines[f"line_{i+1}_s"],
            lines[f"line_{i+1}_e"],
            width=5,
        )


def check_win(player: Player, game: Game) -> bool:
    if len(player.centers) >= 3:
        player.centers.sort()
        centers_string = "+".join(player.centers)
        if (
            ("c_1+c_2+c_3" in centers_string)
            or ("c_4+c_5+c_6" in centers_string)
            or ("c_7+c_8+c_9" in centers_string)
            or ("c_1+c_4+c_7" in centers_string)
            or ("c_2+c_5+c_8" in centers_string)
            or ("c_3+c_6+c_9" in centers_string)
            or ("c_1+c_5+c_9" in centers_string)
            or ("c_3+c_5+c_7" in centers_string)
        ):
            player.won = True
            game.winner = player.name
            game_music.stop()
            victory_music.play(-1)

    return player.won


def check_draw(board: Board, game: Game) -> bool:
    state = [i for i in board.state if board.state[i]]

    if len(state) == 9:
        game.draw = True
        game_music.stop()
        draw_music.play(-1)

    return game.draw


def get_center() -> str:
    click = pygame.mouse.get_pressed()
    center = ""

    if click[0]:
        pos = pygame.mouse.get_pos()
        min_dist = 9999
        for i in CENTERS:
            dist = pygame.math.Vector2(pos).distance_to(CENTERS[i])
            if dist < min_dist:
                min_dist = dist
                center = i

    return center


def switch_turn(circle: Circle, cross: Cross) -> None:
    circle.turn = not circle.turn
    cross.turn = not cross.turn


game_music.play(-1)
game = Game()
board = Board()
circle = Circle()
cross = Cross()

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game.game_over:
                valid = False
                center = board.update(get_center())
                if circle.turn and center not in cross.centers:
                    valid = circle.add_center(center)
                elif cross.turn and center not in circle.centers:
                    valid = cross.add_center(center)

                if valid:
                    switch_turn(circle, cross)

    screen.fill("grey")
    generate_grid()
    circle.draw(screen)
    cross.draw(screen)

    if circle.won or check_win(circle, game):
        text = font.render("Circle Wins", True, "green", "blue")
        screen.blit(text, screen_center)
        game.game_over = True
    elif cross.won or check_win(cross, game):
        text = font.render("Cross Wins", True, "green", "blue")
        screen.blit(text, screen_center)
        game.game_over = True
    else:
        if game.draw or check_draw(board, game):
            text = font.render("Draw", True, "green", "blue")
            screen.blit(text, screen_center)
            game.game_over = True

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
