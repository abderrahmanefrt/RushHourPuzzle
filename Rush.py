import csv
import copy
from collections import deque




class RushHourPuzzle: 
    def __init__(self, board_height, board_width, vehicles, walls, board):
        self.board_height = board_height
        self.board_width = board_width
        self.vehicles = vehicles
        self.walls = walls
        self.board = []

    def setVehicles(self, csv_file):
        self.vehicles = []
        self.walls = []
        with open(csv_file, newline='') as csvfile:
            read = csv.reader(csvfile)
            ligne1 = next(read)
            self.board_height, self.board_width = int(ligne1[0]), int(ligne1[1])

            for i in read:
                if i[0] == '#':
                    self.walls.append((int(i[1]), int(i[2])))
                else:
                    vehicle = {
                        "id": i[0],
                        "x": int(i[1]),
                        "y": int(i[2]),
                        "orientation": i[3],
                        "length": int(i[4])
                    }
                    self.vehicles.append(vehicle)
        self.setBoard()

    def setBoard(self):
        board = [[' ' for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.board = board

        for x, y in self.walls:
            self.board[y][x] = '#'

        for v in self.vehicles:
            vid = v["id"]
            x = v["x"]
            y = v["y"]
            orientation = v["orientation"]
            length = v["length"]
            for i in range(length):
                if orientation == "H":
                    self.board[y][x + i] = vid
                else:
                    self.board[y + i][x] = vid

    def isGoal(self):
        for v in self.vehicles:
            if v["id"] == "X" and v["orientation"] == "H":
                last_x = v["x"] + v["length"] - 1
                if last_x == self.board_width - 1:
                    return True
        return False

    def successorFunction(self):
        successors = []
        for v in self.vehicles:
            vid = v["id"]
            x, y = v["x"], v["y"]
            orientation, length = v["orientation"], v["length"]

            if orientation == "H":
                if x + length < self.board_width and self.board[y][x + length] == ' ':
                    new_state = self._moveVehicle(v, dx=1, dy=0)
                    successors.append(((vid, "forward"), new_state))
                if x - 1 >= 0 and self.board[y][x - 1] == ' ':
                    new_state = self._moveVehicle(v, dx=-1, dy=0)
                    successors.append(((vid, "backward"), new_state))

            elif orientation == "V":
                if y + length < self.board_height and self.board[y + length][x] == ' ':
                    new_state = self._moveVehicle(v, dx=0, dy=1)
                    successors.append(((vid, "forward"), new_state))
                if y - 1 >= 0 and self.board[y - 1][x] == ' ':
                    new_state = self._moveVehicle(v, dx=0, dy=-1)
                    successors.append(((vid, "backward"), new_state))

        return successors

    def _moveVehicle(self, vehicle, dx, dy):
        new_puzzle = RushHourPuzzle(
            board_height=self.board_height,
            board_width=self.board_width,
            vehicles=copy.deepcopy(self.vehicles),
            walls=copy.deepcopy(self.walls),
            board=[]
        )
        for v in new_puzzle.vehicles:
            if v["id"] == vehicle["id"]:
                v["x"] += dx
                v["y"] += dy
                break
        new_puzzle.setBoard()
        return new_puzzle

    def showBoard(self):
        for row in self.board:
            print(" ".join(row))
        print("-" * (2 * self.board_width - 1))

class Node:
    def __init__(self,state,parent=None,action=None, g=0,f=0):
        self.state=state
        self.parent=parent
        self.action=action
        self.g=g
        self.f=f

    def getPath(self):
        path=[]
        node=self
        while node is not None:
            path.append(node.state)
            node=node.parent
        path.reverse()

        return path
    
    def getSolution(self):
        actions=[]
        node=self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions
    
  
        


class Search:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def BFS(self):
        # 1. Créer le nœud initial
        init_node = Node(self.initial_state, None, None)

        # Si déjà à l'état but
        if self.initial_state.isGoal():
            return init_node.getSolution()

        # 2. Initialiser les structures
        open_list = deque([init_node])
        closed_list = []

        # 3. Boucle principale
        while open_list:
            current = open_list.popleft()  # retirer le premier élément (FIFO)
            closed_list.append(current)

            # 4. Générer les successeurs
            for (action, state) in current.state.successorFunction():
                child = Node(state, current, action)

                # Vérifier si le but est atteint
                if child.state.isGoal():
                    print("✅ Solution trouvée !")
                    return child.getSolution()

                # Vérifier si déjà visité
                if not self._in_list(child, open_list) and not self._in_list(child, closed_list):
                    open_list.append(child)

        print("❌ Aucune solution trouvée.")
        return None

    def _in_list(self, node, node_list):
        """Vérifie si un état identique existe déjà dans une liste de nœuds."""
        for n in node_list:
            if self._same_state(n.state, node.state):
                return True
        return False

    def _same_state(self, s1, s2):
        """Compare deux états du puzzle (positions des véhicules)."""
        for v1, v2 in zip(s1.vehicles, s2.vehicles):
            if v1["id"] != v2["id"] or v1["x"] != v2["x"] or v1["y"] != v2["y"]:
                return False
        return True
