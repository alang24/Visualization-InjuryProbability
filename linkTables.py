
def chooseFromTwo(twoT):
    if twoT.iloc[0].Prob > twoT.iloc[1].Prob:
        return twoT.iloc[0].Name
    else:
        return twoT.iloc[1].Name

def getName(row, simData, case):
    bodypart = row['BodyPart']

    if bodypart == 'Head':
        one = simData[simData.Name.str.contains('(?:HIC36|BrIC MPS) \(AIS 2\+\)')]
        newname = chooseFromTwo(one)
    elif bodypart == 'Thorax' and case >= 2:
        one = simData[simData.Name.str.contains('Thorax (?:Rmax|PCA) \(AIS 3\+\)')]
        newname = chooseFromTwo(one)

    elif bodypart == 'Tibia Right' and case < 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI|Proximal) Right \(AIS 2\+\)')]
        newname = chooseFromTwo(one)

    elif bodypart == 'Tibia Left' and case < 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI|Proximal) Left \(AIS 2\+\)')]
        newname = chooseFromTwo(one)

    else:
        foundAny = simData.Name.str.contains(bodypart)
        if not foundAny.any():
            return "Not Found"
        newname = simData[foundAny].iloc[0].Name
    return newname


def getProb(row,simData):
    bodypart = row['NewName']

    if bodypart == 'Not Found':
        return -1
    else:
        return simData[simData.Name == bodypart].iloc[0].Prob * 100