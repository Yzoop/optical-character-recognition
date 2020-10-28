import os
from random import randint, sample

import matplotlib.pyplot as plt
from data_mining.image_manager import image_generator as n_generator, character_generator as c_generator
from data_mining.image_manager.saver import *
from PIL import Image, UnidentifiedImageError, ImageDraw

SAVE_BOUNDING_TRAIN_PATH = 'train\\characters_with_bounding'
SAVE_SPLITS_TRAIN_PATH = 'train\\strictly_characters'

SAVE_BOUNDING_TEST_PATH = 'test\\characters_with_bounding'
SAVE_SPLITS_TEST_PATH = 'test\\strictly_characters'

SAVE_STRICTLY_IMG_PATH = 'train\\strictly_imgs'

SAVE_PANDAS_TRAIN_PATH = 'train\\csvdata'
SAVE_PANDAS_IMAGE_TRAIN_PATH = 'train\\csvdata\\images'


def resize_all_split_images(main_folders, new_size=(32, 32), verbose=False):
    for main_folder in main_folders:
        if verbose:
            print('current main:', main_folder)
        for class_fold in os.listdir(main_folder):
            print('\tcurrent class_fold:', class_fold)
            cur_full_path = os.path.join(main_folder, class_fold)
            for file in os.listdir(cur_full_path):
                file_full_path = os.path.join(cur_full_path, file)
                try:
                    Image.open(file_full_path).resize(new_size).save(file_full_path)
                except UnidentifiedImageError:
                    if verbose:
                        print('warning: image', file_full_path, 'can not be resized: UnidentfieidImageError')


def show_image(image, bound_info):
    draw = ImageDraw.Draw(image)
    for bound_data in bound_info:
        draw.rectangle(bound_data[0], fill=None, outline="red")
    plt.imshow(image)
    plt.show()


def start_generating_images(characters_to_generate, splits_path, path_for_img_detection):
    my_modes = [n_generator.FILL_WITH_LINES]
    name_counter = 0
    generate_folders_for_save(characters_to_generate.keys(), splits_path, verbose=True)

    while len(characters_to_generate) > 0:
        print(name_counter)
        image, colors = n_generator.get_generated_image()
        image, colors = n_generator.get_image_with_noise(image, colors, my_modes, level_of_noise=0.02)
        num_characters_to_gen = randint(1, min(len(characters_to_generate),
                                               c_generator.get_max_number_of_characters(image.size)))
        chosen_characters = sample(characters_to_generate.keys(), num_characters_to_gen)
        for ch in chosen_characters:
            characters_to_generate[ch] -= 1
            if characters_to_generate[ch] == 0:
                characters_to_generate.pop(ch)
        image, bounds = c_generator.generate_characters(image, chosen_characters, colors)
        # DEBUG
        image, colors = n_generator.get_image_with_noise(image, colors, my_modes, level_of_noise=0.02)
        save_pd_data(image, bounds, SAVE_PANDAS_IMAGE_TRAIN_PATH)
        save_strictly_chars(image, bounds, SAVE_STRICTLY_IMG_PATH)
        name_counter += 1


def create_folders(list_folds):
    for fold in list_folds:
        try:
            os.mkdir(fold)
        except:
            print('folder', fold, 'already created')


if __name__ == "__main__":
    splits_folders = [SAVE_SPLITS_TEST_PATH, SAVE_SPLITS_TRAIN_PATH]
    bounding_folders = [SAVE_BOUNDING_TEST_PATH, SAVE_BOUNDING_TRAIN_PATH]
    create_folders([SAVE_SPLITS_TEST_PATH, SAVE_SPLITS_TRAIN_PATH,
                    SAVE_BOUNDING_TRAIN_PATH, SAVE_BOUNDING_TEST_PATH,
                    SAVE_STRICTLY_IMG_PATH,
                    SAVE_PANDAS_TRAIN_PATH, SAVE_PANDAS_IMAGE_TRAIN_PATH])
    sizes = [200, 1]
    for splits_folder, bounding_folder, num_chars in zip(splits_folders, bounding_folders, sizes):
        characters_to_generate = c_generator.get_dict_of_characters_for_generation(num_chars)
        start_generating_images(characters_to_generate, splits_folder, bounding_folder)
    final_save_pd_data('train')
    resize_all_split_images([SAVE_SPLITS_TEST_PATH, SAVE_SPLITS_TRAIN_PATH], verbose=True)
