from PIL import Image,ImageDraw
import pandas as pd
from colorPicker import colorPicker
coord = pd.read_excel('coord.xlsx')
simData = pd.read_excel('simulation_results/Guardrail_injury_analysis.xlsx', sheet_name=0, header=None, names=['Name', 'Fill', 'Prob'])

#coord = coord.set_index("BodyPart")
#simData = simData.set_index("Name")
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


def typo(bodypart):
    if bodypart == 'Head':
        one = simData[simData.Name.str.contains('(?:HIC36|BrIC MPS) \(AIS 2\+\)')]
        if one.iloc[0].Prob > one.iloc[1].Prob:
            bleh = one.iloc[0].Name
        else:
            bleh = one.iloc[1].Name
    else:
        foundAny = simData.Name.str.contains(bodypart)
        if not foundAny.any():
            return "Not Found"
        bleh = simData[foundAny].iloc[0].Name
    return bleh

def typo2(bodypart):
    if bodypart == 'Not Found':
        return -1
    else:
        return simData[simData.Name == bodypart].iloc[0].Prob * 100


coord.insert(len(coord.columns),'NewName',coord.BodyPart.map(typo))
coord.insert(len(coord.columns),'Prob',coord.loc[:,'NewName'].map(typo2))
coord.insert(len(coord.columns),'Color',coord.loc[:,'Prob'].map(colorPicker))

print(coord)

#im = Image.open('ciss_human_driver_legend_CAB.jpg')

#im.save('pepega.jpg')

