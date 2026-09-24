import os

from dotenv import load_dotenv

api_key_name = "TODOIST_API_KEY"
load_dotenv()
data = os.getenv(api_key_name)
print(data)
