import csv


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

   successor=[]
   
   
   




