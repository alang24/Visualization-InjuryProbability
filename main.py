from PIL import Image, ImageDraw
import pandas as pd
from pickColor import *
from linkTables import *
from drawShapes import *
from getTopFive import *


def makeImage(name, sheet, firstind):
    coordCirc = pd.read_excel('coord.xlsx',sheet_name=0)
    coordEll = pd.read_excel('coord.xlsx',sheet_name=1)

    image = 'ciss_human_driver_legend_CAB.jpg'
    person = 'Driver'
    carNum = '-1'
    if name == 'Guardrail':
        index = sheet
    elif name == 'OverCenterline':
        temp = int(sheet[:-1]) - firstind + 1
        if temp % 2 == 0:
            temp = temp - 1
        if temp > 8:
            index = str(temp % 8//2+1+4)
        else:
            index = str(temp % 8//2+1)

        if int(sheet[:-1]) % 2 == 0:
            carNum = '2'
        else:
            carNum = '1'
    else:
        carNum = '-1'
        if int(sheet[:-1]) % 8 == 0:
            index = '8'
        else:
            index = str(int(sheet[:-1]) % 8)

    if sheet[-1] == 'P':
        image = 'ciss_human_passenger_legend_CAB.jpg'
        person = 'Passenger'

    simData = pd.read_excel('simulation_results/' + name + '_injury_analysis.xlsx', sheet_name=sheet, header=None,
                            names=['Name', 'Fill', 'Prob'])

    numrows = simData.shape[0]

    case = 0
    if numrows == 52:
        case = 1
    elif numrows == 63:
        case = 2
    elif numrows == 83:
        case = 3
    elif numrows == 111:
        case = 4
    else:
        print("Incorrect number of rows. Something has changed with the table.")
        exit(1)

    coordCirc['NewName'] = coordCirc.apply(getName, axis=1, args=(simData, case))
    coordCirc['Prob'] = coordCirc.apply(getProb, axis=1, args=(simData,))
    coordCirc['Color'] = coordCirc.apply(colorPicker, axis=1)

    coordEll['NewName'] = coordEll.apply(getName, axis=1, args=(simData, case))
    coordEll['Prob'] = coordEll.apply(getProb, axis=1, args=(simData,))
    coordEll['Color'] = coordEll.apply(colorPicker, axis=1)

    topFive = getTopFive(coordCirc, coordEll)

    with Image.open(image) as im:
        drawer = ImageDraw.Draw(im)
        coordCirc.apply(drawCircle, axis=1, args=(drawer,))
        coordEll.apply(drawEllipse, axis=1, args=(drawer,))

        drawTop5(topFive, drawer)

        if name == 'OverCenterline':
            drawTitle(name, index, person, im.size, drawer, True, carNum)
            im.save('images/' + name + '_' + index + '_' + carNum + '_' + person + '.jpg')
        else:
            drawTitle(name, index, person, im.size, drawer, False, carNum)
            im.save('images/' + name + '_' + index + '_' + person + '.jpg')
    return


simulname = 'RoadsideTree'
excelfile = pd.ExcelFile('simulation_results/' + simulname + '_injury_analysis.xlsx')
sheetnames = excelfile.sheet_names

first = '0'
if simulname == 'OverCenterline':
    first = int(sheetnames[0][:-1])

for sheetname in sheetnames:
    makeImage(simulname, sheetname,first)
    print("Finished image for " + sheetname)

