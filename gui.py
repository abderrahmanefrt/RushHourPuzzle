import pygame
import sys
import time
import itertools
import heapq
from Rush import RushHourPuzzle, Search

# === PARAMÈTRES D’AFFICHAGE ===
CELL_SIZE = 80
MARGIN = 10
FPS = 2

# === COULEURS ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 80, 80)
BLUE = (80, 150, 255)
GREEN = (100, 255, 150)
YELLOW = (255, 255, 100)
ORANGE = (255, 160, 0)
PURPLE = (160, 80, 255)
CYAN = (0, 200, 200)

CAR_COLORS = {
    "X": RED,
    "A": BLUE,
    "B": GREEN,
    "C": YELLOW,
    "D": ORANGE,
    "E": PURPLE,
    "F": CYAN,
}

# === INTERFACE PYGAME ===
def draw_board(screen, puzzle):
    """Dessine le plateau et les véhicules."""
    screen.fill(WHITE)
    for y in range(puzzle.board_height):
        for x in range(puzzle.board_width):
            rect = pygame.Rect(
                x * CELL_SIZE + MARGIN,
                y * CELL_SIZE + MARGIN,
                CELL_SIZE - 2 * MARGIN,
                CELL_SIZE - 2 * MARGIN,
            )
            cell = puzzle.board[y][x]
            if cell == "#":
                pygame.draw.rect(screen, BLACK, rect)
            elif cell == " ":
                pygame.draw.rect(screen, GRAY, rect, 1)
            else:
                color = CAR_COLORS.get(cell, (120, 120, 255))
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 2)
    pygame.display.flip()


def draw_menu(screen, font):
    """Affiche les boutons du menu."""
    screen.fill(WHITE)
    title = font.render("🚗 Rush Hour Puzzle", True, BLACK)
    screen.blit(title, (CELL_SIZE * 1.5, 30))

    buttons = [
        ("🔵 BFS", (100, 150)),
        ("🟢 A* h1", (100, 250)),
        ("🟠 A* h2", (100, 350)),
        ("🔴 A* h3", (100, 450)),
        ("❌ Quitter", (100, 550)),
    ]
    rects = []
    for text, pos in buttons:
        rect = pygame.Rect(pos[0], pos[1], 300, 60)
        pygame.draw.rect(screen, GRAY, rect)
        label = font.render(text, True, BLACK)
        screen.blit(label, (pos[0] + 20, pos[1] + 10))
        rects.append((rect, text))
    pygame.display.flip()
    return rects


def animate_solution(puzzle, actions):
    """Anime les mouvements de la solution trouvée."""
    pygame.init()
    screen_width = puzzle.board_width * CELL_SIZE
    screen_height = puzzle.board_height * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Rush Hour - Solution")

    clock = pygame.time.Clock()
    draw_board(screen, puzzle)
    time.sleep(1)

    for move in actions:
        vid, direction = move
        print(f"🚗 {vid} -> {direction}")

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

        draw_board(screen, puzzle)
        clock.tick(FPS)

    print("✅ Solution terminée !")
    time.sleep(2)
    pygame.quit()


def main_gui():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Rush Hour Puzzle - Choix de l'algorithme")
    font = pygame.font.SysFont("Arial", 30)

    puzzle = RushHourPuzzle(0, 0, [], [], [])
    puzzle.setVehicles("1.csv") 

    search = Search(puzzle)
    buttons = draw_menu(screen, font)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for rect, text in buttons:
                    if rect.collidepoint(pos):
                        if "BFS" in text:
                            print("\n===== 🔵 BFS =====")
                            sol = search.BFS()
                            if sol:
                                animate_solution(puzzle, sol)
                        elif "h1" in text:
                            print("\n===== 🟢 A* (h1) =====")
                            sol = search.AStar("h1")
                            if sol:
                                animate_solution(puzzle, sol)
                        elif "h2" in text:
                            print("\n===== 🟠 A* (h2) =====")
                            sol = search.AStar("h2")
                            if sol:
                                animate_solution(puzzle, sol)
                        elif "h3" in text:
                            print("\n===== 🔴 A* (h3) =====")
                            sol = search.AStar("h3")
                            if sol:
                                animate_solution(puzzle, sol)
                        elif "Quitter" in text:
                            pygame.quit()
                            sys.exit()


if __name__ == "__main__":
    main_gui()
