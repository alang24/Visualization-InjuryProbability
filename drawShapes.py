# Allen Lang
# Updated: October 2020
# https://github.com/alang24/Injury-Visualization

import numpy as np
import math
from PIL import ImageFont
import pandas as pd


def drawCircle(row, drawer):
    """
    drawCircle is a function that is applied across a DataFrame (circle) along axis = 1, so each entry is a row.
    It takes in a row and an ImageDraw object. The row comes from the DataFrame that has all the body parts that will
    have circles drawn on them. Since ImageDraw module's ellipse method takes in a point that is the top-left corner
    of a box, and the DataFrame contains coordinates of the circle's center, proper adjustments were made. The center,
    radius, and color are read in, and the top-left is found by adjusting the center by the radius.

    :param row: row in circle DataFrame, contains body part information for shape and circle properties
    :param drawer: ImageDraw object that will draw circles
    :return: nothing, ImageDraw object will just draw on top of the image
    """
    # get properties
    center = (row['X'], row['Y'])
    r = row['R']
    color = row['Color']

    # calculate coordinate of top left corner
    box = (center[0] - r, center[1] - r, center[0] + r, center[1] + r)
    drawer.ellipse(box, fill=color, outline=color)
    return


def drawEllipse(row, drawer):
    """
    drawEllipse is a function that is applied across a DataFrame (ellipse) along axis = 1, so each entry is a row.
    It takes in a row and an ImageDraw object. The row comes from the DataFrame that has all the body parts that will
    have ellipses drawn on them. Since the ellipse method cannot change in orientation, a list of polygons had to be
    produced instead, parameterizing the ellipse formula. The ellipse DataFrame already had the ellipse properties
    necessary to define a proper ellipse.

    :param row: row in ellipse DataFrame, contains body part information for shape and ellipse properties
    :param drawer: ImageDraw object that will draw ellipse
    :return: nothing, ImageDraw object will just draw on top of the image
    """
    # get properties/define precision
    a = row['A']
    b = row['B']
    xSh = row['xSh']
    ySh = row['ySh']
    theta = row['theta']
    precision = 200
    color = row['Color']

    # parameterize and draw
    t = np.linspace(0, 2*math.pi, precision)
    ell = []

    for i in np.arange(precision):
        x = a * math.cos(t[i]) * math.cos(math.radians(theta)) - b * math.sin(t[i]) * math.sin(math.radians(theta)) + xSh
        y = a * math.cos(t[i]) * math.sin(math.radians(theta)) - b * math.sin(t[i]) * math.cos(math.radians(theta)) + ySh
        ell.append((x, y))
    drawer.polygon(ell, fill=color, outline=color)
    return


def getTop5(circ, ell):
    """
    getTopFive is a helper function to drawTop5. It extracts the name and probability columns from both circle and
    ellipse DataFrames. It concatenates the two together, sorts by Probability, and returns the five body parts with
    the five highest injury probabilities.

    :param circ: circle DataFrame
    :param ell: ellipse DataFrame
    :return: a DataFrame with five highest probabilities
    """
    # extract columns
    a = circ.loc[:, ['NewName', 'Prob']]
    b = ell.loc[:, ['NewName', 'Prob']]

    # sort by probability high to low and take the first five
    combined = pd.concat([a, b]).sort_values(by='Prob', ascending=False)
    return combined.iloc[0:5]


def drawTop5(drawer, circle, ellipse):
    """
    drawTop5 writes the 5 highest body part names with their probabilities onto the top-left corner of the image. It
    uses a helper function to find that top 5, and then uses multiline_text method.

    :param drawer: ImageDraw object
    :param circle: circle DataFrame
    :param ell: ellipse DataFrame
    :return: nothing
    """

    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 18)
    top5 = getTop5(circle,ellipse)

    topfivelist = ""
    for i in np.arange(5):
        line = str(i+1) + '. ' + top5.iloc[i]['NewName'] + ': ' + str(round(top5.iloc[i]['Prob'], 2)) + '%'
        topfivelist += line + "\n\n"

    drawer.multiline_text((20, 20), topfivelist, font=fnt, fill=(0, 0, 0))

    return


def drawTitle(a, size, drawer):
    """
    drawTitle creates the title based on information about the particular crash type

    :param a: dictionary of attributes (see getAttributes)
    :param size: size of image
    :param drawer: ImageDraw object

    :return: nothing
    """
    fnt1 = ImageFont.truetype('fonts/Roboto-Regular.ttf', 34)
    W, H = size
    title1 = a['CarName'] + ' ' + a['TestType'] + ' ' + a['Index']
    w1, h1 = drawer.textsize(title1, font=fnt1)

    if a['TestType'] == 'OverCenterline':
        title2 = a['Person'] + ' Car #' + a['CarNum']
    else:
        title2 = a['Person']

    w2,h2 = drawer.textsize(title2, font=fnt1)

    drawer.text((W - w1 - 20, 20), title1, font=fnt1, fill=(0, 0, 0))
    drawer.text((W - w2 - 20, 80), title2, font=fnt1, fill=(0, 0, 0))

    fnt2 = ImageFont.truetype('fonts/Roboto-Regular.ttf', 22)

    title3 = "Occupant Model: " + a['OccName']
    w3,h3 = drawer.textsize(title3, font=fnt2)
    drawer.text((20, H - h3 - 50), title3, font=fnt2, fill=(0, 0, 0))
    return
