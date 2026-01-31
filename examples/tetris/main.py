import love

from tetris.game import TetrisGame


_game = TetrisGame()


def love_conf(t):
    t["window"]["title"] = "Tetris (Python)"
    t["window"]["width"] = 640
    t["window"]["height"] = 720
    t["window"]["resizable"] = False
    t["window"]["vsync"] = True


def love_load():
    _game.reset()


def love_update(dt):
    _game.update(dt)


def love_draw():
    _game.draw()


def love_keypressed(key, scancode, isrepeat):
    _game.keypressed(key, scancode, isrepeat)


def love_keyreleased(key, scancode):
    _game.keyreleased(key, scancode)

