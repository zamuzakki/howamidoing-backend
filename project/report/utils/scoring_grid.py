def status_score_km_grid(
        user_report_green = 0,
        user_report_yellow = 0,
        user_report_red = 0,
        population = 0,
        error_allowed = 0.0,
        estimated_responden = 0.1
    ):
    """
    scoring km_grid based on count of user report

    ::params::
    user_report_green : count of green report in grid
    user_report_yellow : count of yellow report in grid
    user_report_red : count of red report in grid
    population : number of ppulation in grid
    error_allowed : minimum percentage responden of population required
    estimated_responden : estimated percentage responden of population
    
    ::params type::
    user_report_green : integer 
    user_report_yellow : integer 
    user_report_red : integer 
    populaton : integer 
    error_allowed : float 
    estimated_responden : float

    return :: status km_grid red / yellow / green
    return type :: string
    """
    number_of_sample = user_report_green + user_report_yellow + user_report_red
    
    if population <= 0:
        return 'green'

    if number_of_sample < population * error_allowed:
        return 'green'

    if not user_report_yellow and not user_report_red:
        return 'green'

    score = (1 / population) * \
            ((5 * user_report_red) + (2 * user_report_yellow) - user_report_green)

    max_score_estimated = (1 / population) * (5 * estimated_responden * population)
    min_score_estimated = (1 / population) * (-1 * estimated_responden * population)

    # setpoint red zone
    setpoint_red_zone = (1 / 3) * (max_score_estimated - min_score_estimated)

    if score < setpoint_red_zone:
        status_score = 'yellow'
    else:
        status_score = 'red'
   
    return status_score