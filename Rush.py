import csv
import copy


class RushHourPuzzle: 
  def __init__(self, board_height, board_widht,vehicles,walls,board):
    self.board_height=board_height
    self.board_widht=board_widht
    self.vehicles=vehicles
    self.walls=walls
    self.board=[]

  def setVehicles(self,csv_file):

      self.vehicles=[]
      self.walls=[]
      with open(csv_file, newline='') as csvfile:
        read=csv.reader(csvfile)
        ligne1=next(read)
        self.board_height,self.board_widht=int(ligne1[0]),int(ligne1[1])

        for i in read:
          if i[0]=='#':
            self.walls.append((int(i[1]),int(i[2])))
          else:
            vehicle={
              "id":i[0],
              "x":int(i[1]),
              "y":int(i[2]),
              "orientation": i[3],
              "length":int(i[4])
            }
            self.vehicles.append(vehicle)

      self.setBoard()


def setBoard(self):
    board = []
    for y in range(self.board_height):
        ligne = []
        for x in range(self.board_width):
            ligne.append(' ')
        board.append(ligne)
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
        if v["id"] == "X":
            if v["orientation"] == "H":
                last_x = v["x"] + v["length"] - 1
                if last_x == self.board_width - 1:
                    return True
    return False




def successorFunction(self):
    successors = []

    for v in self.vehicles:
        vid = v["id"]
        x = v["x"]
        y = v["y"]
        orientation = v["orientation"]
        length = v["length"]

        if orientation == "H":
            #  Déplacement vers la droite 
            if x + length < self.board_width and self.board[y][x + length] == ' ':
                new_state = self._moveVehicle(v, dx=1, dy=0)
                successors.append(((vid, "forward"), new_state))

            # Déplacement vers la gauche 
            if x - 1 >= 0 and self.board[y][x - 1] == ' ':
                new_state = self._moveVehicle(v, dx=-1, dy=0)
                successors.append(((vid, "backward"), new_state))

        elif orientation == "V":
            # Déplacement vers le bas
            if y + length < self.board_height and self.board[y + length][x] == ' ':
                new_state = self._moveVehicle(v, dx=0, dy=1)
                successors.append(((vid, "forward"), new_state))

            # Déplacement vers le haut
            if y - 1 >= 0 and self.board[y - 1][x] == ' ':
                new_state = self._moveVehicle(v, dx=0, dy=-1)
                successors.append(((vid, "backward"), new_state))

    return successors


def _moveVehicle(self, vehicle, dx, dy):
    new_puzzle = RushHourPuzzle(
        board_height=self.board_height,
        board_width=self.board_width,
        vehicles=copy.deepcopy(self.vehicles),
        walls=copy.deepcopy(self.walls)
    )

    # Déplacer le véhicule correspondant
    for v in new_puzzle.vehicles:
        if v["id"] == vehicle["id"]:
            v["x"] += dx
            v["y"] += dy
            break

    new_puzzle.setBoard()
    return new_puzzle


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
    
    def setF(self ,heuristic):
        
        self.f=self.g+heuristic(self.state)
        


