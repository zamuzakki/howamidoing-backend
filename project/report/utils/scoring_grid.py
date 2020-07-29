def color_score_km_grid(user_report=0, population=1, color="green"):
    """
    color scoring km_grid based on count of a color

    ::params::
    user_report : count report of a color in grid
    population_1 : number of ppulation in grid
    color : color code of status (green, yellow, red)

    ::params type::
    user_report : integer
    population_1 : integer
    color : string

    ::return ::
    score : score for the color

    ::return type :: integer
    """
    if population == 0:
        population = 1
    weight = {'green': 1, 'yellow': 2, 'red': 5}
    score = (1 / population) * (weight.get(color, '1') * user_report)
    return score

def status_score_km_grid(
        user_report_green=0,
        user_report_yellow=0,
        user_report_red=0,
        population=1,
        error_allowed=0.0,
        estimated_respondent=0.1):
    """
    scoring km_grid based on count of user report

    ::params::
    user_report_green : count of green report in grid
    user_report_yellow : count of yellow report in grid
    user_report_red : count of red report in grid
    population : number of ppulation in grid
    error_allowed : minimum percentage respondent of population_1 required
    estimated_respondent : estimated percentage respondent of population_1

    ::params type::
    user_report_green : integer
    user_report_yellow : integer
    user_report_red : integer
    populaton : integer
    error_allowed : float
    estimated_respondent : float

    ::return :: status km_grid
    0: green status
    1: yellow status
    2: red status

    return type :: integer
    """
    if population == 0:
        population = 1
    number_of_sample = user_report_green + user_report_yellow + user_report_red

    if population <= 0:
        return 0

    if number_of_sample < population * error_allowed:
        return 0

    if not user_report_yellow and not user_report_red:
        return 0

    score = color_score_km_grid(user_report_red, population, 'red') \
        + color_score_km_grid(user_report_yellow, population, 'yellow') \
        - color_score_km_grid(user_report_green, population, 'green')

    max_score_estimated = (1 / population) * (5 * estimated_respondent * population)
    min_score_estimated = (1 / population) * (-1 * estimated_respondent * population)

    # setpoint red zone
    setpoint_red_zone = (1 / 3) * (max_score_estimated - min_score_estimated)

    if score < setpoint_red_zone:
        status_score = 1
    else:
        status_score = 2

    return status_score
