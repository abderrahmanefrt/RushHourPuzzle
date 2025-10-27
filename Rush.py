import csv
import copy
from collections import deque
import time



class RushHourPuzzle:
    def __init__(self, board_height, board_width, vehicles, walls, board):
        self.board_height = board_height
        self.board_width = board_width
        self.vehicles = vehicles
        self.walls = walls
        self.board = []

    def setVehicles(self, csv_file):
        """Charge les véhicules et les murs depuis un fichier CSV."""
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
        """Construit le plateau à partir des véhicules et murs."""
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
        """Vérifie si le véhicule rouge (X) est à la sortie."""
        for v in self.vehicles:
            if v["id"] == "X" and v["orientation"] == "H":
                last_x = v["x"] + v["length"] - 1
                if last_x == self.board_width - 1:
                    return True
        return False

    def successorFunction(self):
        """Génère tous les états successeurs possibles."""
        successors = []
        for v in self.vehicles:
            vid = v["id"]
            x, y = v["x"], v["y"]
            orientation, length = v["orientation"], v["length"]

            if orientation == "H":
                if x + length < self.board_width and self.board[y][x + length] == ' ':
                    new_state = self._deplacementVehicle(v, dx=1, dy=0)
                    successors.append(((vid, "forward"), new_state))
                if x - 1 >= 0 and self.board[y][x - 1] == ' ':
                    new_state = self._deplacementVehicle(v, dx=-1, dy=0)
                    successors.append(((vid, "backward"), new_state))

            elif orientation == "V":
                if y + length < self.board_height and self.board[y + length][x] == ' ':
                    new_state = self._deplacementVehicle(v, dx=0, dy=1)
                    successors.append(((vid, "forward"), new_state))
                if y - 1 >= 0 and self.board[y - 1][x] == ' ':
                    new_state = self._deplacementVehicle(v, dx=0, dy=-1)
                    successors.append(((vid, "backward"), new_state))

        return successors

    def _deplacementVehicle(self, vehicle, dx, dy):
        """Retourne un nouvel état après déplacement d’un véhicule."""
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
        """Affiche le plateau dans la console."""
        for row in self.board:
            print(" ".join(row))
        print("-" * (2 * self.board_width - 1))



class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = 0 if parent is None else parent.g + 1
        self.f = 0

    def getPath(self):
        path = []
        node = self
        while node is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def getSolution(self):
        actions = []
        node = self
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions

    def setF(self, h_value):
        self.f = self.g + h_value

    def __lt__(self, other):
        return self.f < other.f



class Search:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def BFS(self):
        start_time = time.time()
        counter = 0

        init_node = Node(self.initial_state, None, None)

        if self.initial_state.isGoal():
            print("Temps  : {:.4f} secondes".format(time.time() - start_time))
            print("Nombre d'étapes explorées : 0")
            return init_node.getSolution()

        open = deque([init_node])
        closed = []

        while open:
            current = open.popleft()
            closed.append(current)
            counter += 1

            for (action, state) in current.state.successorFunction():
                child = Node(state, current, action)

                if child.state.isGoal():
                    timex = time.time() - start_time
                    print(f" Nombre d'étapes explorées : {counter}")
                    print(f" Temps d'exécution : {timex:.4f} secondes\n")
                    return child.getSolution()

                if not self._identique(child, open) and not self._identique(child, closed):
                    open.append(child)

        timex = time.time() - start_time
        print("\nAucune solution trouvée.")
        print(f" Nombre d'étapes explorées : {counter}")
        print(f" Temps d'exécution : {timex:.4f} secondes\n")
        return None

    #A* 
    def AStar(self, heuristic="h1"):
        start_time = time.time()
        counter = 0

        init_node = Node(self.initial_state)
        init_node.g = 0
        init_node.f = self._heuristic(init_node.state, heuristic)

        open_list = [init_node]
        closed_list = []

        while open_list:
            current = min(open_list, key=lambda node: node.f)
            open_list.remove(current)
            counter += 1

            if current.state.isGoal():
                timex = time.time() - start_time
                print(f" A* ({heuristic}) : solution trouvée en {timex:.4f}s, {counter} étapes explorées")
                return current.getSolution()

            closed_list.append(current)

            for (action, successor) in current.state.successorFunction():
                child = Node(successor, current, action)
                child.g = current.g + self._cost(current, action, successor)
                child.f = child.g + self._heuristic(successor, heuristic)

                open2 = self._existe(open_list, child)
                closed2 = self._existe(closed_list, child)

                if not open2 and not closed2:
                    open_list.append(child)
                elif open2 and child.f < open2.f:
                    open_list.remove(open2)
                    open_list.append(child)
                elif closed2 and child.f < closed2.f:
                    closed_list.remove(closed2)
                    open_list.append(child)

        print(f" Aucune solution trouvée avec A* ({heuristic}) après {counter} étapes")
        return None

    def _heuristic(self, state, type="h1"):
     xcar = next(v for v in state.vehicles if v["id"] == "X")

     distance = (state.board_width - 1) - (xcar["x"] + xcar["length"] - 1)

     if type == "h1":
        return distance

    
     elif type == "h2":
        blockers = 0
        y = xcar["y"]
        for x in range(xcar["x"] + xcar["length"], state.board_width):
            if state.board[y][x] != ' ':
                blockers += 1
        return distance + blockers

     elif type == "h3":
        blockers = 0
        y = xcar["y"]
        for x in range(xcar["x"] + xcar["length"], state.board_width):
            if state.board[y][x] != ' ':
                for v in state.vehicles:
                    if v["id"] == state.board[y][x]:
                        blockers += v["length"]  
                        break
        return distance + blockers

     return 0


    def _cost(self, current, action, successor):
        return 1  

    def _identique(self, node, node_list):
        for n in node_list:
            if isinstance(n, tuple):
                n = n[2]
            if self._same_state(n.state, node.state):
                return True
        return False

    def _existe(self, lst, node):
        for item in lst:
            n = item[2] if isinstance(item, tuple) else item
            if self._same_state(n.state, node.state):
                return n
        return None

    def _same_state(self, s1, s2):
        for v1, v2 in zip(s1.vehicles, s2.vehicles):
            if v1["id"] != v2["id"] or v1["x"] != v2["x"] or v1["y"] != v2["y"]:
                return False
        return True



if __name__ == "__main__":
    puzzle = RushHourPuzzle(0, 0, [], [], [])
    puzzle.setVehicles("e-f.csv")

    search = Search(puzzle)

    print("\n BFS ")
    bfs_solution = search.BFS()

    print("\n A* avec h1 ")
    a1_solution = search.AStar("h1")

    print("\n A* avec h2 ")
    a2_solution = search.AStar("h2")

    print("\n  A* avec h3 ")
    a3_solution = search.AStar("h3")
