from PIL import Image,ImageDraw
import pandas as pd
from colorPicker import colorPicker
from linkTables import *

coord = pd.read_excel('coord.xlsx')
simData = pd.read_excel('simulation_results/Guardrail_injury_analysis.xlsx', sheet_name=0, header=None, names=['Name', 'Fill', 'Prob'])

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


coord['NewName'] = coord.apply(getName,axis=1,args=(simData,))
coord['Prob'] = coord.apply(getProb,axis=1,args=(simData,))

#coord['Color'] = coord.loc[:, 'Prob'].map(colorPicker)

print(coord)

#im = Image.open('ciss_human_driver_legend_CAB.jpg')

#im.save('pepega.jpg')

