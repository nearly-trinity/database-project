import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://trinitytigers.com/services/schedule_txt.ashx?schedule="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send an HTTP GET request to the URL

for i in range(1, 229):
    print(i)
    url = "https://trinitytigers.com/services/schedule_txt.ashx?schedule=" + str(i)

    response = requests.get(url, headers=headers)
    print(response.status_code)

    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the text or other relevant information
        data = soup.get_text()  # This will get all the text from the page

        # Split the data into sections (header and schedule)
        # sections = re.split(r"\n{2,}", data)

        # # Extract header information
        # header_info = sections[0:7]

        # # Extract and clean the schedule data
        # schedule_data = sections[2].strip().split("\n")
        # schedule_data = [re.split(r"\s{2,}", line.strip()) for line in schedule_data]
        # schedule_data = [line for line in schedule_data if len(line) == 7]

        # # Create a Pandas DataFrame
        # df = pd.DataFrame(
        #     schedule_data,
        #     columns=[
        #         "Date",
        #         "Time",
        #         "At",
        #         "Opponent",
        #         "Location",
        #         "Tournament",
        #         "Result",
        #     ],
        # )

        # # Print the DataFrame
        # print(df)

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
