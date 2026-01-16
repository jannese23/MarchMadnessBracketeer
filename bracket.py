def compare_brackets(predicted, real):
    for matchup in real.keys():
        return predicted[matchup][0] == real[matchup][0], predicted[matchup][1], real[matchup][1]

def create_empty_bracket():
    """
    Creates an empty bracket structure.

    :returns:
        dict: An empty bracket with all matchups set to None.
    """
    pass