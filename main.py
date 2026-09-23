# My thoughts are not really anything so im thinking of Jesus Christ my Lord Amen! So okay so we need a some kind of a text file where we will store the classes data. Which file format sohuld we use? json? maybe csv though? csv is like a table. okay so i created a text file that will show me this thing. oaky now i wanna read the file for this i will need a current folder. okay yeah i need to read the file. okay so when trying to access the file i have an issue where i not always have the url or the code but i cant account for that, i need to decouple the 3 arguments in case they are there. one option would be to use a pandas dataframe because it allows for missing values. althogh this might be an overkill for the schedule that will need to access. created a csv file but there's still missing values so i should maybe just fill them in with the hoax values or create a json file where i would be able to just assign an empty string to the thing. okay it turns out the .split python method has a max split param. although i have no idea how to use it. lets try the json option.

from dataclasses import dataclass
import json
import os
import time
import schedule


def open_in_browser(url: str):
    os.system(f'start "" {url}')


def copy_to_clipboard(text: str):
    os.system(f"echo {text.strip()}| clip")


@dataclass
class Entry:
    title_and_type: str
    url: str
    code: str


current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = "data.json"
file_path = os.path.join(current_dir, file_name)
classes_data: list[Entry] = list()
with open(file_path, encoding="utf-8", mode="r") as f:
    lines = json.load(f)
    for line in lines:
        entry = Entry(
            title_and_type=line["title_and_type"], url=line["url"], code=line["code"]
        )
        classes_data.append(entry)
classes_data = sorted(classes_data, key=lambda entry: entry.title_and_type)


def open_tznk():
    url: str = "https://us02web.zoom.us/j/6067984257"
    code: str = "964488"

    open_in_browser(url)
    copy_to_clipboard(code)
    print("Opening TZNK class.")


"""
schedule.every().wednesday.at("16:25").do(open_tznk)
while True:
    print("Running...")
    schedule.run_pending()
    time.sleep(5)
"""
