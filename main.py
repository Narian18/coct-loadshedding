from datetime import datetime
from typing import List 

from get_stage_api import get_stage, CoCTApiError
from zone_calculator import get_zones


def main():
    try:
        stage: int = get_stage()
    except CoCTApiError as e:
        print(e)
        return

    zones: List[int] = get_zones(datetime.now(), stage)
    zone_str = str(zones)[1:-1]
    print(f"Affected zones: {zone_str}\n")


if __name__ == "__main__":
    main()

