import pyxel


GAME_TITLE = "Pyxel Space Game"
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 240
HEIGHT_MARGIN = 20
WIDTH_MARGIN = 10

SHIP_SPEED=3

class Border:
    def __init__(self,color):
        self.color = color

    def draw(self):
        pyxel.rect(0, 0, SCREEN_WIDTH, HEIGHT_MARGIN, self.color)
        pyxel.rect(0, SCREEN_HEIGHT-HEIGHT_MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT, self.color)

class Ship:
    def __init__(self, coords, vel, color):
        self.coords = coords
        self.vel = vel
        self.color = color
        self.height = 10
        self.width = 10

    def update(self):
        if ((self.coords[1]-1) > HEIGHT_MARGIN) and pyxel.btn(pyxel.KEY_W):  # Move up
            self.coords[1] -= SHIP_SPEED
        if ((self.coords[1]+self.height+1) < SCREEN_HEIGHT-HEIGHT_MARGIN) and pyxel.btn(pyxel.KEY_S):  # Move down
            self.coords[1] += SHIP_SPEED


    def draw(self):
        pyxel.rect(self.coords[0], self.coords[1], self.width, self.height, self.color)


class Star:
    def __init__(self, coords, vel, color):
        self.coords = coords
        self.vel = vel
        self.color = color

    def update(self, ship):
        
        self.coords[0] += self.vel[0]
        self.coords[1] += self.vel[1]

        if ((ship.coords[1]-1) > HEIGHT_MARGIN) and pyxel.btn(pyxel.KEY_W):
            self.coords[1] -= SHIP_SPEED//2
        if ((ship.coords[1]+ship.height+1) < SCREEN_HEIGHT-HEIGHT_MARGIN) and pyxel.btn(pyxel.KEY_S):  # Move up
            self.coords[1] += SHIP_SPEED//2

        if self.coords[0] < 0: 
            self.coords[0] = SCREEN_WIDTH
            self.coords[1] = pyxel.rndi(0, SCREEN_HEIGHT-HEIGHT_MARGIN)
        
        if self.coords[1] < HEIGHT_MARGIN: self.coords[1] = SCREEN_HEIGHT - HEIGHT_MARGIN
        if self.coords[1] > SCREEN_HEIGHT - HEIGHT_MARGIN: self.coords[1] = HEIGHT_MARGIN

    def draw(self):
        pyxel.pset(self.coords[0], self.coords[1], self.color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=GAME_TITLE)
        self.ship = Ship([0+WIDTH_MARGIN, SCREEN_HEIGHT // 2], [0, 0],pyxel.COLOR_RED)
        self.stars = [
            Star(
                coords=[pyxel.rndi(0, SCREEN_WIDTH), pyxel.rndi(0, SCREEN_HEIGHT-HEIGHT_MARGIN)],
                vel=[-pyxel.rndi(1, SHIP_SPEED), 0],
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
        #rect(x, y, w, h, col)
        #pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)


App()