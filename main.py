import os
import time
import schedule


def open_url(url: str):
    os.system(f'start "" {url}')


def copy_to_clipboard(text: str):
    os.system(f"echo {text.strip()}| clip")


def open_am():
    url: str = "https://us02web.zoom.us/j/86437456930"
    code: str = "330748"

    open_url(url)
    copy_to_clipboard(code)


def open_tznk():
    url: str = "https://us02web.zoom.us/j/6067984257"
    code: str = "964488"

    open_url(url)
    copy_to_clipboard(code)


schedule.every().wednesday.at("16:25").do(open_tznk)
schedule.every().thursday.at("14:55").do(open_am)

while True:
    schedule.run_pending()
    time.sleep(5)
