import random

TITLE = "Pac-Man"

# init environment
BLOCK_SIZE = 32
WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE * BLOCK_SIZE
HEIGHT = WORLD_SIZE * BLOCK_SIZE
SPEED = 2
GHOST_SPEED = 1

# declare world
world = []


def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)


char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
}

# define world


def draw():
    screen.clear()
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block],
                            (x * BLOCK_SIZE, y * BLOCK_SIZE))


load_level(1)
print(world)


# define pacman
pacman = Actor("pacman_o.png", anchor=("left", "top"))
pacman.x = pacman.y = 1 * BLOCK_SIZE


def draw():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block],
                            (x * BLOCK_SIZE, y * BLOCK_SIZE))
    pacman.draw()


# define move
def on_key_down(key):
    if key == keys.LEFT:
        pacman.x += -BLOCK_SIZE
    if key == keys.RIGHT:
        pacman.x += BLOCK_SIZE
    if key == keys.UP:
        pacman.y += -BLOCK_SIZE
    if key == keys.DOWN:
        pacman.y += BLOCK_SIZE


def on_key_down(key):
    if key == keys.LEFT:
        pacman.dx = -1
    if key == keys.RIGHT:
        pacman.dx = 1
    if key == keys.UP:
        pacman.dy = -1
    if key == keys.DOWN:
        pacman.dy = 1


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


# Direction that we're going in
pacman.dx, pacman.dy = 0, 0


def update():
    pacman.x += pacman.dx
    pacman.y += pacman.dy


# collision detection
def blocks_ahead_of_pacman(dx, dy):
    """Return a list of tiles at this position + (dx,dy)"""

    # Here's where we want to move to
    x = pacman.x + dx
    y = pacman.y + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix + 1])
    if ry:
        blocks.append(world[iy + 1][ix])
    if rx and ry:
        blocks.append(world[iy + 1][ix + 1])

    return blocks


def update():
    # To go in direction (dx, dy) check for no walls
    if "=" not in blocks_ahead_of_pacman(pacman.dx, 0):
        pacman.x += pacman.dx
    if "=" not in blocks_ahead_of_pacman(0, pacman.dy):
        pacman.y += pacman.dy


# adding a ghost
char_to_image = {
    ".": "dot.png",
    "=": "wall.png",
    "*": "power.png",
    "g": "ghost1.png",
    "G": "ghost2.png",
}

ghosts = []


def make_ghost_actors():
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            if block == "g" or block == "G":
                g = Actor(
                    char_to_image[block],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE),
                    anchor=("left", "top"),
                )
                ghosts.append(g)
                # Now we have the ghost sprite we don't need this block
                world[y][x] = None
                make_ghost_actors()
