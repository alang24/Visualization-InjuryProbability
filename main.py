# Allen Lang
# Updated: August 2020
# https://github.com/alang24/Injury-Visualization

from PIL import Image, ImageDraw
from pickColor import *
from linkTables import *
from drawShapes import *
from getAttributes import *


def makeImage(name, sheet, firstind):
    """
    Produces an Image for a particular sheet (simulation)
    1. Import circle/ellipse coord and create DataFrame
    2. Import simulation results based on sheet name and create DataFrame
    3. Get attributes about said simulation necessary for labeling
    4. Link circle and ellipse tables with simulation results (getting name of bodypart and probability)
    5. Use probability value to obtain a color for said shape
    6. Open the image and draw the circles/ellipses onto image
    7. Find five highest probability bodyparts and place it on top left corner
    8. Place title on top right corner
    9. Save image using attributes from step 3

    :param name: crash type (Guardrail, MedianStrip, OverCenterline, RoadsideTree)
    :param sheet: sheet name in spreadsheet
    :param firstind: for OverCenterline index calculation
    :return: nothing
    """

    # 1
    coordCirc = pd.read_excel('coord.xlsx',sheet_name=0)
    coordEll = pd.read_excel('coord.xlsx',sheet_name=1)

    # 2
    simData = pd.read_excel('simulation_results/' + name + '_injury_analysis.xlsx', sheet_name=sheet, header=None,
                            names=['Name', 'Fill', 'Prob'])

    # 3
    attr = getAttributes(name, sheet, firstind, simData)

    # 4/5
    coordCirc['NewName'] = coordCirc.apply(getName, axis=1, args=(simData, attr['Case']))
    coordCirc['Prob'] = coordCirc.apply(getProb, axis=1, args=(simData,))
    coordCirc['Color'] = coordCirc.apply(colorPicker, axis=1)

    coordEll['NewName'] = coordEll.apply(getName, axis=1, args=(simData, attr['Case']))
    coordEll['Prob'] = coordEll.apply(getProb, axis=1, args=(simData,))
    coordEll['Color'] = coordEll.apply(colorPicker, axis=1)

    # 6/7/8/9
    with Image.open(attr['Image']) as im:
        drawer = ImageDraw.Draw(im)
        coordCirc.apply(drawCircle, axis=1, args=(drawer,))
        coordEll.apply(drawEllipse, axis=1, args=(drawer,))

        drawTop5(drawer, coordCirc, coordEll)

        if name == 'OverCenterline':
            drawTitle(name, attr, im.size, drawer)
            im.save('images/' + name + '_' + attr['Index'] + '_' + attr['CarNum'] + '_' + attr['Person'] + '.jpg')
        else:
            drawTitle(name, attr, im.size, drawer)
            im.save('images/' + name + '_' + attr['Index'] + '_' + attr['Person'] + '.jpg')
    return


for simulname in ['Guardrail', 'MedianStrip', 'RoadsideTree','OverCenterline']:
    excelfile = pd.ExcelFile('simulation_results/' + simulname + '_injury_analysis.xlsx')
    sheetnames = excelfile.sheet_names

    first = '0'
    if simulname == 'OverCenterline':
        first = int(sheetnames[0][:-1])

    for sheetname in sheetnames:
        makeImage(simulname, sheetname,first)
        print("Finished image for " + sheetname)

