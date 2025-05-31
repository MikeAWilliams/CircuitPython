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
                if r == 0 and g == 0 and b == 0:
                    continue
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

def update_display():
    display.auto_refresh = False
    for i in range(MATRIX_WIDTH):
        for j in range(MATRIX_HEIGHT):
            color_index = random.randint(0, len(palette) - 1)
            bitmap[i, j] = color_index
    display.auto_refresh = True



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

while True:
    update_display()
    time.sleep(DELAY)
