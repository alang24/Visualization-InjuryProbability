# Allen Lang
# Updated: August 2020
# https://github.com/alang24/Injury-Visualization


def colorPicker(row):
    """
    colorPicker is a function that is applied across a DataFrame (circle or ellipse) along axis = 1, so each entry
    is a row. It takes in a row and finds its probability value. Based on that value, a tuple of rgb values is returned.
    Body parts not included in that certain case will be colored white. Severe injury risks are red/reddish while less
    severe risks are green/greenish.

    :param row: a row in the combined DataFrame. Among other things, it will have a value for injury probability
    :return: a rgb tuple with the specified color
    """
    prob = row['Prob']

    # Green
    if 0 <= prob < 10:
        rgb = (0, 255, 0)
    # Light Green
    elif 10 <= prob < 20:
        rgb = (150, 255, 0)
    # Yellow
    elif 20 <= prob < 30:
        rgb = (255, 255, 0)
    # Orange Yellow
    elif 30 <= prob < 40:
        rgb = (255, 190, 0)
    # Orange
    elif 40 <= prob < 50:
        rgb = (255, 255//2, 0)
    # Red
    elif 50 <= prob <= 100:
        rgb = (255, 0, 0)
    # White
    else:
        rgb = (255, 255, 255)
    return rgb
