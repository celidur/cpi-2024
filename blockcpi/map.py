import base64
import io
from blockcpi.game import COLOR

from PIL import Image

def to_2d_arr(encoded_image: str):
    cell_size = 20
    grid_size = 20
    decoded = base64.decodebytes(bytes(encoded_image, "utf-8"))
    img = Image.open(io.BytesIO(decoded))
    board = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    

    for x in range(grid_size):
        for y in range(grid_size):
            center_x = x * cell_size + cell_size // 2
            center_y = y * cell_size + cell_size // 2
            pixel = img.getpixel((center_x, center_y))
            color_hex = '#{:02X}{:02X}{:02X}'.format(*pixel[:3])
            color = COLOR.from_hex(color_hex)
            board[y][x] = color
    return board
        