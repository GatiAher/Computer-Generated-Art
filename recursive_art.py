"""
YOUR HEADER COMMENT HERE

@author: Gati Aher
"""

import random
import math
from PIL import Image

import time

building_blocks = [
["x", 0],
["y", 0],
#["#", 0], # gets speckled effect
["prod", 2],
["avg", 2],
["cos_pi", 1],
["sin_pi", 1],
["min", 2],
["max", 2],
["sigmoid", 1]
]

NUM_TERM = 2 # number index that not terminating functions start

####################
# FUNCTION LIBRARY #
####################



#########################
# BUILD RANDOM FUNCTION #
#########################

def build_random_function(min_depth, max_depth):
    """Build a random function.

    Builds a random function of depth at least min_depth and depth at most
    max_depth. (See the assignment write-up for the definition of depth
    in this context)

    Args:
        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function

    Returns:
        The randomly generated function represented as a nested list.
        (See the assignment write-up for details on the representation of
        these functions)
    """
    # CHANGED: works

    # store list
    retlist = []

    if max_depth == 1:
        # terminate immidiately
        # CHANGED: playing around with this, random.choice([x, y])
        # retlist.append('#')
        retlist.append(random.choice(['x', 'y']))
        return retlist
    elif min_depth > 1:
        # do not terminate immidiately
        # don't pick function with zero parameters
        exp_ind = random.randint(NUM_TERM, len(building_blocks)-1)
    else:
        # possibility of picking non- and terminating options
        exp_ind = random.randint(0, len(building_blocks)-1)

    exp = building_blocks[exp_ind][0]
    retlist.append(exp)
    # find next number of arguments
    exp_num = building_blocks[exp_ind][1]

    for i in range(exp_num):
        arg = build_random_function(min_depth - 1, max_depth - 1)
        retlist.append(arg)

    return retlist



def evaluate_random_function(f, x, y):
    """Evaluate the random function f with inputs x,y.

    The representation of the function f is defined in the assignment write-up.

    Args:
        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function

    Returns:
        The function value

    Examples:
        >>> evaluate_random_function(["x"], -0.5, 0.75)
        -0.5

        >>> evaluate_random_function(["y"], 0.1, 0.02)
        0.02

    # CHANGED: added unit tests to test each function

        >>> evaluate_random_function(["prod",["x"],["y"]], 0.1, 0.02)
        0.002

        >>> evaluate_random_function(["avg",["x"],["y"]], 0.1, 0.02)
        0.060000000000000005

        >>> evaluate_random_function(["min",["x"],["y"]], 0.1, 0.02)
        0.02

        >>> evaluate_random_function(["max",["x"],["y"]], 0.1, 0.02)
        0.1

        >>> evaluate_random_function(["cos_pi",["x"]], 0.1, 0.02)
        0.9510565162951535

        >>> evaluate_random_function(["sin_pi",["y"]], 0.1, 0.02)
        0.06279051952931337

        >>> evaluate_random_function(["#"], 0.1, 0.1)
        0.1

    """

    # CHANGED: finished and passed all tests

    arg = f[0]

    if arg == "x":
        return x
    elif arg == "y":
        return y
    elif arg == "#":
        return random.choice([x, y])
    elif arg == "prod":
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    elif arg == "avg":
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y))*0.5
    elif arg == "cos_pi":
        return math.cos(math.pi * evaluate_random_function(f[1], x, y))
    elif arg == "sin_pi":
        return math.sin(math.pi * evaluate_random_function(f[1], x, y))
    elif arg == "min":
        return min(evaluate_random_function(f[1], x, y), evaluate_random_function(f[2], x, y))
    elif arg == "max":
        return max(evaluate_random_function(f[1], x, y), evaluate_random_function(f[2], x, y))
    elif arg == "sigmoid":
        return 1 / (1 + math.exp(-1 * evaluate_random_function(f[1], x, y)))
    else:
        print("VAL ERR", f)
        return ValueError()



def remap_interval(val,
                   input_interval_start=0,
                   input_interval_end=350,
                   output_interval_start=-1,
                   output_interval_end=1):
    """Remap a value from one interval to another.

    Given an input value in the interval [input_interval_start,
    input_interval_end], return an output value scaled to fall within
    the output interval [output_interval_start, output_interval_end].

    Args:
        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values

    Returns:
        The value remapped from the input to the output interval

    Examples:
        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5

    """

    # CHANGED: finished and passed all tests
    return (((val - input_interval_start) /
    (input_interval_end - input_interval_start)) *
    (output_interval_end - output_interval_start)) + output_interval_start



def color_map(val):
    """Maps input value between -1 and 1 to an integer 0-255,
    suitable for use as an RGB color code.

    Args:
        val: value to remap, must be a float in the interval [-1, 1]

    Returns:
        An integer in the interval [0,255]

    Examples:
        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)



def generate_art(filename, x_size=350, y_size=350, a=7, b=9, c=7, d=9, e=7, f=9):
    """Generate computational art and save as an image file.

    Args:
        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    t0 = time.time()
    red_function = build_random_function(a, b)
    green_function = build_random_function(c, d)
    blue_function = build_random_function(e, f)
    t1 = time.time()
    print("*** TIME TO BUILD *** ", str(t1 - t0))

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()

    t0 = time.time()
    x = list(map(remap_interval, range(x_size)))
    y = list(map(remap_interval, range(y_size)))
    t1 = time.time()
    print("*** TIME TO MAP *** ", str(t1 - t0))

    # TODO: array + multiprocess
    t0 = time.time()
    for i in range(x_size):
        ta = time.time()
        print(str(i) + " TIME CHECK: " + str(ta - t0))
        for j in range(y_size):
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x[i], y[j])),
                color_map(evaluate_random_function(green_function, x[i], y[j])),
                color_map(evaluate_random_function(blue_function, x[i], y[j]))
            )
    t1 = time.time()
    print("*** TIME TO EVALUATE *** ", str(t1 - t0))

    # saving image and function
    t0 = time.time()
    suffix = "_".join([str(a), str(b), str(c), str(d), str(e), str(f)])
    filename_new = filename + "-" + suffix
    im.save(filename_new + ".png")

    f = open(filename_new + '.txt', 'w')

    f.write("\n" + "FILE NAME: " + filename_new)

    f.write("\n" + "RED FUNCTION: " + str(red_function))
    print("RED FUNCTION: " + str(red_function))

    f.write("\n" + "GREEN FUNCTION: " + str(green_function))
    print("GREEN FUNCTION: " + str(green_function))

    f.write("\n" + "BLUE FUNCTION: " + str(blue_function))
    print("BLUE FUNCTION: " + str(blue_function))

    f.close()
    t1 = time.time()
    print("*** TIME TO SAVE *** ", str(t1 - t0))


    print(filename_new)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # doctest.run_docstring_examples(evaluate_random_function, globals(), verbose=True)

    # change range to produce and save more images at once
    # saves to images folder with suffix defined by parameters i, a, b, c, d, e, f
    for i in range(20):
        # generate_art("images/gatic-" + str(i), a=2, b=4, c=2, d=4, e=2, f=4)
        generate_art("images/no-hash-sigmoid-c-" + str(i), a=7, b=9, c=7, d=9, e=7, f=9)
