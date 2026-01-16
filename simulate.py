from bracket import create_unsimulated_bracket

def simulate(year):
    toSimulate = create_unsimulated_bracket(year)
    for matchup in toSimulate.keys():
        result = simulate_matchup(matchup)

def simulate_matchup(matchup):
    pass

