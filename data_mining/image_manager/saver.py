import os
import random
import string
import pandas as pd
import numpy as np
from dict2xml import dict2xml
import data_mining.image_manager.character_generator as c_gen

__pandas_data = {'image_id': [], 'width': [], 'height': [], 'bbox': []}
__strictly_chars_data = {'image': [], 'label': []}


def save_strictly_chars(img, boundings, path):
    for bound_data in boundings:
        box = bound_data[0]
        label = bound_data[1]
        char_img = img.crop((box[0], box[1], box[2], box[3]))
        new_name = get_random_alphanumeric_string(15)
        char_img.save(os.path.join(path, new_name) + '.png')
        __strictly_chars_data['image'].append(new_name)
        __strictly_chars_data['label'].append(label)


def generate_folders_for_save(characters, father_path, verbose=False):
    for char in characters:
        full_path = os.path.join(father_path, c_gen.CHARACTERS_CLASS_NAMES[char])
        try:
            os.mkdir(full_path)
            if verbose:
                print('created', full_path, 'folder')
        except OSError:
            print('error: ', full_path, 'already exists')


def get_random_alphanumeric_string(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str


def save_boundings_xml(folder, img_name, img_format, img_size, boundings_data):
    full_img_path = os.path.join(folder, img_name + img_format)
    full_xml_path = os.path.join(folder, img_name + '.xml')
    dict_bounding_data = {'annotation': {'folder': folder,
                                         'filename': img_name,
                                         'path': full_img_path,
                                         'source': {'database': 'Unknown'},
                                         'size': {'width': img_size[0],
                                                  'height': img_size[1],
                                                  'depth': 3},
                                         'segmented': 0,
                                         'object': []}}
    for bound_data in boundings_data:
        dict_bounding_data['annotation']['object'].append({
            'name': 'CHARACTER',
            'pose': 'Unspecified',
            'truncated': 0,
            'difficult': 0,
            'bndbox': {'xmin': bound_data[0][0], 'ymin': bound_data[0][1],
                       'xmax': bound_data[0][2], 'ymax': bound_data[0][3]}
        })
    xml_bounding_data = dict2xml(dict_bounding_data)
    open(full_xml_path, 'w+').write(xml_bounding_data)


def save_pd_data(img, bboxes, path, width=256, height=256):
    name = get_random_alphanumeric_string(10)
    while name in __pandas_data['image_id']:
        name = get_random_alphanumeric_string()
    for bbox_data in bboxes:
        bbox_data = np.array([bbox_data[0][0],
                              bbox_data[0][1],
                              bbox_data[0][2] - bbox_data[0][0],
                              bbox_data[0][3] - bbox_data[0][1]], dtype='float')
        __pandas_data['image_id'].append(name)
        __pandas_data['width'].append(width)
        __pandas_data['height'].append(height)
        __pandas_data['bbox'].append(bbox_data)
    img.save(os.path.join(path, name) + '.png')


def final_save_pd_data(path):
    pd_data = pd.DataFrame(__pandas_data)
    pd_data.to_csv(os.path.join(path, 'train.csv'), index=False)
    strictly_data = pd.DataFrame(__strictly_chars_data)
    strictly_data.to_csv(os.path.join(path, 'strictly.csv'), index=False)
