import random
import time
import pgzrun

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
    # screen.clear()
    for y, row in enumerate(world):
        for x, block in enumerate(row):
            image = char_to_image.get(block, None)
            if image:
                screen.blit(char_to_image[block], (x*BLOCK_SIZE, y*BLOCK_SIZE))
    pacman.draw()


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
            break

        if(world[east[0]//32][east[1]//32] != '=' and isInLinkedList(east) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(east)
            current.next = newNode
            current.next.prev = currentNode

        if(east == coordinate):
            break

        if(world[south[0]//32][south[1]//32] != '=' and isInLinkedList(south) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(south)
            newNode.prev = currentNode
            current.next = newNode

        if(south == coordinate):
            break

        if(world[west[0]//32][west[1]//32] != '=' and isInLinkedList(west) == True):
            current = head
            while current.next is not None:
                current = current.next

            newNode = Node(west)

            newNode.prev = currentNode
            current.next = newNode

        if(west == coordinate):
            break

        now += 1


# Load Txt
load_level(1)

# Call Bfs
bfs([384, 0])

current = head
listNode = []
listPath = []
move = []

while current.next is not None:
    listNode.append(current.data)
    current = current.next


while current is not None:
    listPath.insert(0, current.data)
    move.insert(0, current.data)
    current = current.prev


def update():
    move_ahead(pacman)

    if(len(listNode) != 0):
        if len(listNode) != 0:
            screen.blit('marker.png', (listNode[0][1], listNode[0][0]))
            time.sleep(0.05)

        if len(listNode) != 0:
            listNode.pop(0)
        else:
            mode = 'Move'

    elif(len(listPath) != 0):

        if len(listPath) != 0:
            screen.blit('dot.png', (listPath[0][1], listPath[0][0]))
            time.sleep(0.05)

        if len(listPath) != 0:
            listPath.pop(0)
    else:
        screen.clear()
        if len(move) != 0:
            pacman.x = move[0][1]
            pacman.y = move[0][0]
            time.sleep(0.05)

        if len(move) != 0:
            move.pop(0)


for row in world:
    print(row)

pgzrun.go()
