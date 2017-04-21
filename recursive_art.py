""" This program generates random computational art. The input argument is the file name.
    The default size of the image is 350x350 pixels. The RGB values of each pixel are determined
    by building a random function for each color and then evaluate those funcitons at each
    pixel. By design, the functions have a depth of 7-9 function levels but the program
    could easily be altered to create deeper or shallower functions.

    Author : Lakhvinder Jordan <ljordan51@gmail.com>
    Course : Olin Software Design Spring 2017
    Date   : 2017-02-21
"""

import random
import math
from PIL import Image

prod = lambda x, y: x*y
avg = lambda x, y: 0.5*(x+y)
cos_pi = lambda x: math.cos(math.pi*x)
sin_pi = lambda x: math.sin(math.pi*x)
sqroot = lambda x: math.sqrt(math.fabs(x))
cubed = lambda x: x**3
xfunc = lambda x, y: x
yfunc = lambda x, y: y
FUNCS = [prod, avg, cos_pi, sin_pi, sqroot, cubed, xfunc, yfunc]


def build_func(runs):
    ind = random.randint(0, 5)  # x and y are only to be used as the final function (or the input)
    if runs == 1:  # base case for recursive function, last level should be either x or y
        ind = random.randint(6, 7)
        return FUNCS[ind]
    else:
        """ Standard recursive case in which pick_funcs returns a list with the function it chose as the first item and a
            list of the nested functions as the second item by running pick_funcs with runs-1.
        """
        if ind < 2:  # if the index is less than 2 then the func is either prod or avg in which case it needs 2 inputs
            nested1 = build_func(runs-1)
            nested2 = build_func(runs-1)
            return FUNCS[ind](nested1, nested2)
        else:
            nested = build_func(runs-1)
            return FUNCS[ind](nested)


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth. This funciton utilizes the helper function pick_funcs.
        Therefore the only real use of this runction is to choose the random depth.

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
    """
    depth = random.randint(min_depth, max_depth)
    func = lambda x, y: build_func(depth)(x, y)
    return func


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    a = val
    b = input_interval_start
    c = input_interval_end
    d = output_interval_start
    e = output_interval_end
    ans = ((a-b)/(c-b))*(e-d)+d
    # finds ratio of distance of val from input_interval_start, then multiplies that by range of output_interval and adds to output_interval_start
    return ans


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code. This is necessary for translating from the
        random function output (which is between -1 and 1) to RGB values
        (which range from 0 to 255).

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # Create some computational art!
    generate_art("myart2.png")

    # Test that PIL is installed correctly
    # test_image("noise.png")
