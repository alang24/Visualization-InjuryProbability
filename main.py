from PIL import Image,ImageDraw
import pandas as pd
from colorPicker import *
from linkTables import *
from drawShapes import *

coordCirc = pd.read_excel('coord.xlsx',sheet_name=0)
coordEll = pd.read_excel('coord.xlsx',sheet_name=1)

simData = pd.read_excel('simulation_results/Guardrail_injury_analysis.xlsx', sheet_name=1, header=None, names=['Name', 'Fill', 'Prob'])

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


coordCirc['NewName'] = coordCirc.apply(getName, axis=1, args=(simData,case))
coordCirc['Prob'] = coordCirc.apply(getProb, axis=1, args=(simData,))
#coordCirc['Color'] = coordCirc.apply(colorPicker, axis=1)

coordEll['NewName'] = coordEll.apply(getName, axis=1, args=(simData,case))
coordEll['Prob'] = coordEll.apply(getProb, axis=1, args=(simData,))
#coordEll['Color'] = coordEll.apply(colorPicker, axis=1)

print(coordCirc)
print(coordEll)

#
# with Image.open('ciss_human_driver_legend_CAB.jpg') as im:
#     drawer = ImageDraw.Draw(im)
#     coordCirc.apply(drawCircle,axis=1,args=(drawer,))
#     coordEll.apply(drawEllipse,axis=1,args=(drawer,))
#     im.save('pepega.jpg')

