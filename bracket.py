def compare_brackets(predicted, real):
    correct = 0
    for matchup in real.keys():
        return predicted[matchup][0] == real[matchup][0], predicted[matchup][1], real[matchup][1]
    
def input_bracket(makeFullBracket):
    inputText = "Enter year of March Madness Tournament in YYYY format, e.g. 2023-2024 season is 2024: "
    while True:
        year = input(inputText)
        if year.isdigit() and len(year) == 4:
            print(f"Creating bracket for March Madness {year}")
            break
        else:
            inputText = "Invalid Input, try again: "

    regions = ["South", "East", "Midwest", "West"]
    setup = ["East", "Midwest", "West"]
    stages = ["Baseline", "Round of 64", "Round of 32", "Sweet Sixteen", "Elite Eight", "Final Four", "Championship"]
    bracket = create_empty_bracket()

    inputText = "Enter South region Final Four region matchup (East, Midwest, West): "
    while True:
        southMatchup = input(inputText).title()
        if southMatchup in regions and southMatchup != "South":
            setup.remove(southMatchup)
            break
        else:
            inputText = "Invalid input, try again: "
    
    #inputText = "Input just the round of 64? (Y/N): "
    #while True:
    #    answer = input(inputText).upper()
    #    if answer == "Y" or answer == "N":
    #        break
    #    else:
    #        inputText = "Invalid input, try again: "

    for region in regions:
        oneSeed = take_valid_name_input(f"{region} 1 seed: ")
        sixtnSeed = take_valid_name_input(f"{region} 16 seed: ")
        bracket[region]["1-16"] = {"1": oneSeed, "16": sixtnSeed} 
    
    print(bracket)

    if makeFullBracket:
        pass
    
def take_valid_name_input(question):
    while True:
        answer = input(question)
        if len(answer) > 6:
            question = "Invalid input, try again: "
        else:
            break
    
    output = answer.upper().center(6)

    return output

def commit_bracket_to_db():
    pass

def create_empty_bracket():
    """
    Creates an empty bracket structure.

    :returns:
        dict: A bracket with the 4 regions empty.
    """
    bracket = dict()
    bracket["Champion"] = None
    South, East, Midwest, West = dict(), dict(), dict(), dict()
    bracket["South"], bracket["East"], bracket["Midwest"], bracket["West"] = South, East, Midwest, West
    return bracket
        

def create_unsimulated_bracket(bracket):
    blank = create_empty_bracket()
    pass

def print_bracket():
    XXXXXX = "UCONN "
    bracket = f"""
        ███████╗ ██████╗ ██╗   ██╗████████╗██╗  ██╗
        ██╔════╝██╔═══██╗██║   ██║╚══██╔══╝██║  ██║
        ███████╗██║   ██║██║   ██║   ██║   ███████║
        ╚════██║██║   ██║██║   ██║   ██║   ██╔══██║
        ███████║╚██████╔╝╚██████╔╝   ██║   ██║  ██║
        ╚══════╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [{XXXXXX}]══╗      │            │            │            │
              ╠══[{XXXXXX}]══╗      │            │            │
    [{XXXXXX}]══╝            ║      │            │            │
                           ╠══[{XXXXXX}]══╗      │            │
    [{XXXXXX}]══╗            ║            ║      │            │
              ╠══[{XXXXXX}]══╝            ║      │            │
    [{XXXXXX}]══╝                         ║      │            │
                                        ╠══[{XXXXXX}]══╗      │
    [{XXXXXX}]══╗                         ║            ║      │
              ╠══[{XXXXXX}]══╗            ║            ║      │
    [{XXXXXX}]══╝            ║            ║            ║      │
                           ╠══[{XXXXXX}]══╝            ║      │
    [{XXXXXX}]══╗            ║                         ║      │
              ╠══[{XXXXXX}]══╝                         ║      │
    [{XXXXXX}]══╝                                      ║      │
                                                     ╠══[{XXXXXX}]
    [{XXXXXX}]══╗                                      ║
              ╠══[{XXXXXX}]══╗                         ║
    [{XXXXXX}]══╝            ║                         ║
                           ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╗            ║            ║            ║
              ╠══[{XXXXXX}]══╝            ║            ║
    [{XXXXXX}]══╝                         ║            ║
                                        ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗                         ║
              ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╝            ║            ║
                           ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗            ║
              ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╝

        ███████╗ █████╗ ███████╗████████╗
        ██╔════╝██╔══██╗██╔════╝╚══██╔══╝
        █████╗  ███████║███████╗   ██║   
        ██╔══╝  ██╔══██║╚════██║   ██║   
        ███████╗██║  ██║███████║   ██║   
        ╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [{XXXXXX}]══╗      │            │            │            │
              ╠══[{XXXXXX}]══╗      │            │            │
    [{XXXXXX}]══╝            ║      │            │            │
                           ╠══[{XXXXXX}]══╗      │            │
    [{XXXXXX}]══╗            ║            ║      │            │
              ╠══[{XXXXXX}]══╝            ║      │            │
    [{XXXXXX}]══╝                         ║      │            │
                                        ╠══[{XXXXXX}]══╗      │
    [{XXXXXX}]══╗                         ║            ║      │
              ╠══[{XXXXXX}]══╗            ║            ║      │
    [{XXXXXX}]══╝            ║            ║            ║      │
                           ╠══[{XXXXXX}]══╝            ║      │
    [{XXXXXX}]══╗            ║                         ║      │
              ╠══[{XXXXXX}]══╝                         ║      │
    [{XXXXXX}]══╝                                      ║      │
                                                     ╠══[{XXXXXX}]
    [{XXXXXX}]══╗                                      ║
              ╠══[{XXXXXX}]══╗                         ║
    [{XXXXXX}]══╝            ║                         ║
                           ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╗            ║            ║            ║
              ╠══[{XXXXXX}]══╝            ║            ║
    [{XXXXXX}]══╝                         ║            ║
                                        ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗                         ║
              ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╝            ║            ║
                           ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗            ║
              ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╝

        ███╗   ███╗██╗██████╗ ██╗    ██╗███████╗███████╗████████╗
        ████╗ ████║██║██╔══██╗██║    ██║██╔════╝██╔════╝╚══██╔══╝
        ██╔████╔██║██║██║  ██║██║ █╗ ██║█████╗  ███████╗   ██║   
        ██║╚██╔╝██║██║██║  ██║██║███╗██║██╔══╝  ╚════██║   ██║   
        ██║ ╚═╝ ██║██║██████╔╝╚███╔███╔╝███████╗███████║   ██║   
        ╚═╝     ╚═╝╚═╝╚═════╝  ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [{XXXXXX}]══╗      │            │            │            │
              ╠══[{XXXXXX}]══╗      │            │            │
    [{XXXXXX}]══╝            ║      │            │            │
                           ╠══[{XXXXXX}]══╗      │            │
    [{XXXXXX}]══╗            ║            ║      │            │
              ╠══[{XXXXXX}]══╝            ║      │            │
    [{XXXXXX}]══╝                         ║      │            │
                                        ╠══[{XXXXXX}]══╗      │
    [{XXXXXX}]══╗                         ║            ║      │
              ╠══[{XXXXXX}]══╗            ║            ║      │
    [{XXXXXX}]══╝            ║            ║            ║      │
                           ╠══[{XXXXXX}]══╝            ║      │
    [{XXXXXX}]══╗            ║                         ║      │
              ╠══[{XXXXXX}]══╝                         ║      │
    [{XXXXXX}]══╝                                      ║      │
                                                     ╠══[{XXXXXX}]
    [{XXXXXX}]══╗                                      ║
              ╠══[{XXXXXX}]══╗                         ║
    [{XXXXXX}]══╝            ║                         ║
                           ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╗            ║            ║            ║
              ╠══[{XXXXXX}]══╝            ║            ║
    [{XXXXXX}]══╝                         ║            ║
                                        ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗                         ║
              ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╝            ║            ║
                           ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗            ║
              ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╝

        ██╗    ██╗███████╗███████╗████████╗
        ██║    ██║██╔════╝██╔════╝╚══██╔══╝
        ██║ █╗ ██║█████╗  ███████╗   ██║   
        ██║███╗██║██╔══╝  ╚════██║   ██║   
        ╚███╔███╔╝███████╗███████║   ██║   
        ╚══╝╚══╝ ╚══════╝╚══════╝   ╚═╝   

    [R.o.64]     [R.o.32]     [Swt 16]     [Elit 8]     [Fina 4]
        │            │            │            │            │
    [{XXXXXX}]══╗      │            │            │            │
              ╠══[{XXXXXX}]══╗      │            │            │
    [{XXXXXX}]══╝            ║      │            │            │
                           ╠══[{XXXXXX}]══╗      │            │
    [{XXXXXX}]══╗            ║            ║      │            │
              ╠══[{XXXXXX}]══╝            ║      │            │
    [{XXXXXX}]══╝                         ║      │            │
                                        ╠══[{XXXXXX}]══╗      │
    [{XXXXXX}]══╗                         ║            ║      │
              ╠══[{XXXXXX}]══╗            ║            ║      │
    [{XXXXXX}]══╝            ║            ║            ║      │
                           ╠══[{XXXXXX}]══╝            ║      │
    [{XXXXXX}]══╗            ║                         ║      │
              ╠══[{XXXXXX}]══╝                         ║      │
    [{XXXXXX}]══╝                                      ║      │
                                                     ╠══[{XXXXXX}]
    [{XXXXXX}]══╗                                      ║
              ╠══[{XXXXXX}]══╗                         ║
    [{XXXXXX}]══╝            ║                         ║
                           ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╗            ║            ║            ║
              ╠══[{XXXXXX}]══╝            ║            ║
    [{XXXXXX}]══╝                         ║            ║
                                        ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗                         ║
              ╠══[{XXXXXX}]══╗            ║
    [{XXXXXX}]══╝            ║            ║
                           ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╗            ║
              ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╝

        ███████╗██╗███╗   ██╗ █████╗ ██╗         ███████╗ ██████╗ ██╗   ██╗██████╗ 
        ██╔════╝██║████╗  ██║██╔══██╗██║         ██╔════╝██╔═══██╗██║   ██║██╔══██╗
        █████╗  ██║██╔██╗ ██║███████║██║         █████╗  ██║   ██║██║   ██║██████╔╝
        ██╔══╝  ██║██║╚██╗██║██╔══██║██║         ██╔══╝  ██║   ██║██║   ██║██╔══██╗
        ██║     ██║██║ ╚████║██║  ██║███████╗    ██║     ╚██████╔╝╚██████╔╝██║  ██║
        ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝      ╚═════╝  ╚═════╝ ╚═╝  ╚═╝

    [Fina 4]     [Chip Gm]     [Champs]
        │            │            │
    [{XXXXXX}]══╗      │            │
              ╠══[{XXXXXX}]══╗      │
    [{XXXXXX}]══╝            ║      │
                           ╠══[{XXXXXX}]
    [{XXXXXX}]══╗            ║
              ╠══[{XXXXXX}]══╝
    [{XXXXXX}]══╝"""
    print(bracket)

if __name__ == "__main__":
    input_bracket(False)