import turtle #görsel
import random #rastgele sayı
import numpy as np

GRID_SIZE = 4 #ızgara boyutu
CELL_SIZE = 100 #her ızgara piksel boyutu
FONT = ("Arial", 24, "bold") #yazı tip,boy
SCORE_FONT = ("Arial", 18, "bold") #skor göstergesi
COLORS = {0: "white", 2: "grey", 4: "yellow", 8: "orange", 16: "brown", 
          32: "purple", 64: "red", 128: "green", 256: "ligt blue", 512: "pink", 
          1024: "magenta", 2048: "blue"} #sayı değeri hücre rengi

class Game2048:
    def __init__(self):
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int) #matrisi 0 ile başlat
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = list(zip(*np.where(self.grid == 0)))
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (GRID_SIZE - len(new_row)) # yeni sıranın kalanını 0 ile doldur
        return new_row

    def merge(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0: #yanyana aynıları birleştir
                row[i] *= 2
                self.score += row[i] #birleştirilen hücrenin değerini skora ekle
                row[i + 1] = 0 #hücre boşalt
        return row

    def move(self, direction):
        rotated = False
        if direction in ['up', 'down']:
            self.grid = np.transpose(self.grid)
            rotated = True

        if direction in ['right', 'down']:
            self.grid = np.flip(self.grid, axis=1)

        moved = False
        for i in range(GRID_SIZE):
            original_row = self.grid[i].copy()
            new_row = self.compress(self.merge(self.compress(self.grid[i])))
            self.grid[i] = new_row
            if not np.array_equal(original_row, new_row):
                moved = True

        if direction in ['right', 'down']:
            self.grid = np.flip(self.grid, axis=1)

        if rotated:
            self.grid = np.transpose(self.grid)

        if moved:
            self.add_new_tile()

    def is_game_over(self):
        if np.any(self.grid == 0):
            return False
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def draw(self):
        turtle.clear()
        self.draw_score()
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_tile(i, j, self.grid[i][j])
        turtle.update()

    def draw_score(self):
        turtle.penup()
        turtle.goto(-200, 250) #skorun çizileceği konum
        turtle.pendown()
        turtle.color("red")
        turtle.write(f"Score: {self.score}", align="left", font=SCORE_FONT) #skoru yazdır

    def draw_tile(self, row, col, value):
        x = col * CELL_SIZE - 200
        y = 200 - row * CELL_SIZE
        turtle.penup()
        turtle.goto(x, y)
        turtle.pendown()
        turtle.color("dark blue", COLORS[value]) #hücre rengi
        turtle.begin_fill() #hücre doldur
        for _ in range(4):
            turtle.forward(CELL_SIZE)
            turtle.right(90) #hücre için dört kenar dolaş
        turtle.end_fill()

        if value != 0:
            turtle.penup()
            turtle.goto(x + CELL_SIZE // 2, y - CELL_SIZE // 2)
            turtle.pendown()
            turtle.color("black")
            turtle.write(value, align="center", font=FONT)

def setup():
    turtle.hideturtle()
    turtle.speed(0)
    turtle.tracer(0, 0) #çizimi anında yap
    game.draw()

def on_key_up():
    game.move('up')
    game.draw()
    check_game_over()

def on_key_down():
    game.move('down')
    game.draw()
    check_game_over()

def on_key_left():
    game.move('left')
    game.draw()
    check_game_over()

def on_key_right():
    game.move('right')
    game.draw()
    check_game_over()

def check_game_over():
    if game.is_game_over():
        turtle.penup()
        turtle.goto(0, -50)
        turtle.pendown()
        turtle.color("red")
        turtle.write("Game Over", align="center", font=FONT)
        turtle.update()
        turtle.done()

game = Game2048()
setup()
turtle.listen()
turtle.onkey(on_key_up, "Up")
turtle.onkey(on_key_down, "Down")
turtle.onkey(on_key_left, "Left")
turtle.onkey(on_key_right, "Right")
turtle.mainloop()
