import os
from random import choice, randint, shuffle
from data_mining.image_manager.image_generator import get_grid_of_image
from PIL import ImageFont, ImageDraw
import matplotlib.pyplot as plt

from data_mining.miner import show_image

FONTS_PATH = 'image_manager/fonts/'
FOLDER_FOR_STRICTLY_CHARACTERS = 'strictly_characters/'
FOLDER_FOR_CHARACTERS_WITH_BOUNDS = 'characters_with_bounding/'
CHARACTERS_DEFAULT_FILE = 'characters.txt'
CHARACTERS_CLASS_NAMES = {line.split(':')[0]: line.split(':')[1] for line in open(CHARACTERS_DEFAULT_FILE)
    .read()
    .split('\n')}
MINIMUM_RECOMMENDED_CHARACTER_SIZE = 45


def get_max_number_of_characters(img_size):
    return min(img_size) // MINIMUM_RECOMMENDED_CHARACTER_SIZE


def get_dict_of_characters_for_generation(number_of_characters, characters=None):
    characters_for_generation = {}
    if characters is None:
        characters = CHARACTERS_CLASS_NAMES.keys()
    for ch in characters:
        characters_for_generation[ch] = number_of_characters
    return characters_for_generation


def __get_character_random_xy(rect_coords, char, draw, font):
    width_text, height_text = draw.textsize(char, font)
    offset_x, offset_y = font.getoffset(char)
    width_text += offset_x
    height_text += offset_y
    min_x, min_y, max_x, max_y = rect_coords
    char_x_min = min_x
    char_x_max = max_x - width_text
    char_y_min = max_y // 4 - height_text // 1.8
    char_y_max = max_y - height_text
    xy = randint(char_x_min, char_x_max), randint(char_y_min, char_y_max)
    return xy


def __get_char_box(font, char, xy):
    right, bottom = font.getsize(char)
    width, height = font.getmask(char).size
    right += xy[0]
    bottom += xy[1]
    top = bottom - height
    left = right - width
    return left, top, right, bottom


def intersects_with(rect, other_rects):
    for coord in rect:
        if coord < 0 or coord >= 255:
            return True
    for other_rect in other_rects:
        if (rect[0] < other_rect[0][2] and rect[2] > other_rect[0][0] and
            rect[1] > other_rect[0][3] and rect[3] < other_rect[0][1]) or \
           (other_rect[0][0] <= rect[0] <= other_rect[0][2] and
            rect[1] >= other_rect[0][1] and rect[3] <= other_rect[0][3]):
            return True
    return False


def generate_characters(image, characters_available, colors_available,
                        font_pathes=None, char_size_bound=(MINIMUM_RECOMMENDED_CHARACTER_SIZE, None)):
    if font_pathes is None:
        font_pathes = [os.path.join(FONTS_PATH) + font_file for font_file in os.listdir(FONTS_PATH)]
    # split image into len(characters_available char_cells
    char_cells = []
    raws, columns = get_grid_of_image(image.size[0], image.size[1], len(characters_available))
    cell_h = image.size[0] // raws
    cell_w = image.size[1] // columns
    for x_cell_id in range(columns):
        for y_cell_id in range(raws):
            char_cells.append([x_cell_id * cell_w, y_cell_id * cell_h,
                               (x_cell_id + 1) * cell_w, (y_cell_id + 1) * cell_h])
    char_size_bound = (char_size_bound[0], min(cell_h, cell_w))
    drawer = ImageDraw.Draw(image)
    characters_bounds = []
    shuffle(char_cells)
    for i, char in enumerate(characters_available):
        char_box_rectangle = None
        correct_intersect = False
        xy = None
        font = None
        while not correct_intersect:
            char_size = randint(char_size_bound[0], char_size_bound[1])
            font = ImageFont.truetype(choice(font_pathes), char_size)
            try:
                char_cell = char_cells[i].copy()
                xy = __get_character_random_xy(rect_coords=char_cell, char=char, draw=drawer, font=font)
                char_box_rectangle = __get_char_box(font, char, xy)
                correct_intersect = not intersects_with(char_box_rectangle, characters_bounds)
            except BaseException:
                print('WARNING: can not deal with letter', char, 'its bounding can not be set for', char_cell)
        drawer.text(xy, text=char, fill=choice(colors_available), font=font)
        characters_bounds.append((char_box_rectangle, char))
    return image, characters_bounds
