__author__ = "Lingteng Kong <jn19830@bristol.ac.uk>"
__created__ = "[10-12-2020 Wed 20:00]"

import codecs
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage, misc
import textwrap


# dir = './20_11_2020'
# dir = './25_11_2020'
dir = './07_12_2020'


name_tag = '600nm'


min = 5
max = 10

reduce = True  # subtract min value in every image
filter = False  # median_filter

# only one should be True
save_img = False  # save images
save_multi = True  # save multiple images


def get_data(indir, reduce=True):
    '''get the data from file, length and width is the image shape'''

    with codecs.open(indir, encoding='utf-8-sig') as f:  # open the file
        # initilization
        data = []

        # remove the information lines
        for line in f:
            if len(line) > 300:
                s = line.split(',')
                # remove the first line of useless data and the last enter
                data.append([float(s[i])
                             for i in range(1, len(s)-1)])

        data = np.array(data)

        if reduce:
            # print(data.min())
            data -= data.min()

    return data


def fig_save(image, info, path, name_tag, cmap, min, max, filter):
    '''save image and plot infomation'''

    if filter:
        image = ndimage.median_filter(image, size=20)

    fig, ax = plt.subplots(1, 2, figsize=(10, 10))

    im = ax[0].imshow(image, cmap=cmap, vmin=min, vmax=max)
    ax[0].set_xlabel('Pixels')
    ax[0].set_ylabel('Pixels')
    fig.colorbar(im, ax=ax[0])

    ax[1].text(0.5, 0.4, info, va='center',
               ha='center', size=15)
    ax[1].axis('off')

    if not os.path.exists(path):
        os.mkdir(path)

    plt.savefig('%s/added_%s.jpg' % (path, name_tag))
    plt.savefig('%s/added_%s.pdf' % (path, name_tag))

    plt.show()


def fig_multiSave(imageset, subplots_row, subplots_coloum, path, name_tag, cmap, min, max, filter):
    '''save multiple images, imageset contains multiple images'''

    num_subplot = subplots_row * subplots_coloum

    if not os.path.exists(path):
        os.mkdir(path)

    path_jpg = '%s/%s' % (path, 'jpg')
    path_pdf = '%s/%s' % (path, 'pdf')

    if not os.path.exists(path_jpg):
        os.mkdir(path_jpg)

    if not os.path.exists(path_pdf):
        os.mkdir(path_pdf)

    for i, img in enumerate(imageset):

        n = i % num_subplot

        if n == 0:
            fig, ax = plt.subplots(
                subplots_row, subplots_coloum, figsize=(subplots_coloum*10, subplots_row*20))

        if filter:
            img = ndimage.median_filter(img, size=20)

        ax = ax.ravel()
        im = ax[n].imshow(img, cmap=cmap, vmin=min, vmax=max)
        ax[n].set_title('Picture number: %s' % (i+1))
        fig.colorbar(im, ax=ax[n])

        if n == (num_subplot - 1) or i == (len(imageset) - 1):

            file_num = (i+1) / num_subplot

            if file_num != int(file_num):
                file_num = int(file_num) + 1

            plt.savefig('%s/%s_%d.jpg' % (path_jpg, name_tag, file_num))
            plt.savefig('%s/%s_%d.pdf' % (path_pdf, name_tag, file_num))
            plt.close()


if __name__ == '__main__':

    imageset = []

    print('######### reading files #########')

    for root, dirs, files in os.walk(dir):
        for file in sorted(files):  # let the files in files order
            if file.startswith(name_tag) and file.endswith('.asc'):
                print(file)
                indir = os.path.join(root, file)
                data = get_data(indir, reduce)
                imageset.append(data)

    imageset = np.array(imageset)  # seperate image
    image = np.sum(imageset, axis=0)  # sum of images
    files_number = len(imageset)  # number of images

    # change long name_tage into multiple lines
    name = "\n".join(textwrap.wrap(name_tag, 20))
    info = f'There are {files_number} files with: \n \n path: {dir}\n \n name: \n{name}\n \n shape: {image.shape}'

    print('######### finish reading #########')

    print('-----------------------------')
    print(info)
    print('-----------------------------')

    counts_min = files_number * min
    counts_max = files_number * max

    fig_path = './figure/%s' % dir

    if save_img:
        print('######### plotting added images #########')
        fig_save(image, info, fig_path, name_tag, 'jet',
                 counts_min, counts_max, filter)

    if save_multi:
        print('######### plotting seperate image #########')
        fig_multiSave(imageset, 2, 3, fig_path, name_tag,
                      'jet', min, max, filter)

    print('######### finished, have a good day :) #########')
