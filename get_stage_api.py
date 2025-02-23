import os
import requests
from ast import literal_eval
from datetime import datetime, timedelta
from dateutil.parser import parse
from typing import List


COCT_STAGE_API = "https://d42sspn7yra3u.cloudfront.net/?"


class CoCTApiError(Exception):
    pass


def cache_stage(stage: int):
    """
    Caching until the end of the current stage, assuming the govt cannot change the loadshedding stage
     in the middle of a 2-hour block (but otherwise, can change whenever they want)
    """
    hour_current_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    next_block_start = hour_current_time + timedelta(hours=(2 - hour_current_time.hour % 2))
    stage_file_name = f"{next_block_start}.stage"
    with open(stage_file_name, "w") as f:
        f.write(str(stage))


def clear_cache(stage_files: List[str]):
    for stage_file in stage_files:
        os.remove(stage_file)


def get_cached_stage() -> int:
    """0 status means cache miss"""
    stage_files = [f for f in os.listdir() if f.endswith(".stage")]
    if len(stage_files) == 0:
        return 0

    stage_files.sort(reverse=True)
    stage_file = stage_files[0]
    last_stages_end = stage_file.split(".")[0]
    if datetime.now() > parse(last_stages_end):
        clear_cache(stage_files)
        return 0

    with open(stage_file) as f:
        try:
            return literal_eval(f.read())
        except Exception as e:
            print(f"WARNING: broken cache file {e}")
            return 0


def get_stage_online() -> int:
    print("Getting loadshedding stage online...")
    try:
        response = requests.get(COCT_STAGE_API, timeout=60)
        stage: int = response.json()[0]["currentStage"]
    except:
        raise CoCTApiError("Failed to get loadshedding info from City of Cape Town site")

    cache_stage(stage)

    return stage


def get_stage(no_cache=False) -> int:
    if no_cache or (stage := get_cached_stage()):
        stage = stage
    else:
        stage = get_stage_online()

    print(f"Stage is: stage {stage}\n")
    return stage


