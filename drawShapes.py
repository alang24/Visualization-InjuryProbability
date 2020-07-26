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


def drawTitle(name,index,person,size, drawer):
    fnt = ImageFont.truetype('fonts/Roboto-Regular.ttf', 18)

    title = name + ' ' + str(index) + '\n' + person

    drawer.multiline_text((size[0] - 20, 20), title, font=fnt, fill=(0, 0, 0))

    return
