import requests
from bs4 import BeautifulSoup

url = "https://www.google.com/"

# Send an HTTP GET request to the URL
response = requests.get(url)
print(response)

if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the text or other relevant information
    data = soup.get_text()  # This will get all the text from the page

    # Print or process the data as needed
    print(data)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
