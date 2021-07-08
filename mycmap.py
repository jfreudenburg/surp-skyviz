# Code from https://towardsdatascience.com/beautiful-custom-colormaps-with-matplotlib-5bab3d1f0e72
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def hex_to_rgb(value):
    '''
    Converts hex to rgb colours
    value: string of 6 characters representing a hex colour.
    Returns: list length 3 of RGB values'''
    value = value.strip("#") # removes hash symbol if present
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_dec(value):
    '''
    Converts rgb to decimal colours (i.e. divides each value by 256)
    value: list (length 3) of RGB values
    Returns: list (length 3) of decimal values'''
    return [v/256 for v in value]


def get_continuous_cmap(hex_list, float_list=None):
    ''' creates and returns a color map that can be used in heat map figures.
        If float_list is not provided, colour map graduates linearly between each color in hex_list.
        If float_list is provided, each color in hex_list is mapped to the respective location in float_list. 
        
        Parameters
        ----------
        hex_list: list of hex code strings
        float_list: list of floats between 0 and 1, same length as hex_list. Must start with 0 and end with 1.
        
        Returns
        ----------
        colour map'''
    rgb_list = [rgb_to_dec(hex_to_rgb(i)) for i in hex_list]
    if float_list:
        pass
    else:
        float_list = list(np.linspace(0,1,len(rgb_list)))
        
    cdict = dict()
    for num, col in enumerate(['red', 'green', 'blue']):
        col_list = [[float_list[i], rgb_list[i][num], rgb_list[i][num]] for i in range(len(float_list))]
        cdict[col] = col_list
    cmp = mcolors.LinearSegmentedColormap('my_cmp', segmentdata=cdict, N=256)
    return cmp

mauve = get_continuous_cmap(['1E252A',
                             '2A323A',
                             '373D4A',
                             '434859',
                             '505168',
                             '5E5D78',
                             '6F6A86',
                             '817795',
                             '9188A3',
                             'A19AB0',
                             'B0ABBE',
                             'C1BCCB'])

bluegreen = get_continuous_cmap(['#083428',
                                 '#0d4237', 
                                 '#125146', 
                                 '#186156', 
                                 '#1d7167', 
                                 '#238178', 
                                 '#2a918a', 
                                 '#39a297', 
                                 '#55b39b', 
                                 '#72c3a0', 
                                 '#90d2a4', 
                                 '#afe1a9'])

purples = get_continuous_cmap(['18133A',
                               '271845',
                               '391D4F',
                               '4E225A',
                               '642764',
                               '6E2C5F',
                               '824678',
                               '956090',
                               'A87BA6',
                               'BA96BB',
                               'CBB1CD',
                               'DCCDDF'])

greens = get_continuous_cmap(['#083428', 
                              '#0e4539', 
                              '#14564b', 
                              '#176760', 
                              '#16787c', 
                              '#148a99', 
                              '#0eab95', 
                              '#07d582', 
                              '#00ff6e'])

blues = get_continuous_cmap(['#010e3d', 
                             '#011640', 
                             '#001d44', 
                             '#002547', 
                             '#002c49', 
                             '#00314b', 
                             '#00364c', 
                             '#003b4d', 
                             '#005663', 
                             '#007b84', 
                             '#00a0a5', 
                             '#00c5c6'])

sunset = get_continuous_cmap(['#221155', 
                              '#412156', 
                              '#593256', 
                              '#704356', 
                              '#865655', 
                              '#9b6a54', 
                              '#af7e51', 
                              '#c3934e', 
                              '#d6a949', 
                              '#e8c043', 
                              '#f7d83b', 
                              '#fff332'])

hotpink = get_continuous_cmap(['150070',
                               '320085',
                               '550099',
                               '7D00AD',
                               'A900C2',
                               'D602D6',
                               'EB07C9',
                               'FA0CB3',
                               'FB25CA',
                               'FD3EDD',
                               'FE57ED',
                               'FF70FA',
                               'FB8AFF',
                               'F6A4FF',
                               'F5BEFF'])

lf = get_continuous_cmap(['#010052', 
                          '#27015d', 
                          '#410066', 
                          '#59016f', 
                          '#700575', 
                          '#870e79', 
                          '#9e187b', 
                          '#b42479', 
                          '#ca3273', 
                          '#de4166', 
                          '#f0534e', 
                          '#fc6a13'])