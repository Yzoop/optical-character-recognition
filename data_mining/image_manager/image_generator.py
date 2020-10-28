import math
from random import choice, randint, sample

from PIL import Image, ImageDraw
from data_mining.color_manager.color_generator import get_colors

MAX_NUMBER_OF_ELEMENTS_NOISE = 500

FILL_WITH_LINES = 1
FILL_WITH_ELLIPSES = 2
FILL_WITH_RECTANGLES = 3
FILL_WITH_DOTS = 4

DEFAULT_COLORS = get_colors()
DEFAULT_COLOR_MODE = "RGB"
DEFAULT_SHAPE = (256, 256)


def get_random_point(bound_h, bound_w):
    return randint(0, bound_h), randint(0, bound_w)


def __is_prime_number(num):
    # Iterate from 2 to n / 2
    #1 is not prime only for my 1by1 grid
    if num == 1:
        return False
    for i in range(2, num // 2 + 2):
        # If num is divisible by any number between
        # 2 and n / 2, it is not prime
        if (num % i) == 0:
            return False
    return True


def __get_two_close_dividers(num):
    difference_value = num
    val2 = 1
    close_values = (1, 1)
    for val1 in range(1, num // 2 + 1):
        if num % val1 == 0:
            val2 = num // val1
            current_difference = abs(val2 - val1)
            if current_difference < difference_value:
                difference_value = current_difference
                close_values = (val1, val2) if (val1 < val2) else (val2, val1)
    return close_values


def get_grid_of_image(img_h, img_w, min_num_of_cells):
    '''

    :param img_h:
    :param img_w:
    :param min_num_of_cells:
    :return: number of raws and number of columns of an image grid
    '''
    while __is_prime_number(min_num_of_cells):
        min_num_of_cells += 1
    grid_val1, grid_val2 = __get_two_close_dividers(min_num_of_cells)
    return (grid_val1, grid_val2) if img_h < img_w else (grid_val2, grid_val1)


def fill_image(image, noise, available_colors, mods):
    assert len(mods) > 0
    num_elements = int(noise * MAX_NUMBER_OF_ELEMENTS_NOISE)
    img_h, img_w = image.size
    drawer = ImageDraw.Draw(image)
    for mode in mods:
        for _ in range(num_elements):
            p1, p2 = get_random_point(img_h, img_w), get_random_point(img_h, img_w)
            clr = choice(available_colors)
            if mode == FILL_WITH_LINES:
                drawer.line([p1, p2], fill=clr)
            elif mode == FILL_WITH_ELLIPSES:
                drawer.ellipse([p1, (p1[0] + randint(1, 10), p1[1] + randint(1, 10))], fill=None, outline=clr)
            elif mode == FILL_WITH_DOTS:
                drawer.point([p1, p2], fill=clr)
    del drawer
    return image


def get_generated_image(size=DEFAULT_SHAPE, color_mode=DEFAULT_COLOR_MODE, colors=DEFAULT_COLORS):
    colors_left = colors.copy()
    outer_color = choice(colors_left)
    generated_image = Image.new(color_mode, size, outer_color)
    colors_left.remove(outer_color)
    return generated_image, colors_left


def get_image_with_noise(img_obj, colors_available, additional_modes=None, level_of_noise=0):
    if additional_modes is None:
        additional_modes = [None]
    fill_image(img_obj, level_of_noise, colors_available, additional_modes)
    return img_obj, colors_available
