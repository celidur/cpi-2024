import base64
import io
from .game import Color

from PIL import Image

def to_2d_arr(encoded_image: str):
    decoded = base64.decode(encoded_image)
    img = Image.open(io.BytesIO(decoded))
    width, height = img.size
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    cell_size = 20
    grid_size = 20
    for y in range(grid_size):
        for x in range(grid_size):
            center_x = x * cell_size + cell_size // 2
            center_y = y * cell_size + cell_size // 2
            pixel = img.getpixel((center_x, center_y))
            color_hex = '#{:02X}{:02X}{:02X}'.format(*pixel[:3])
            color = Color.from_hex(color_hex)
            board[y][x] = color
    return board
        