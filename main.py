# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("The Tic-Tac-Toe Game")
font = pygame.font.Font("freesansbold.ttf", 32)
half_width = screen.get_width() / 2
half_height = screen.get_height() / 2
clock = pygame.time.Clock()
running = True
game_over = False
dt = 0

player_1 = True

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

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

game_music = pygame.mixer.Sound("sound/hot_pursuit.mp3")
victory_music = pygame.mixer.Sound("sound/new_hero_in_town.mp3")
draw_music = pygame.mixer.Sound("sound/dark_star.mp3")


class Game:
    def __init__(self) -> None:
        self.draw = False
        self.winner = ""


class Player:
    def __init__(self) -> None:
        self.name = ""
        self.centers = {
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
        self.won = False

    def get_centers(self) -> None:
        click = pygame.mouse.get_pressed()
        if click[0]:
            pos = pygame.mouse.get_pos()
            min_dist = 99999
            center = ""

            for i in CENTERS:
                dist = pygame.math.Vector2(pos).distance_to(CENTERS[i])
                if dist < min_dist:
                    min_dist = dist
                    center = i

            if not self.centers[center]:
                self.centers[center] = True


class Circle(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "circle"

    def draw(self, surface) -> None:
        for center in self.centers:
            if self.centers[center]:
                pygame.draw.circle(
                    surface, color="red", center=CENTERS[center], radius=40, width=5
                )


class Cross(Player):
    def __init__(self) -> None:
        super().__init__()
        self.name = "cross"

    def draw(self, surface) -> None:
        for center in self.centers:
            if self.centers[center]:
                line_1_start = pygame.Vector2(
                    CENTERS[center].x + 40, CENTERS[center].y + 40
                )
                line_1_end = pygame.Vector2(
                    CENTERS[center].x - 40, CENTERS[center].y - 40
                )
                line_2_start = pygame.Vector2(
                    CENTERS[center].x + 40, CENTERS[center].y - 40
                )
                line_2_end = pygame.Vector2(
                    CENTERS[center].x - 40, CENTERS[center].y + 40
                )
                pygame.draw.line(
                    surface,
                    color="blue",
                    start_pos=line_1_start,
                    end_pos=line_1_end,
                    width=5,
                )
                pygame.draw.line(
                    surface,
                    color="blue",
                    start_pos=line_2_start,
                    end_pos=line_2_end,
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
    if (
        (player.centers["c_1"] and player.centers["c_2"] and player.centers["c_3"])
        or (player.centers["c_4"] and player.centers["c_5"] and player.centers["c_6"])
        or (player.centers["c_7"] and player.centers["c_8"] and player.centers["c_9"])
        or (player.centers["c_1"] and player.centers["c_4"] and player.centers["c_7"])
        or (player.centers["c_2"] and player.centers["c_5"] and player.centers["c_8"])
        or (player.centers["c_3"] and player.centers["c_6"] and player.centers["c_9"])
        or (player.centers["c_1"] and player.centers["c_5"] and player.centers["c_9"])
        or (player.centers["c_3"] and player.centers["c_5"] and player.centers["c_7"])
    ):
        player.won = True
        game.winner = player.name
        game_music.stop()
        victory_music.play(-1)

    return player.won


def check_draw(player_1: Circle, player_2: Cross, game: Game) -> bool:
    true_centers = [i for i in player_1.centers if player_1.centers[i]] + [
        i for i in player_2.centers if player_2.centers[i]
    ]
    if len(true_centers) == 9:
        game.draw = True
        game_music.stop()
        draw_music.play(-1)

    return game.draw


game_music.play(-1)

game = Game()
circle = Circle()
cross = Cross()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if player_1:
                    circle.get_centers()
                    player_1 = False
                else:
                    cross.get_centers()
                    player_1 = True

    screen.fill("grey")
    generate_grid()
    circle.draw(screen)
    cross.draw(screen)

    if circle.won or check_win(circle, game):
        text = font.render("Circle Wins", True, "green", "blue")
        screen.blit(text, player_pos)
        game_over = True
    elif cross.won or check_win(cross, game):
        text = font.render("Cross Wins", True, "green", "blue")
        screen.blit(text, player_pos)
        game_over = True
    else:
        if game.draw or check_draw(circle, cross, game):
            text = font.render("Draw", True, "green", "blue")
            screen.blit(text, player_pos)
            game_over = True

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
