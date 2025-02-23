from datetime import datetime
from typing import List

after_28th_corrections = {
    5: 12, 
    6: 5,
    7: 9,
    8: 1
}

def get_adder_for_stage(stage: int, day: int) -> int:
    stage_adders = [0, 8, 12, 4, 1, 9, 13, 5]
    after_28th = [0, 8, 12, 4, 13, 5, 9, 1]

    return stage_adders[stage] if (day > 28) else after_28th[stage]


def get_zones(dt: datetime, stage: int) -> List[int]:
    """
    - There are 16 zones
    - Every month starts at zone 1 i.e. is the same
    - Every 2 hours the zone increases by 1, every 16th interval it resets 
    - i.e. (hour_in_month // 2) % 16
    - Caveat 1: Every 4 days, they skip one zone
    - Caveat 2: The whole thing resets after 16 days
    - Caveat 3: For no reason at all, they reset stage 5 and 6 to (1, 9) on the 29th
    """
    day_of_month = (dt.day - 1) # convert to zero-index
    day_of_month %= 16 # reset after 16 days
    hour = dt.hour

    hour_in_month = (day_of_month * 12) + hour // 2

    # handling the skip-one-every-4-days
    days_to_skip = day_of_month // 4
    
    base_zone = (hour_in_month % 16) + days_to_skip + 1 # +1 because zones are 1-indexed

    result = []
    for i in range(stage):
        adder = get_adder_for_stage(i, day_of_month + 1) 
        zone_stage = ((base_zone + adder - 1) % 16) + 1
        result.append(zone_stage)
    
    return result

