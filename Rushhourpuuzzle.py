import csv
import copy

class RushHourPuzzle:
    def __init__(self, boardheight=0, boardwidth=0, vehicles=None, walls=None):
        self.boardheight = boardheight
        self.boardwidth = boardwidth
        self.vehicles = vehicles if vehicles else [] 
        self.walls = walls if walls else []
        self.board = []

    def setVehicles(self, csv_file):
        """
        Lecture du fichier CSV et initialisation des véhicules et des murs.
        Format attendu :
        Première ligne : hauteur,largeur
        Puis : id,x,y,orientation,length
        ou bien : WALL,x,y
        """
        self.vehicles = []
        self.walls = []

        with open(csv_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            first_line = next(reader)
            self.boardheight, self.boardwidth = int(first_line[0]), int(first_line[1])

            for row in reader:
                if not row:
                    continue
                if row[0].upper() == 'WALL':
                    self.walls.append((int(row[1]), int(row[2])))
                else:
                    vehicle = {
                        "id": row[0],
                        "x": int(row[1]),
                        "y": int(row[2]),
                        "orientation": row[3],
                        "length": int(row[4])
                    }
                    self.vehicles.append(vehicle)

        self.setBoard()

    def setBoard(self):
        """Construit le plateau à partir des véhicules et des murs."""
        board = [[' ' for _ in range(self.boardwidth)] for _ in range(self.boardheight)]

        # murs
        for wall in self.walls:
            x, y = wall
            board[y][x] = '#'

        # véhicules
        for v in self.vehicles:
            for i in range(v["length"]):
                if v["orientation"] == 'H':
                    board[v["y"]][v["x"] + i] = v["id"]
                else:
                    board[v["y"] + i][v["x"]] = v["id"]

        self.board = board

    def isGoal(self):
        """Vérifie si le véhicule rouge X est à la sortie."""
        for v in self.vehicles:
            if v["id"] == "X":
                # Sortie : dernière colonne du plateau
                if v["orientation"] == "H" and v["x"] + v["length"] - 1 == self.boardwidth - 1:
                    return True
        return False

    def successorFunction(self):
        """
        Génère tous les mouvements possibles (action, nouvel état)
        Chaque action = (id, direction)
        direction : 'forward' ou 'backward'
        """
        successors = []

        for v in self.vehicles:
            # copie profonde du plateau
            board_copy = copy.deepcopy(self.board)

            if v["orientation"] == "H":
                # Mouvement vers la droite (forward)
                if v["x"] + v["length"] < self.boardwidth and board_copy[v["y"]][v["x"] + v["length"]] == ' ':
                    new_state = self._moveVehicle(v, dx=1, dy=0)
                    successors.append(((v["id"], "forward"), new_state))

                # Mouvement vers la gauche (backward)
                if v["x"] > 0 and board_copy[v["y"]][v["x"] - 1] == ' ':
                    new_state = self._moveVehicle(v, dx=-1, dy=0)
                    successors.append(((v["id"], "backward"), new_state))

            else:
                # Mouvement vers le bas (forward)
                if v["y"] + v["length"] < self.boardheight and board_copy[v["y"] + v["length"]][v["x"]] == ' ':
                    new_state = self._moveVehicle(v, dx=0, dy=1)
                    successors.append(((v["id"], "forward"), new_state))

                # Mouvement vers le haut (backward)
                if v["y"] > 0 and board_copy[v["y"] - 1][v["x"]] == ' ':
                    new_state = self._moveVehicle(v, dx=0, dy=-1)
                    successors.append(((v["id"], "backward"), new_state))

        return successors

    def _moveVehicle(self, vehicle, dx, dy):
        """Crée un nouvel état après le déplacement d’un véhicule."""
        new_puzzle = RushHourPuzzle(
            boardheight=self.boardheight,
            boardwidth=self.boardwidth,
            vehicles=copy.deepcopy(self.vehicles),
            walls=copy.deepcopy(self.walls)
        )

        # déplace le véhicule sélectionné
        for v in new_puzzle.vehicles:
            if v["id"] == vehicle["id"]:
                v["x"] += dx
                v["y"] += dy
                break

        new_puzzle.setBoard()
        return new_puzzle
    



