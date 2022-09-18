import random
import time

WORLD_SIZE = 20
BLOCK_SIZE = 32
WIDTH = WORLD_SIZE*BLOCK_SIZE
HEIGHT = WORLD_SIZE*BLOCK_SIZE

SPEED = 2


# An array containing the world tiles
world = []

# Our sprites
pacman = Actor('pacman_o.png', anchor=('left', 'top'))
marker = Actor('marker.png', anchor=('left', 'top'))
pacman.x = pacman.y = 1*BLOCK_SIZE
marker.x = marker.y = 1*BLOCK_SIZE

# Direction that we're going in
pacman.dx, pacman.dy = 0, 0
marker.dx, marker.dy = 0, 0

# Your level will contain characters, they map
# to the following images
char_to_image = {
    '.': 'dot.png',
    '=': 'wall.png',
}


def load_level(number):
    file = "level-%s.txt" % number
    with open(file) as f:
        for line in f:
            row = []
            for block in line:
                row.append(block)
            world.append(row)


def set_random_dir(sprite, speed):
    sprite.dx = random.choice([-speed, speed])
    sprite.dy = random.choice([-speed, speed])


def draw():
    screen.clear()
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pacman.draw()
    marker.draw()


def blocks_ahead_of(sprite, dx, dy):
    """Return a list of tiles at this position + delta"""

    # Here's where we want to move to
    x = sprite.x + dx
    y = sprite.y + dy

    # Find integer block pos, using floor (so 4.7 becomes 4)
    ix, iy = int(x // BLOCK_SIZE), int(y // BLOCK_SIZE)
    # Remainder let's us check adjacent blocks
    rx, ry = x % BLOCK_SIZE, y % BLOCK_SIZE
    # Keep in bounds of world
    if ix == WORLD_SIZE-1:
        rx = 0
    if iy == WORLD_SIZE-1:
        ry = 0

    blocks = [world[iy][ix]]
    if rx:
        blocks.append(world[iy][ix+1])
    if ry:
        blocks.append(world[iy+1][ix])
    if rx and ry:
        blocks.append(world[iy+1][ix+1])

    return blocks


def wrap_around(mini, val, maxi):
    if val < mini:
        return maxi
    elif val > maxi:
        return mini
    else:
        return val


def move_ahead(sprite):
    # Record current pos so we can see if the sprite moved
    oldx, oldy = sprite.x, sprite.y
    # print(blocks_ahead_of(sprite, sprite.dx, 0))
    # In order to go in direction dx, dy there must be no wall that way
    if '=' not in blocks_ahead_of(sprite, sprite.dx, 0):
        sprite.x += sprite.dx
    if '=' not in blocks_ahead_of(sprite, 0, sprite.dy):
        sprite.y += sprite.dy

    # Keep sprite on the screen
    sprite.x = wrap_around(0, sprite.x, WIDTH-BLOCK_SIZE)
    sprite.y = wrap_around(0, sprite.y, HEIGHT-BLOCK_SIZE)

    # Return whether we moved
    return oldx != sprite.x or oldy != sprite.y


# a = [
#     [32, 32], [64, 32], [96, 32], [128, 32],
#     [160, 32], [192, 32], [0, ]
# ]

a2 = []
now = [32, 32]


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None


head = Node([32, 32])


def isInLinkedList(data):
    current2 = head

    while current2 is not None:
        if current2.data == data:
            return False

        current2 = current2.next

    return True


def bfs(coordinate):

    now = 1

    # print(world[64//32][96//32], "========================================")

    while True:

        counter = 1
        current = head
        currentNode = head

        while counter != now:
            currentNode = currentNode.next
            counter += 1

        while current.next is not None:
            current = current.next

        north = [currentNode.data[0]-32, currentNode.data[1]]

        east = [currentNode.data[0], currentNode.data[1]+32]

        south = [currentNode.data[0]+32, currentNode.data[1]]

        west = [currentNode.data[0], currentNode.data[1]-32]

        if(world[north[0]//32][north[1]//32] != '=' and isInLinkedList(north) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(north)
            newNode.prev = currentNode
            current.next = newNode

        if(north == coordinate):
            # print(north)
            print("DAPETT n")
            break

        if(world[east[0]//32][east[1]//32] != '=' and isInLinkedList(east) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(east)
            current.next = newNode
            current.next.prev = currentNode

        if(east == coordinate):
            # print(east)
            print("DAPETT e")
            break

        if(world[south[0]//32][south[1]//32] != '=' and isInLinkedList(south) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(south)
            newNode.prev = currentNode
            current.next = newNode

            # print(south)

        if(south == coordinate):
            # print(south)
            print("DAPETT s")
            break

        if(world[west[0]//32][west[1]//32] != '=' and isInLinkedList(west) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(west)

            newNode.prev = currentNode
            current.next = newNode

        if(west == coordinate):

            print("DAPETT west")
            break

        now += 1


def on_key_up(key):
    if key in (keys.LEFT, keys.RIGHT):
        pacman.dx = 0
    if key in (keys.UP, keys.DOWN):
        pacman.dy = 0


def on_key_down(key):
    print(pacman.x, pacman.y)
    if key == keys.LEFT:
        pacman.dx = -SPEED
    if key == keys.RIGHT:
        pacman.dx = SPEED
    if key == keys.UP:
        pacman.dy = -SPEED
    if key == keys.DOWN:
        pacman.dy = SPEED


# Game set up
load_level(1)
bfs([384, 0])

current = head
print("=======================")
while current.next is not None:
    print(current.data)
    current = current.next

listPath = []

while current is not None:
    listPath.insert(0, current.data)
    print(current.data)
    current = current.prev


print(listPath)
# for row in world:
#     print(row)
# print(world[2][2], "adsfgh")


def update():
    move_ahead(pacman)
    move_ahead(marker)

    if len(listPath) != 0:
        marker.x = listPath[0][1]
        marker.y = listPath[1][0]
        time.sleep(0.5)

    if len(listPath) != 0:
        listPath.pop(0)
