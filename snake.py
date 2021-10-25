from PIL import ImageGrab
import keyboard

# PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)

class Snake:

    # 680, 367
    # 1000, 547
    boardX = 680
    boardY = 367
    
    headIndex = (4,7)
    boardWidth = 17
    boardHeight = 15
    squareSize = 32
    squareCenterPixel = ((squareSize - 1) // 2, (squareSize - 1) // 2)
    boardBBox = (boardX, boardY, boardX + squareSize * boardWidth, boardY + squareSize * boardHeight)
    applePixel = (231, 71, 29)
    startingDirection = 'right'

    checkingPixelMargin = 10
    checkingPixelLeft = ((squareSize - 1) - checkingPixelMargin, (squareSize - 1) // 2)
    checkingPixelRight = (checkingPixelMargin, (squareSize - 1) // 2)
    checkingPixelUp = ((squareSize - 1) // 2, (squareSize - 1) - checkingPixelMargin)
    checkingPixelDown = ((squareSize - 1) // 2, checkingPixelMargin)

    backgroundColor = (87, 138, 52)
    backgroundColor2 = (74, 117, 44)

    def __init__(self):
        x, y = Snake.headIndex
        self.head = (x,y)
        self.body = [self.head, (x - 1, y), (x - 2, y), (x - 3, y)]
        self.direction = None
        self.apple = None
        self.eatenApple = False

    def startGame(self):
        self.findPlayingBoardOnMonitor()
        keyboard.press_and_release(Snake.startingDirection)
        self.direction = Snake.startingDirection
        self.findApple()

    def update(self, head=None, direction=None):
        if head is not None:
            self.head = head
            self.body.insert(0, head)
            if not self.eatenApple:
                self.body.pop()
            self.eatenApple = False
        if direction is not None:
            self.direction = direction

    def move(self, newDirection):
        if newDirection != self.direction:
            self.checkSquare()
            keyboard.press_and_release(newDirection)
            self.update(direction=newDirection)

    def findApple(self):
        self.board = ImageGrab.grab(bbox=Snake.boardBBox)
        for x in range(Snake.boardWidth):
            for y in range(Snake.boardHeight):
                squareX = x * Snake.squareSize
                squareY = y * Snake.squareSize
                square = self.board.crop((squareX, squareY, squareX + Snake.squareSize, squareY + Snake.squareSize))
                centerpixel = square.getpixel(Snake.squareCenterPixel)
                if centerpixel == Snake.applePixel:
                    self.apple = (x,y)
                    return
        self.apple = None
    
    def playGame(self):
        while True:
            if self.head == self.apple:
                self.eatenApple = True
                self.findApple()
            
            if self.apple == None:
                self.findApple()

            self.checkNextSquare()

    def findPlayingBoardOnMonitor(self):
        indexY = None
        for y in range(100, 2000, 100):
            neki = ImageGrab.grab(bbox=(0, y, 2000,y + 1))
            try:
                indexX = list(neki.getdata()).index(Snake.backgroundColor)
                break
            except ValueError:
                pass
        
        neki = ImageGrab.grab(bbox=(indexX, 0, indexX + 1, 2000))
        indexY = list(neki.getdata()).index(Snake.backgroundColor2)
        neki = ImageGrab.grab(bbox=(indexX, indexY, indexX + 100, indexY + 100))

        Snake.boardX = indexX + 28
        Snake.boardY = indexY + 95

        Snake.boardBBox = (Snake.boardX, Snake.boardY, Snake.boardX + Snake.squareSize * Snake.boardWidth, Snake.boardY + Snake.squareSize * Snake.boardHeight)


    def checkSquare(self):
        
        x, y = self.head

        if self.direction == 'down':
            y += 1
            checkingPixel = Snake.checkingPixelDown
        elif self.direction == 'up':
            y -= 1
            checkingPixel = Snake.checkingPixelUp
        elif self.direction == 'right':
            x += 1
            checkingPixel = Snake.checkingPixelRight
        elif self.direction == 'left':
            x -= 1     
            checkingPixel = Snake.checkingPixelLeft

        squareX = x * Snake.squareSize
        squareY = y * Snake.squareSize

        c = 0
        while True:
            self.board = ImageGrab.grab(bbox=Snake.boardBBox)
            square = self.board.crop((squareX, squareY, squareX + Snake.squareSize, squareY + Snake.squareSize))
            centerpixel = square.getpixel(checkingPixel)
            if centerpixel[2] >= 150:
                self.update(head=(x,y))
                return True
            elif c > 5:
                return False
            c += 1
    
    def checkNextSquare(self):
        
        x, y = self.head
        
        if self.direction == 'right':
            if (x + 1) == (Snake.boardWidth - 1):
                if y == 0 or y < self.apple[1]:
                    self.move('down')
                else:
                    self.move('up')
            else:
                self.checkSquare()
        
        elif self.direction == 'down':
            if (y + 1) == (Snake.boardHeight - 1) or (y + 1) == self.apple[1]:
                if x == 0 or x < self.apple[0]:
                    self.move('right')
                else:
                    self.move('left')
            else:
                self.checkSquare()
        
        elif self.direction == 'left':
            if (x - 1) == 0:
                if y == 0 or y < self.apple[1]:
                    self.move('down')
                else:
                    self.move('up')
            else:
                self.checkSquare()
        
        elif self.direction == 'up':
            if (y - 1) == 0 or (y - 1) == self.apple[1]:
                if x == 0 or x < self.apple[0]:
                    self.move('right')
                else:
                    self.move('left')
            else:
                self.checkSquare()