def compare_brackets(predicted, real):
    for matchup in real.keys():
        return predicted[matchup][0] == real[matchup][0], predicted[matchup][1], real[matchup][1]
    
def input_bracket():
    regions = ["South, East, Midwest, West"]
    stages = ["Baseline", "Round of 64", "Round of 32", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship"]
    bracket = create_empty_bracket()

def commit_bracket_to_db():
    pass

def create_empty_bracket():
    """
    Creates an empty bracket structure.

    :returns:
        dict: An empty bracket with all matchups set to None.
    """

    pass

def create_unsimulated_bracket(bracket):
    blank = create_empty_bracket()
    pass

def print_bracket():
    bracket = """
        ███████╗ ██████╗ ██╗   ██╗████████╗██╗  ██╗
        ██╔════╝██╔═══██╗██║   ██║╚══██╔══╝██║  ██║
        ███████╗██║   ██║██║   ██║   ██║   ███████║
        ╚════██║██║   ██║██║   ██║   ██║   ██╔══██║
        ███████║╚██████╔╝╚██████╔╝   ██║   ██║  ██║
        ╚══════╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [XXXXXX]══╗      │            │            │            │
              ╠══[XXXXXX]══╗      │            │            │
    [XXXXXX]══╝            ║      │            │            │
                           ╠══[XXXXXX]══╗      │            │
    [XXXXXX]══╗            ║            ║      │            │
              ╠══[XXXXXX]══╝            ║      │            │
    [XXXXXX]══╝                         ║      │            │
                                        ╠══[XXXXXX]══╗      │
    [XXXXXX]══╗                         ║            ║      │
              ╠══[XXXXXX]══╗            ║            ║      │
    [XXXXXX]══╝            ║            ║            ║      │
                           ╠══[XXXXXX]══╝            ║      │
    [XXXXXX]══╗            ║                         ║      │
              ╠══[XXXXXX]══╝                         ║      │
    [XXXXXX]══╝                                      ║      │
                                                     ╠══[XXXXXX]
    [XXXXXX]══╗                                      ║
              ╠══[XXXXXX]══╗                         ║
    [XXXXXX]══╝            ║                         ║
                           ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╗            ║            ║            ║
              ╠══[XXXXXX]══╝            ║            ║
    [XXXXXX]══╝                         ║            ║
                                        ╠══[XXXXXX]══╝
    [XXXXXX]══╗                         ║
              ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╝            ║            ║
                           ╠══[XXXXXX]══╝
    [XXXXXX]══╗            ║
              ╠══[XXXXXX]══╝
    [XXXXXX]══╝

        ███████╗ █████╗ ███████╗████████╗
        ██╔════╝██╔══██╗██╔════╝╚══██╔══╝
        █████╗  ███████║███████╗   ██║   
        ██╔══╝  ██╔══██║╚════██║   ██║   
        ███████╗██║  ██║███████║   ██║   
        ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [XXXXXX]══╗      │            │            │            │
              ╠══[XXXXXX]══╗      │            │            │
    [XXXXXX]══╝            ║      │            │            │
                           ╠══[XXXXXX]══╗      │            │
    [XXXXXX]══╗            ║            ║      │            │
              ╠══[XXXXXX]══╝            ║      │            │
    [XXXXXX]══╝                         ║      │            │
                                        ╠══[XXXXXX]══╗      │
    [XXXXXX]══╗                         ║            ║      │
              ╠══[XXXXXX]══╗            ║            ║      │
    [XXXXXX]══╝            ║            ║            ║      │
                           ╠══[XXXXXX]══╝            ║      │
    [XXXXXX]══╗            ║                         ║      │
              ╠══[XXXXXX]══╝                         ║      │
    [XXXXXX]══╝                                      ║      │
                                                     ╠══[XXXXXX]
    [XXXXXX]══╗                                      ║
              ╠══[XXXXXX]══╗                         ║
    [XXXXXX]══╝            ║                         ║
                           ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╗            ║            ║            ║
              ╠══[XXXXXX]══╝            ║            ║
    [XXXXXX]══╝                         ║            ║
                                        ╠══[XXXXXX]══╝
    [XXXXXX]══╗                         ║
              ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╝            ║            ║
                           ╠══[XXXXXX]══╝
    [XXXXXX]══╗            ║
              ╠══[XXXXXX]══╝
    [XXXXXX]══╝

        ███╗   ███╗██╗██████╗ ██╗    ██╗███████╗███████╗████████╗
        ████╗ ████║██║██╔══██╗██║    ██║██╔════╝██╔════╝╚══██╔══╝
        ██╔████╔██║██║██║  ██║██║ █╗ ██║█████╗  ███████╗   ██║   
        ██║╚██╔╝██║██║██║  ██║██║███╗██║██╔══╝  ╚════██║   ██║   
        ██║ ╚═╝ ██║██║██████╔╝╚███╔███╔╝███████╗███████║   ██║   
        ╚═╝     ╚═╝╚═╝╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [XXXXXX]══╗      │            │            │            │
              ╠══[XXXXXX]══╗      │            │            │
    [XXXXXX]══╝            ║      │            │            │
                           ╠══[XXXXXX]══╗      │            │
    [XXXXXX]══╗            ║            ║      │            │
              ╠══[XXXXXX]══╝            ║      │            │
    [XXXXXX]══╝                         ║      │            │
                                        ╠══[XXXXXX]══╗      │
    [XXXXXX]══╗                         ║            ║      │
              ╠══[XXXXXX]══╗            ║            ║      │
    [XXXXXX]══╝            ║            ║            ║      │
                           ╠══[XXXXXX]══╝            ║      │
    [XXXXXX]══╗            ║                         ║      │
              ╠══[XXXXXX]══╝                         ║      │
    [XXXXXX]══╝                                      ║      │
                                                     ╠══[XXXXXX]
    [XXXXXX]══╗                                      ║
              ╠══[XXXXXX]══╗                         ║
    [XXXXXX]══╝            ║                         ║
                           ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╗            ║            ║            ║
              ╠══[XXXXXX]══╝            ║            ║
    [XXXXXX]══╝                         ║            ║
                                        ╠══[XXXXXX]══╝
    [XXXXXX]══╗                         ║
              ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╝            ║            ║
                           ╠══[XXXXXX]══╝
    [XXXXXX]══╗            ║
              ╠══[XXXXXX]══╝
    [XXXXXX]══╝

        ██╗    ██╗███████╗███████╗████████╗
        ██║    ██║██╔════╝██╔════╝╚══██╔══╝
        ██║ █╗ ██║█████╗  ███████╗   ██║   
        ██║███╗██║██╔══╝  ╚════██║   ██║   
        ╚███╔███╔╝███████╗███████║   ██║   
        ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [XXXXXX]══╗      │            │            │            │
              ╠══[XXXXXX]══╗      │            │            │
    [XXXXXX]══╝            ║      │            │            │
                           ╠══[XXXXXX]══╗      │            │
    [XXXXXX]══╗            ║            ║      │            │
              ╠══[XXXXXX]══╝            ║      │            │
    [XXXXXX]══╝                         ║      │            │
                                        ╠══[XXXXXX]══╗      │
    [XXXXXX]══╗                         ║            ║      │
              ╠══[XXXXXX]══╗            ║            ║      │
    [XXXXXX]══╝            ║            ║            ║      │
                           ╠══[XXXXXX]══╝            ║      │
    [XXXXXX]══╗            ║                         ║      │
              ╠══[XXXXXX]══╝                         ║      │
    [XXXXXX]══╝                                      ║      │
                                                     ╠══[XXXXXX]
    [XXXXXX]══╗                                      ║
              ╠══[XXXXXX]══╗                         ║
    [XXXXXX]══╝            ║                         ║
                           ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╗            ║            ║            ║
              ╠══[XXXXXX]══╝            ║            ║
    [XXXXXX]══╝                         ║            ║
                                        ╠══[XXXXXX]══╝
    [XXXXXX]══╗                         ║
              ╠══[XXXXXX]══╗            ║
    [XXXXXX]══╝            ║            ║
                           ╠══[XXXXXX]══╝
    [XXXXXX]══╗            ║
              ╠══[XXXXXX]══╝
    [XXXXXX]══╝

        ███████╗██╗███╗   ██╗ █████╗ ██╗         ███████╗ ██████╗ ██╗   ██╗██████╗ 
        ██╔════╝██║████╗  ██║██╔══██╗██║         ██╔════╝██╔═══██╗██║   ██║██╔══██╗
        █████╗  ██║██╔██╗ ██║███████║██║         █████╗  ██║   ██║██║   ██║██████╔╝
        ██╔══╝  ██║██║╚██╗██║██╔══██║██║         ██╔══╝  ██║   ██║██║   ██║██╔══██╗
        ██║     ██║██║ ╚████║██║  ██║███████╗    ██║     ╚██████╔╝╚██████╔╝██║  ██║
        ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝

    [Fina 4]     [Chip Gm]     [Champs]
        │            │            │
    [XXXXXX]══╗      │            │
              ╠══[XXXXXX]══╗      │
    [XXXXXX]══╝            ║      │
                           ╠══[XXXXXX]
    [XXXXXX]══╗            ║
              ╠══[XXXXXX]══╝
    [XXXXXX]══╝"""
    print(bracket)

if __name__ == "__main__":
    print_bracket()