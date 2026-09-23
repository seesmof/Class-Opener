"""
My thoughts are not really anything so im thinking of Jesus Christ my Lord Amen! So okay so we need a some kind of a text file where we will store the classes data. Which file format sohuld we use? json? maybe csv though? csv is like a table. okay so i created a text file that will show me this thing.
"""

import os
import time
import schedule


def open_in_browser(url: str):
    os.system(f'start "" {url}')


def copy_to_clipboard(text: str):
    os.system(f"echo {text.strip()}| clip")


def open_am():
    url: str = "https://us02web.zoom.us/j/86437456930"
    code: str = "330748"

    open_in_browser(url)
    copy_to_clipboard(code)
    print("Opening AM class.")


def open_tznk():
    url: str = "https://us02web.zoom.us/j/6067984257"
    code: str = "964488"

    open_in_browser(url)
    copy_to_clipboard(code)
    print("Opening TZNK class.")


schedule.every().wednesday.at("16:25").do(open_tznk)
schedule.every().thursday.at("14:55").do(open_am)

while True:
    print("Running...")
    schedule.run_pending()
    time.sleep(5)
