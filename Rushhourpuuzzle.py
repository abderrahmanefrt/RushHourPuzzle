

class  RushHourPuzzle :
    def __init__(self, boardheight, boardwidth, vehicles, walls=None):
        self.boardheight = boardheight
        self.boardwidth = boardwidth
        self.vehicles = vehicles  
        self.walls = walls if walls else []
        self.board = self.setBoard()
   
