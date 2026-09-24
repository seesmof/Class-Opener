# My thoughts are not really anything so im thinking of Jesus Christ my Lord Amen! So okay so we need a some kind of a text file where we will store the classes data. Which file format sohuld we use? json? maybe csv though? csv is like a table. okay so i created a text file that will show me this thing. oaky now i wanna read the file for this i will need a current folder. okay yeah i need to read the file. okay so when trying to access the file i have an issue where i not always have the url or the code but i cant account for that, i need to decouple the 3 arguments in case they are there. one option would be to use a pandas dataframe because it allows for missing values. althogh this might be an overkill for the schedule that will need to access. created a csv file but there's still missing values so i should maybe just fill them in with the hoax values or create a json file where i would be able to just assign an empty string to the thing. okay it turns out the .split python method has a max split param. although i have no idea how to use it. lets try the json option. okay the class opening works. okay so the schedule works, i mean the data for the classes. now i gotta figure out how to make a schedule. so for now i have my classes schedule in portal website. i thought of scraping it from there, but it's a weird table where nothing can be understood if looking into the html. so i think to either add the data to google calendar, or a better options which seems to me is to add a schedule to todoist and fetch it from there. i think i will go with the latter. for now i need to test the api key environment variable. okay it all works praise King Jesus, now i just need to add a check if the time of the class is past, or although its okay without it i think.

from dataclasses import dataclass
import datetime
import json
import os
import pprint
import time
from dotenv import load_dotenv
import schedule
from todoist_api_python.api import TodoistAPI

load_dotenv()

# Global Variables
current_dir = os.path.dirname(os.path.abspath(__file__))
api_key_name = "TODOIST_API_KEY"
todoist_api_key = os.getenv(
    api_key_name, ""
)  # the second argument is a fallback default
todoist_api = TodoistAPI(todoist_api_key)


# Helper Functions
def open_in_browser(url: str):
    os.system(f'start "" {url}')


def copy_to_clipboard(text: str):
    os.system(f"echo {text.strip()}| clip")


def load_todays_tasks():
    tasks = todoist_api.get_tasks()
    classes_for_today: list[ScheduledClass] = list()

    for task in tasks:
        for t in task:
            if (
                not t.due
                or len(t.content) != 4
                or not " " in t.content
                or not ("P" in t.content.upper() or "L" in t.content.upper())
            ):
                continue

            class_datetime = t.due.date.strftime("%d.%m.%Y %H:%M")
            class_time = class_datetime.split(" ")[-1]

            # Rule out the classes that are not for today
            if class_datetime.split(" ")[0] != datetime.date.today().strftime(
                "%d.%m.%Y"
            ):
                continue

            # Give a -3 minutes delay before the class time
            wait_minutes_before_class = 3
            class_hours, class_minutes = class_time.split(":")
            preponed_time = (
                f"{class_hours}:{int(class_minutes)-wait_minutes_before_class:02}"
            )

            entry = ScheduledClass(name_and_type=t.content, time=preponed_time)
            classes_for_today.append(entry)

    return classes_for_today


# Data Models
@dataclass
class Entry:
    name_and_type: str
    url: str
    code: str


@dataclass
class ScheduledClass:
    name_and_type: str
    time: str


def populate_classes_data(data_file_name: str = "data.json") -> list[Entry]:
    classes_data: list[Entry] = list()
    file_path = os.path.join(current_dir, data_file_name)

    with open(file_path, encoding="utf-8", mode="r") as f:
        lines = json.load(f)
        for line in lines:
            entry = Entry(
                name_and_type=line["title_and_type"],
                url=line["url"],
                code=line["code"],
            )
            classes_data.append(entry)
    classes_data = sorted(classes_data, key=lambda entry: entry.name_and_type)

    return classes_data


def open_class(class_data: Entry):
    open_in_browser(class_data.url)
    copy_to_clipboard(class_data.code) if class_data.code else ""

    class_name, class_type = class_data.name_and_type.split(" ")
    print(
        f'Opening {class_name}, it is a {"practice" if class_type=="P" else "lecture"}.'
    )


def main():
    classes_data = populate_classes_data()
    todays_schedule = load_todays_tasks()
    if not todays_schedule:
        print("No classes today.")
        exit(1)

    print("Scheduling...")
    for scheduled_class in todays_schedule:
        class_data = [
            data
            for data in classes_data
            if data.name_and_type == scheduled_class.name_and_type
        ][0]

        print(
            f"Schedule {scheduled_class.name_and_type} for {scheduled_class.time} today."
        )
        schedule.every().day.at(scheduled_class.time).do(open_class, class_data)


if __name__ == "__main__":
    main()
    print("\nRunning...")

    while True:
        schedule.run_pending()
        time.sleep(12)
