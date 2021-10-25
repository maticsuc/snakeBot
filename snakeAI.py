import collections
from PIL import ImageGrab
import keyboard

# TO-DO

class SnakeAI:

    headIndex = (4,7)
    boardWidth = 17
    boardHeight = 15
    squareSize = 32
    squareCenterPixel = ((squareSize - 1) // 2, (squareSize - 1) // 2)
    boardBBox = (680, 367, 680 + squareSize * boardWidth, 367 + squareSize * boardHeight)
    applePixel = (231, 71, 29)
    startingDirection = 'right'

    checkingPixelMargin = 12
    checkingPixelLeft = ((squareSize - 1) - checkingPixelMargin, (squareSize - 1) // 2)
    checkingPixelRight = (checkingPixelMargin, (squareSize - 1) // 2)
    checkingPixelUp = ((squareSize - 1) // 2, (squareSize - 1) - checkingPixelMargin)
    checkingPixelDown = ((squareSize - 1) // 2, checkingPixelMargin)

    backgroundColorLight = (87, 138, 52)
    backgroundColorDark = (74, 117, 44)

    def __init__(self):
        self.reset()

    def findPlayingBoardOnMonitor(self):
        maxMonitorHeight = 2000
        startingY = 100
        marginY = 100

        indexY = indexX = None

        for y in range(startingY, maxMonitorHeight, marginY):
            stripe = ImageGrab.grab(bbox=(0, y, 2000, y + 1))
            try:
                indexX = list(stripe.getdata()).index(SnakeAI.backgroundColorLight)
                break
            except ValueError:
                pass
        try:
            stripe = ImageGrab.grab(bbox=(indexX, 0, indexX + 1, 2000))
            indexY = list(stripe.getdata()).index(SnakeAI.backgroundColorDark)
        except:
            return False
        
        self.boardX = indexX + 28
        self.boardY = indexY + 95
        self.boardBBox = (self.boardX, self.boardY, self.boardX + self.squareSize * self.boardWidth, self.boardY + self.squareSize * self.boardHeight)

        return True

    def reset(self):
        x, y = SnakeAI.headIndex
        self.head = (x,y)
        self.body = [self.head, (x - 1, y), (x - 2, y), (x - 3, y)]
        self.direction = None
        self.apple = None
        self.eatenApple = False
        self.frame_iteration = 0
        self.score = 0

    def play_step(self, action):
        
        self.frame_iteration += 1
        game_over = False
        reward = 0

        # Move
        self.move(action)

        # Check if game over
        if self.collision() or self.frame_iteration > 100*len(self.body):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Check if SnakeAI has eaten apple
        if self.head == self.apple:
            self.score += 1
            reward = 10
            self.findApple()
        else:
            self.body.pop()

        return reward, game_over, self.score
            

    def move(self, action):
        # [straight, right, left]
        clock_wise = ['right', 'down', 'left', 'up']

        idx = clock_wise.index(self.direction)

        if action == [1, 0, 0]:
            new_dir = clock_wise[idx]

        elif action == [0, 1, 0]:
            next_idx = (idx + 1) % len(clock_wise)
            new_dir = clock_wise[next_idx]
        
        else:
            next_idx = (idx - 1) % len(clock_wise)
            new_dir = clock_wise[next_idx]
        
        self.direction = new_dir

        keyboard.press_and_release(self.direction)

        x, y = self.head

        if self.direction == 'down':
            y += 1
            checkingPixel = SnakeAI.checkingPixelDown
        elif self.direction == 'up':
            y -= 1
            checkingPixel = SnakeAI.checkingPixelUp
        elif self.direction == 'right':
            x += 1
            checkingPixel = SnakeAI.checkingPixelRight
        elif self.direction == 'left':
            x -= 1     
            checkingPixel = SnakeAI.checkingPixelLeft

        squareX = x * SnakeAI.squareSize
        squareY = y * SnakeAI.squareSize

        c = 0
        while True:
            self.board = ImageGrab.grab(bbox=self.boardBBox)
            square = self.board.crop((squareX, squareY, squareX + SnakeAI.squareSize, squareY + SnakeAI.squareSize))
            centerpixel = square.getpixel(checkingPixel)
            if centerpixel[2] >= 150:
                self.head = (x,y)
                return True
            elif c > 5:
                return False
            c += 1       

    def collision(self, pt=None):
        if pt is None:
            pt = self.head
        
        # Hits boundary
        if pt.x > (SnakeAI.boardWidth - 1) or pt.x < 0 or pt.y < 0 or pt.y > (SnakeAI.boardHeight - 1):
            return True
        
        if pt in self.body[1:]:
            return True

        return False


    def findApple(self):
        self.board = ImageGrab.grab(bbox=SnakeAI.boardBBox)
        for x in range(SnakeAI.boardWidth):
            for y in range(SnakeAI.boardHeight):
                squareX = x * SnakeAI.squareSize
                squareY = y * SnakeAI.squareSize
                square = self.board.crop((squareX, squareY, squareX + SnakeAI.squareSize, squareY + SnakeAI.squareSize))
                centerpixel = square.getpixel(SnakeAI.squareCenterPixel)
                if centerpixel == SnakeAI.applePixel:
                    self.apple = (x,y)
                    return
        self.apple = None