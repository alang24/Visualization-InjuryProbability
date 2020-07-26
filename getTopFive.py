import pandas as pd


def getTopFive(circ,ell):
    a = circ.loc[:, ['NewName', 'Prob']]
    b = ell.loc[:, ['NewName', 'Prob']]

    combined = pd.concat([a, b]).sort_values(by='Prob', ascending=False)

    return combined.iloc[0:5]