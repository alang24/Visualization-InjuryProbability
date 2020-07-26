
def chooseMax(threeT):
    sorted = threeT.sort_values(by='Prob', ascending=False)
    return sorted.iloc[0].Name


def getName(row, simData, case):
    bodypart = row['BodyPart']

    if bodypart == 'Head':
        one = simData[simData.Name.str.contains('(?:HIC36|BrIC MPS) \(AIS 2\+\)')]
        newname = chooseMax(one)
    elif bodypart == 'Thorax' and case >= 2:
        one = simData[simData.Name.str.contains('Thorax (?:Rmax|PCA) \(AIS 3\+\)')]
        newname = chooseMax(one)

    elif bodypart == 'Tibia Right' and case < 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI|Proximal) Right \(AIS 2\+\)')]
        newname = chooseMax(one)

    elif bodypart == 'Tibia Left' and case < 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI|Proximal) Left \(AIS 2\+\)')]
        newname = chooseMax(one)

    elif bodypart == 'Tibia Right' and case == 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI Right \(AIS 2\+\)|Proximal Right \(AIS 2\+\)|Bending Right)')]
        newname = chooseMax(one)

    elif bodypart == 'Tibia Left' and case == 4:
        one = simData[simData.Name.str.contains('Tibia (?:RTI Left \(AIS 2\+\)|Proximal Left \(AIS 2\+\)|Bending Left)')]
        newname = chooseMax(one)

    elif bodypart == 'Femur Right' and case == 4:
        one = simData[simData.Name.str.contains('Femur (?:Bending Right|Right \(AIS 2\+\))')]
        newname = chooseMax(one)

    elif bodypart == 'Femur Left' and case == 4:
        one = simData[simData.Name.str.contains('Femur (?:Bending Left|Left \(AIS 2\+\))')]
        newname = chooseMax(one)
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