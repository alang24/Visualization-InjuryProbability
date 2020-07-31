import numpy as np
import math
from PIL import ImageFont


def drawCircle(row, drawer):

    center = (row['X'],row['Y'])
    r = row['R']

    color = row['Color']

    box = (center[0] - r, center[1] - r, center[0] + r, center[1] + r)
    drawer.ellipse(box, fill=color, outline=color)
    return


def drawEllipse(row, drawer):
    a = row['A']
    b = row['B']
    xSh = row['xSh']
    ySh = row['ySh']
    theta = row['theta']
    precision = 200
    color = row['Color']
    t = np.linspace(0, 2*math.pi, precision)
    ell = []

    for i in np.arange(precision):
        x = a * math.cos(t[i]) * math.cos(math.radians(theta)) - b * math.sin(t[i]) * math.sin(math.radians(theta)) + xSh
        y = a * math.cos(t[i]) * math.sin(math.radians(theta)) - b * math.sin(t[i]) * math.cos(math.radians(theta)) + ySh

        ell.append((x, y))
    drawer.polygon(ell, fill=color, outline=color)
    return


def drawTop5(top5, drawer):
    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 18)

    topfivelist = ""
    for i in np.arange(5):
        line = str(i+1) + '. ' + top5.iloc[i]['NewName'] + ': ' + str(round(top5.iloc[i]['Prob'], 2)) + '%'
        topfivelist += line + "\n\n"

    drawer.multiline_text((20, 20), topfivelist, font=fnt, fill=(0, 0, 0))

    return


def drawTitle(name, index, person, size, drawer, twocars, carNum):
    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 36)
    W,H = size
    title1 = name + ' ' + index
    w1,h1= drawer.textsize(title1, font=fnt)

    if twocars:
        title2 = person + ' Car #' + carNum
    else:
        title2 = person

    w2,h2= drawer.textsize(title2, font=fnt)

    drawer.text((W - w1 - 20, 20), title1, font=fnt, fill=(0, 0, 0))
    drawer.text((W - w2 - 20, 80), title2, font=fnt, fill=(0, 0, 0))

    return
