# Allen Lang
# Updated: August 2020
# https://github.com/alang24/Injury-Visualization


def getCase(simData):
    """
    Helper function to get case number

    :param simData: simulation data
    :return: case number, refer to simulation_matrix for specifics
    """

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
    return case


def getAttributes(name, sheet, firstind, simData):
    """
    Gets information necessary for naming/saving the image

    Image: name of image file to be used
    Person: Driver or passenger
    Index: Sheet number within the spreadsheet
    Carnum: Car number (OverCenterline only)
    Case: needed to link tables

    :param name: crash type (Guardrail, MedianStrip, OverCenterline, RoadsideTree)
    :param sheet: sheet name in spreadsheet
    :param firstind: for OverCenterline index calculation
    :param simData: simData to count number of rows
    :return:
    """
    a = {}

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
        if int(sheet[:-1]) % 8 == 0:
            index = '8'
        else:
            index = str(int(sheet[:-1]) % 8)

    if sheet[-1] == 'P':
        image = 'ciss_human_passenger_legend_CAB.jpg'
        person = 'Passenger'

    a['Image'] = image
    a['Person'] = person
    a['Index'] = index
    a['CarNum'] = carNum
    a['Case'] = getCase(simData)
    return a