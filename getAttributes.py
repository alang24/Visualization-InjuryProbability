# Allen Lang
# Updated: October 2020
# https://github.com/alang24/Injury-Visualization


def getOccupantModel(simData, attr):
    """
    Helper function to get occupant model

    :param simData: simulation data
    :return: case number, refer to simulation_matrix for specifics
    """
    numrows = simData.shape[0]

    if numrows == 52:
        attr['OccName'] = 'H3'
        attr['OccNum'] = 1

    elif numrows == 63:
        attr['OccName'] = 'THOR'
        attr['OccNum'] = 2

    elif numrows == 83:
        attr['OccName'] = 'M50-OS'
        attr['OccNum'] = 3

    elif numrows == 111:
        attr['OccName'] = 'M50-O'
        attr['OccNum'] = 4

    else:
        print("Incorrect number of rows. Something has changed with the table.")
        exit(1)
    return attr


def getAttributes(test_type, sheet, carName, simData):
    """
    Gets information necessary for naming/saving the image

    Image: name of image file to be used (driver or passenger)
    Person: Driver or passenger
    Index: Sheet number within the spreadsheet
    CarName: model of car used
    Carnum: Car number (OverCenterline only)
    OccName: name of occupant dummy model
    OccNum: needed to link tables, value mapped from occupant name

    :param test_type: crash type (Guardrail, MedianStrip, OverCenterline, RoadsideTree)
    :param sheet: sheet name in spreadsheet
    :param carName: model of the car used
    :param simData: simData to count number of rows
    :return:
    """
    a = {}

    # Default assumption that person is a Driver, and no Second Car
    image = 'ciss_human_driver_legend_CAB.jpg'
    person = 'Driver'
    carNum = '-1'

    # Special cases for Guardrail (has only driver) and OverCenterline (has two cars)
    if test_type == 'Guardrail':
        index = sheet
    elif test_type == 'OverCenterline':
        if int(sheet[:-1]) % 2 == 0:
            carNum = '2'
        else:
            carNum = '1'
        index = sheet[:-1]
    else:
        index = sheet[:-1]

    if sheet[-1] == 'P':
        image = 'ciss_human_passenger_legend_CAB.jpg'
        person = 'Passenger'

    a['TestType'] = test_type
    a['Image'] = image
    a['Person'] = person
    a['Index'] = index
    a['CarName'] = carName
    a['CarNum'] = carNum
    a = getOccupantModel(simData, a)
    return a
