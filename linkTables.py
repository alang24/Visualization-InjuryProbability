def getName(row,simData):
    bodypart = row['BodyPart']
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


def getProb(row,simData):
    bodypart = row['NewName']

    if bodypart == 'Not Found':
        return -1
    else:
        return simData[simData.Name == bodypart].iloc[0].Prob * 100