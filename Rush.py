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
        start_time = time.time()  
        counter = 0

        init_node = Node(self.initial_state, None, None)

        if self.initial_state.isGoal():
            print("Temps écoulé : {:.4f} secondes".format(time.time() - start_time))
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

    def _identique(self, node, node_list):
        for n in node_list:
            if self._same_state(n.state, node.state):
                return True
        return False

    def _same_state(self, s1, s2):
        for v1, v2 in zip(s1.vehicles, s2.vehicles):
            if v1["id"] != v2["id"] or v1["x"] != v2["x"] or v1["y"] != v2["y"]:
                return False
        return True








if __name__ == "__main__":
    puzzle = RushHourPuzzle(0, 0, [], [], [])
    puzzle.setVehicles("1.csv")  

    search = Search(puzzle)
    solution = search.BFS()

    if solution:
        print("solution:")
        for step in solution:
            print(step)
    else:
        print("Pas de solution ")
