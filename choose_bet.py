def choose_bet(home_vegas_line, home_model_line, away_vegas_line, away_model_line):
    # set standard bet unit here
    bet_unit = 10

    # if site provides EVEN as bet line, then change to standard 100
    if home_vegas_line == 'EVEN':
        home_vegas_line = 100
    if away_vegas_line == 'EVEN':
        away_vegas_line = 100

    # return appropriate bet statistics based on model vs vegas
    if home_model_line < 0:
        home_model_line *= -1
        home_vegas_line *= -1
        if (home_model_line <= home_vegas_line) & (away_model_line >= away_vegas_line):
            return "NO BET", "None", "None", 0
        elif (home_model_line > home_vegas_line) & (away_model_line > away_vegas_line):
            return "HOME", "Favorite", home_model_line - home_vegas_line, (home_vegas_line * -1) / (100/bet_unit)
        elif (home_model_line < home_vegas_line) & (away_model_line < away_vegas_line):
            return "AWAY", "Dog", away_vegas_line - away_model_line, bet_unit
    else:
        away_model_line *= -1
        away_vegas_line *= -1
        if (home_model_line >= home_vegas_line) & (away_model_line <= away_vegas_line):
            return "NO BET", "None", "None", 0
        elif (home_model_line > home_vegas_line) & (away_model_line > away_vegas_line):
            return "AWAY", "Favorite", away_model_line - away_vegas_line, (away_vegas_line * -1) / (100/bet_unit)
        elif (home_model_line < home_vegas_line) & (away_model_line < away_vegas_line):
            return "HOME", "Dog", home_vegas_line - home_model_line, bet_unit
