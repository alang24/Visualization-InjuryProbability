# Allen Lang
# Updated: August 2020
# https://github.com/alang24/Injury-Visualization


def chooseMax(threeT):
    """
    chooseMax is a helper function to getName, takes in a DataFrame of 2 or 3 rows and returns the name of the one
    that has the highest probability.

    :param threeT: DataFrame of 2 or 3 bodyparts
    :return: Name of bodypart of highest probability
    """
    sorted = threeT.sort_values(by='Prob', ascending=False)
    return sorted.iloc[0].Name


def getName(row, simData, case):
    """
    getName is applied across the coord DataFrame, which has all possible bodyparts. It will find said bodypart in the
    simulationresults DataFrame. If it does not, then that case doesn't have that bodypart, and a "not found" name will
    be returned. It takes in case number to sift through the multiple exception cases, taking advantage of the Regex
    built into the pandas str functions.

    :param row: a row in the DataFrame, circle or ellipse
    :param simData: simulation Data with results, need it for the more scientific body part name
    :param case: four possible cases lead to four possible sets of bodyparts that need to be drawn
    :return: the proper name of the property that should be used
    """
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
    """
    getProb follows after getName, extracting the Prob by looking back into simData for that exact name

    :param row: bodypart either from ellipse or circle DataFrame
    :param simData: simulation data that contains probabilities
    :return: the probability as a percentage
    """
    bodypart = row['NewName']

    if bodypart == 'Not Found':
        return -1
    else:
        return simData[simData.Name == bodypart].iloc[0].Prob * 100