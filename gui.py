import pygame
import sys
import time
from Rush import RushHourPuzzle, Search

# === PARAMÈTRES D’AFFICHAGE ===
CELL_SIZE = 80
MARGIN = 8
FPS = 2

# === COULEURS ===
WHITE = (250, 250, 250)
BLACK = (0, 0, 0)
GRAY = (210, 210, 210)
LIGHT_GRAY = (230, 230, 230)
RED = (255, 80, 80)
BLUE = (80, 150, 255)
GREEN = (100, 255, 150)
YELLOW = (255, 255, 120)
ORANGE = (255, 180, 80)
PURPLE = (180, 100, 255)
CYAN = (80, 220, 220)

CAR_COLORS = {
    "X": RED,
    "A": BLUE,
    "B": GREEN,
    "C": YELLOW,
    "D": ORANGE,
    "E": PURPLE,
    "F": CYAN,
}


# === AFFICHAGE DU PLATEAU ===
def draw_board(screen, puzzle, offset_x=350, offset_y=50):
    """Dessine le plateau avec décalage à droite."""
    for y in range(puzzle.board_height):
        for x in range(puzzle.board_width):
            rect = pygame.Rect(
                offset_x + x * CELL_SIZE + MARGIN,
                offset_y + y * CELL_SIZE + MARGIN,
                CELL_SIZE - 2 * MARGIN,
                CELL_SIZE - 2 * MARGIN,
            )
            cell = puzzle.board[y][x]
            if cell == "#":
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == " ":
                pygame.draw.rect(screen, LIGHT_GRAY, rect, 1)
            else:
                color = CAR_COLORS.get(cell, (120, 120, 255))
                pygame.draw.rect(screen, color, rect, border_radius=10)
                pygame.draw.rect(screen, BLACK, rect, 2, border_radius=10)

    # Bordure du plateau
    border_rect = pygame.Rect(
        offset_x + MARGIN - 5,
        offset_y + MARGIN - 5,
        puzzle.board_width * CELL_SIZE - MARGIN + 10,
        puzzle.board_height * CELL_SIZE - MARGIN + 10,
    )
    pygame.draw.rect(screen, BLACK, border_rect, 4, border_radius=10)


# === MENU LATERAL ===
def draw_menu(screen, font, hover_index=None):
    """Affiche les boutons du menu amélioré à gauche."""
    screen.fill(WHITE)

    # Titre
    title = font.render(" Rush Hour Solver", True, BLACK)
    screen.blit(title, (40, 40))

    subtitle = pygame.font.SysFont("Arial", 22).render(
        "Choisissez un algorithme :", True, (60, 60, 60)
    )
    screen.blit(subtitle, (60, 100))

    buttons = [
        (" BFS", (60, 160)),
        (" A* (h1)", (60, 240)),
        (" A* (h2)", (60, 320)),
        (" A* (h3)", (60, 400)),
        (" Réinitialiser", (60, 480)),
        (" Quitter", (60, 560)),
    ]

    rects = []
    for i, (text, pos) in enumerate(buttons):
        color = (180, 180, 180) if hover_index == i else (200, 200, 200)
        rect = pygame.Rect(pos[0], pos[1], 220, 60)
        pygame.draw.rect(screen, color, rect, border_radius=12)
        label = font.render(text, True, BLACK)
        screen.blit(label, (pos[0] + 20, pos[1] + 12))
        rects.append((rect, text))

    return rects



def animate_solution(puzzle, actions):
    """Anime la solution et laisse le plateau final affiché."""
    screen_width = 900
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rush Hour Puzzle")

    clock = pygame.time.Clock()

    for move in actions:
        vid, direction = move
        print(f" {vid} -> {direction}")

        for v in puzzle.vehicles:
            if v["id"] == vid:
                if direction == "forward":
                    if v["orientation"] == "H":
                        v["x"] += 1
                    else:
                        v["y"] += 1
                else:
                    if v["orientation"] == "H":
                        v["x"] -= 1
                    else:
                        v["y"] -= 1
                break

        puzzle.setBoard()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)
        draw_board(screen, puzzle, 350, 50)
        pygame.display.flip()
        clock.tick(FPS)

    print(" Solution terminée ! (Plateau final affiché)")


# === PROGRAMME PRINCIPAL ===
def main_gui():
    pygame.init()
    screen = pygame.display.set_mode((900, 650))
    pygame.display.set_caption("Rush Hour Puzzle - Interface Graphique")
    font = pygame.font.SysFont("Arial", 28)

    def load_puzzle():
        p = RushHourPuzzle(0, 0, [], [], [])
        p.setVehicles("1.csv")
        return p

    puzzle = load_puzzle()
    search = Search(puzzle)

    hover_index = None
    running = True

    while running:
        buttons = draw_menu(screen, font, hover_index)
        draw_board(screen, puzzle, 350, 50)
        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        hover_index = None
        for i, (rect, _) in enumerate(buttons):
            if rect.collidepoint(mouse_pos):
                hover_index = i
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, text in buttons:
                    if rect.collidepoint(mouse_pos):
                        if "BFS" in text:
                            print("\n=====  BFS =====")
                            sol = search.BFS()
                            if sol:
                                animate_solution(puzzle, sol)

                        elif "h1" in text:
                            print("\n=====  A* (h1) =====")
                            sol = search.AStar("h1")
                            if sol:
                                animate_solution(puzzle, sol)

                        elif "h2" in text:
                            print("\n=====  A* (h2) =====")
                            sol = search.AStar("h2")
                            if sol:
                                animate_solution(puzzle, sol)

                        elif "h3" in text:
                            print("\n=====  A* (h3) =====")
                            sol = search.AStar("h3")
                            if sol:
                                animate_solution(puzzle, sol)

                        elif "Réinitialiser" in text:
                            print("\n Réinitialisation du plateau...")
                            puzzle = load_puzzle()
                            search = Search(puzzle)

                        elif "Quitter" in text:
                            running = False
                            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_gui()
