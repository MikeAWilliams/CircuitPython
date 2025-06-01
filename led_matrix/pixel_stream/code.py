import time
import math
import displayio
import random
from adafruit_matrixportal.matrix import Matrix

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
DELAY = 0.02
PALETTE_SIZE = 100

def make_big_palette(size):
    print("Creating palette with size:", size)
    palette = displayio.Palette(size)
    index = 0
    size_per_color = int(size** (1/3))
    color_step = 255 // size_per_color
    print("size_per_color:", size_per_color, "color_step:", color_step)
    for r in range (0, 255, color_step):
        for g in range (0, 255, color_step):
            for b in range (0, 255, color_step):
                if index < size:
                    palette[index] = (r << 16) | (g << 8) | b
                    index += 1
    print("maximum index:", index - 1)
    return palette 

def draw_full_palette(bitmap, size):
    color_index = 0 
    for j in range(MATRIX_HEIGHT):
        for i in range(MATRIX_WIDTH):
            bitmap[i,j]= color_index
            color_index = color_index + 1
            if color_index >= size:
                color_index = 0

def clear_full_screen(bitmap):
    for j in range(MATRIX_HEIGHT):
        for i in range(MATRIX_WIDTH):
            bitmap[i,j] = 0  # Assuming 0 is the index for black or empty color

class Mover:
    def __init__(self, x, y, vx, vy, color_index):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color_index = color_index
        self.should_die = False
    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Check horizontal bounds
        if self.x < 0 or self.x >= MATRIX_WIDTH or self.y < 0 or self.y >= MATRIX_HEIGHT:
            self.should_die = True

def draw_mover(bitmap, mover):
    if not mover.should_die:
        bitmap[int(mover.x), int(mover.y)] = 0
    mover.move()
    if not mover.should_die:
        bitmap[int(mover.x), int(mover.y)] = mover.color_index 

def update_display(display, bitmap, spawn_points, streamers):
    display.auto_refresh = False
    for spawner in spawn_points:
        streamers.append(create_random_mover(spawner[0], spawner[1]))
    for streamer in streamers:
        draw_mover(bitmap, streamer)
        if streamer.should_die:
            streamers.remove(streamer)
    display.auto_refresh = True

def create_random_mover(i, j):
    rand_vx = random.uniform(-2, 2)
    rand_vy = random.uniform(-2, 2)
    if rand_vx == 0 and rand_vy == 0:
        rand_vx = 1  # Ensure at least one movement direction is non-zero
    return Mover(i, j, rand_vx, rand_vy, random.randint(0, PALETTE_SIZE - 1))

palette = make_big_palette(PALETTE_SIZE)
print("Palette size:", len(palette))

matrix = Matrix(width=MATRIX_WIDTH, height=MATRIX_HEIGHT, bit_depth=6)
display = matrix.display
group = displayio.Group()
display.show(group)

bitmap = displayio.Bitmap(display.width, display.height, len(palette))

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group.append(tile_grid)

# draw the full palette just once
draw_full_palette(bitmap, len(palette))
time.sleep(5)
clear_full_screen(bitmap)

# just one mover for now
spawn_points = []
spawn_points.append((MATRIX_WIDTH // 2, MATRIX_HEIGHT // 2)) 
spawn_points.append((MATRIX_WIDTH // 4, MATRIX_HEIGHT // 2)) 
spawn_points.append((MATRIX_WIDTH - MATRIX_WIDTH // 4, MATRIX_HEIGHT // 2)) 
streamers = []
print("spawn points ", spawn_points)

while True:
    update_display(display, bitmap, spawn_points, streamers)
    time.sleep(DELAY)
