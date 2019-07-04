import requests
import appdirs
import os
from pathlib import Path
from .config_file import get_session_value

input_url = "https://adventofcode.com/{}/day/{}/input"
submit_url = "https://adventofcode.com/{}/day/{}/submit"


def download_input(year, day, session):
    """
        Download file from a advent of code server
    """
    session_value = get_session_value(session)
    if session_value is not None:
        if not check_if_downloaded(year, day, session):
            inputUrl = input_url.format(year, day)
            input = requests.get(inputUrl, cookies={"session": session_value})
            save_to_location(year, day, session, input.text)
    else:
        raise Exception("{} key is not present in config file".format(session))


def check_if_downloaded(year, day, session):
    """
    Check if really a input is downloaded or not
    """
    cache_location = appdirs.user_cache_dir()
    cache_file = os.path.join(
        cache_location, str(session), str(year), str(day), "input.txt"
    )
    cache_file = Path(cache_file)
    return cache_file.exists()


def save_to_location(year, day, session, input):
    """
    Save a input to its location
    """
    cache_location = appdirs.user_cache_dir()
    cache_folder = os.path.join(
        cache_location, "advent_of_code", str(session), str(year), str(day)
    )
    Path(cache_folder).mkdir(parents=True, exist_ok=True)
    cache_file = os.path.join(cache_folder, "input.txt")
    with open(cache_file, "w+") as f:
        f.write(input)
