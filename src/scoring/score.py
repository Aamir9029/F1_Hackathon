"""
Scoring functions for each level of the Entelect Grand Prix.

Formulas are taken directly from the problem statement:

Level 1:
    base_score = 500_000 * (time_reference_s / total_race_time) ^ 3

Level 2 & 3:
    base_score  = 500_000 * (time_reference_s / total_race_time) ^ 3
    fuel_bonus  = -500_000 * (1 - fuel_used / fuel_soft_cap_limit_l) ^ 2 + 500_000
    final_score = base_score + fuel_bonus

Level 4:
    base_score  = 500_000 * (time_reference_s / total_race_time) ^ 3
    fuel_bonus  = -500_000 * (1 - fuel_used / fuel_soft_cap_limit_l) ^ 2 + 500_000
    tyre_bonus  = 100_000 * sum(tyre_degradation) - 50_000 * number_of_blowouts
    final_score = base_score + tyre_bonus + fuel_bonus
"""


def calculate_base_score(time_reference_s: float, total_race_time: float) -> float:
    """
    Calculates the base score used by all levels.

    Formula: 500_000 * (time_reference_s / total_race_time) ^ 3

    Args:
        time_reference_s: The reference time for the level (from JSON).
        total_race_time:  The total simulated race time in seconds.

    Returns:
        The base score as a float.
    """
    if total_race_time <= 0:
        return 0.0
    return 500_000 * (time_reference_s / total_race_time) ** 3


def calculate_fuel_bonus(fuel_used: float, fuel_soft_cap_limit_l: float) -> float:
    """
    Calculates the fuel efficiency bonus used by Levels 2, 3, and 4.

    Formula: -500_000 * (1 - fuel_used / fuel_soft_cap_limit_l) ^ 2 + 500_000

    The bonus rewards using fuel close to (but not over) the soft cap.
    - Using exactly the soft cap amount gives the maximum bonus of 500_000.
    - Using more than the soft cap causes the bonus to decrease.
    - Using much less than the soft cap also results in a lower bonus.

    Args:
        fuel_used:             Total fuel consumed during the race (litres).
        fuel_soft_cap_limit_l: The soft cap fuel limit from the JSON.

    Returns:
        The fuel bonus as a float.
    """
    if fuel_soft_cap_limit_l <= 0:
        return 0.0
    return -500_000 * (1 - fuel_used / fuel_soft_cap_limit_l) ** 2 + 500_000


def calculate_tyre_bonus(total_tyre_degradation: float, number_of_blowouts: int) -> float:
    """
    Calculates the tyre usage bonus used by Level 4.

    Formula: 100_000 * sum(tyre_degradation) - 50_000 * number_of_blowouts

    The bonus rewards using as much tyre life as possible (high degradation)
    while penalising blowouts heavily.

    Args:
        total_tyre_degradation: The sum of all accumulated tyre degradation
                                across every tyre set used during the race.
        number_of_blowouts:     The total number of tyre blowouts during the race.

    Returns:
        The tyre bonus as a float.
    """
    return 100_000 * total_tyre_degradation - 50_000 * number_of_blowouts


# --- Public per-level functions ---

def calculate_level1_score(time_reference_s: float, total_race_time: float) -> float:
    """
    Level 1 scoring — speed only.

    Args:
        time_reference_s: Reference time from the level JSON.
        total_race_time:  Your simulated total race time (seconds).

    Returns:
        The final Level 1 score.
    """
    return calculate_base_score(time_reference_s, total_race_time)


def calculate_level2_score(
    time_reference_s: float,
    total_race_time: float,
    fuel_used: float,
    fuel_soft_cap_limit_l: float
) -> float:
    """
    Level 2 scoring — speed + fuel management.

    Args:
        time_reference_s:      Reference time from the level JSON.
        total_race_time:       Your simulated total race time (seconds).
        fuel_used:             Total fuel consumed (litres).
        fuel_soft_cap_limit_l: Fuel soft cap from the level JSON.

    Returns:
        The final Level 2 score.
    """
    base = calculate_base_score(time_reference_s, total_race_time)
    fuel = calculate_fuel_bonus(fuel_used, fuel_soft_cap_limit_l)
    return base + fuel


def calculate_level3_score(
    time_reference_s: float,
    total_race_time: float,
    fuel_used: float,
    fuel_soft_cap_limit_l: float
) -> float:
    """
    Level 3 scoring — speed + fuel + weather (same formula as Level 2).

    Args:
        time_reference_s:      Reference time from the level JSON.
        total_race_time:       Your simulated total race time (seconds).
        fuel_used:             Total fuel consumed (litres).
        fuel_soft_cap_limit_l: Fuel soft cap from the level JSON.

    Returns:
        The final Level 3 score.
    """
    base = calculate_base_score(time_reference_s, total_race_time)
    fuel = calculate_fuel_bonus(fuel_used, fuel_soft_cap_limit_l)
    return base + fuel


def calculate_level4_score(
    time_reference_s: float,
    total_race_time: float,
    fuel_used: float,
    fuel_soft_cap_limit_l: float,
    total_tyre_degradation: float,
    number_of_blowouts: int
) -> float:
    """
    Level 4 scoring — speed + fuel + tyre degradation management.

    Args:
        time_reference_s:       Reference time from the level JSON.
        total_race_time:        Your simulated total race time (seconds).
        fuel_used:              Total fuel consumed (litres).
        fuel_soft_cap_limit_l:  Fuel soft cap from the level JSON.
        total_tyre_degradation: Sum of degradation across all tyre sets used.
        number_of_blowouts:     Number of tyre blowouts during the race.

    Returns:
        The final Level 4 score.
    """
    base = calculate_base_score(time_reference_s, total_race_time)
    fuel = calculate_fuel_bonus(fuel_used, fuel_soft_cap_limit_l)
    tyre = calculate_tyre_bonus(total_tyre_degradation, number_of_blowouts)
    return base + fuel + tyre
