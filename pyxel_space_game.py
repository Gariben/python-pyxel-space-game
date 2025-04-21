import pyxel


GAME_TITLE = "Pyxel Space Game"
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
HEIGHT_MARGIN = 20
WIDTH_MARGIN = 10

DEBUG = 0

SCENE_TTILE = 0
SCENE_PLAY = 1

class Border:
    def __init__(self,color):
        self.color = color

    def draw(self):
        pyxel.rect(0, 0, SCREEN_WIDTH, HEIGHT_MARGIN, self.color)
        pyxel.rect(0, SCREEN_HEIGHT-HEIGHT_MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, self.color)

class Ship:
    def __init__(self, coords, vel, color):
        self.coords = coords
        self.up_count = 0
        self.coins = 0
        self.vel = vel
        self.color = color
        self.height = 10
        self.width = 10

    def update(self):

        self.coords[0] += self.vel[0]
        if pyxel.btn(pyxel.KEY_W):  # Move up
            self.coords[1] -= self.vel[1]
            self.up_count +=1
        elif pyxel.btn(pyxel.KEY_S):  # Move down
            self.coords[1] += self.vel[1]
        else:
            if self.up_count>0: self.up_count -=2


    def draw(self):
        #if pyxel.btn(pyxel.KEY_W):  # Move up
        #    pyxel.rect(WIDTH_MARGIN, (SCREEN_HEIGHT//2)+(self.height//4), self.width, self.height//2, pyxel.COLOR_GREEN)
        #if pyxel.btn(pyxel.KEY_S):  # Move down
        #    pyxel.rect(WIDTH_MARGIN, (SCREEN_HEIGHT//2)+(self.height//4), self.width, self.height//2, pyxel.COLOR_GREEN)
        #else:
            pyxel.rect(WIDTH_MARGIN, SCREEN_HEIGHT//2, self.width, self.height, self.color)


class Star:
    def __init__(self, coords, vel, color):
        self.coords = coords
        self.vel = vel
        self.color = color

    def update(self, ship):
        
        self.coords[0] -= (ship.vel[0]*2)

        if pyxel.btn(pyxel.KEY_W):
            self.coords[1] += ship.vel[1]
        if pyxel.btn(pyxel.KEY_S):
            self.coords[1] -= ship.vel[1]

        if self.coords[0] < 0: 
            self.coords[0] = SCREEN_WIDTH
            self.coords[1] = pyxel.rndi(0, SCREEN_HEIGHT-HEIGHT_MARGIN)
        
        if self.coords[1] < HEIGHT_MARGIN: self.coords[1] = SCREEN_HEIGHT - HEIGHT_MARGIN
        if self.coords[1] > SCREEN_HEIGHT - HEIGHT_MARGIN: self.coords[1] = HEIGHT_MARGIN

    def draw(self):
        pyxel.pset(self.coords[0], self.coords[1], self.color)


#------------------------------------------------------------------------------
# Main Application
#------------------------------------------------------------------------------

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=GAME_TITLE)
        self.ship = Ship([0+WIDTH_MARGIN, SCREEN_HEIGHT // 2], [1,1],pyxel.COLOR_RED)
        self.stars = [
            Star(
                coords=[pyxel.rndi(0, SCREEN_WIDTH), pyxel.rndi(0, SCREEN_HEIGHT-HEIGHT_MARGIN)],
                vel=[-pyxel.rndi(1, self.ship.vel[0]), 0],
                color=pyxel.COLOR_WHITE,
            )
            for _ in range(50)  # Create 50 stars
        ]
        self.border = Border(pyxel.COLOR_BLACK)
        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        for star in self.stars:
            star.update(self.ship)
        self.ship.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, pyxel.COLOR_DARK_BLUE)
        for star in self.stars:
            star.draw()
        self.ship.draw()
        self.border.draw()
        if DEBUG and (pyxel.btn(pyxel.KEY_W) or self.ship.up_count): pyxel.text(0, 0, "W"+str(self.ship.up_count), pyxel.COLOR_WHITE)
        if DEBUG and pyxel.btn(pyxel.KEY_S): pyxel.text(0, 6, "S", pyxel.COLOR_WHITE)
        if DEBUG: pyxel.text(WIDTH_MARGIN, HEIGHT_MARGIN-11, "Xvel:"+str(self.ship.vel[0])+"X:"+str(self.ship.coords[0]), pyxel.COLOR_WHITE)
        if DEBUG: pyxel.text(WIDTH_MARGIN, HEIGHT_MARGIN-5, "Yvel:"+str(self.ship.vel[1])+"Y:"+str(self.ship.coords[1]), pyxel.COLOR_WHITE)
        #rect(x, y, w, h, col)
        #pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)


App()