# Allen Lang
# Updated: October 2020
# https://github.com/alang24/Injury-Visualization

from PIL import Image, ImageDraw
from pickColor import *
from linkTables import *
from drawShapes import *
from getAttributes import *
import time
import os


def makeImage(proj, test_type, sheet, car_name, single_occ, year):
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

    :param proj: HMC 2019 or HMC 2020
    :param test_type: crash type (Guardrail, MedianStrip, OverCenterline, RoadsideTree)
    :param sheet: sheet name in spreadsheet
    :param car_name: Car model
    :param single_occ: Is this simulation only have one occupant in car
    :param year: HMC Project of 2019 or 2020
    :return: nothing
    """

    # 1
    coordCirc = pd.read_excel('coord.xlsx', sheet_name=0)
    coordEll = pd.read_excel('coord.xlsx', sheet_name=1)

    # 2
    if test_type == 'OverCenterline':
        simData = pd.read_excel('simulation_results/' + proj + '/' + car_name + ' ' + test_type + ' V' + single_occ + '_Injury_Analysis.xlsx',
                                sheet_name=sheet, header=None, names=['Name', 'Metric', 'Prob'])
    else:
        simData = pd.read_excel('simulation_results/' + proj + '/' + car_name + ' ' + test_type + '_Injury_Analysis.xlsx',
                                sheet_name=sheet, header=None, names=['Name', 'Metric', 'Prob'])

    # 3
    attr = getAttributes(test_type, sheet, car_name, single_occ, simData, year)

    # 4/5
    coordCirc['NewName'] = coordCirc.apply(getName, axis=1, args=(simData, attr['OccNum']))
    coordCirc['Prob'] = coordCirc.apply(getProb, axis=1, args=(simData,))
    coordCirc['Color'] = coordCirc.apply(colorPicker, axis=1)

    coordEll['NewName'] = coordEll.apply(getName, axis=1, args=(simData, attr['OccNum']))
    coordEll['Prob'] = coordEll.apply(getProb, axis=1, args=(simData,))
    coordEll['Color'] = coordEll.apply(colorPicker, axis=1)

    # 6/7/8/9
    with Image.open(attr['Image']) as im:
        drawer = ImageDraw.Draw(im)
        coordCirc.apply(drawCircle, axis=1, args=(drawer,))
        coordEll.apply(drawEllipse, axis=1, args=(drawer,))

        drawTop5(drawer, coordCirc, coordEll)

        if attr['TestType'] == 'OverCenterline':
            drawTitle(attr, im.size, drawer)
            im.save('images/' + proj + '/' + car_name + '_' + attr['TestType'] + '_' + attr['Index'] + '_'
                    + attr['CarNum'] + '_' + attr['Person'] + '.jpg')
        else:
            drawTitle(attr, im.size, drawer)
            im.save('images/' + proj + '/' + car_name + '_' + attr['TestType'] + '_' + attr['Index'] + '_'
                    + attr['Person'] + '.jpg')
    return


def main(c):
    """
    Wrapper function for image generation process

    :param c: counter used for overhead
    :return: nothing
    """
    project ='HMC_2020'
    simulations = os.listdir('simulation_results/' + project)

    for simul_name in ['CN7 Guardrail_Injury_Analysis.xlsx']:#simulations:
        # Gets list of sheetnames from Excel Spreadsheet
        print("Making images for", simul_name.split('.')[0])
        excelfile = pd.ExcelFile('simulation_results/' + project + '/' + simul_name)
        sheet_names = excelfile.sheet_names
        print(sheet_names)

        # All spreadsheets have format "carname simulationname_injury_analysis.xlsx"
        # So variables are made to get the car name and simulation name
        fullname = simul_name[:simul_name.find('_Injury_Analysis.xlsx')].split(' ')

        name = fullname[1]
        car = fullname[0]
        # Go through Excel sheet in spreadsheet and make an image
        for sheetname in sheet_names:
            if name == 'OverCenterline':
                makeImage(project, name, sheetname, car, fullname[2][-1],project[-4:])
            else:
                makeImage(project, name, sheetname, car, '',project[-4:])
            c += 1
            print("Finished image for " + sheetname)
        print()
    return c


c = 0
start = time.time()
c = main(c)
end = time.time()
print("Total Elapsed Time: " + str(end-start))
print("Average Time per image: ", str((end-start)/c))
