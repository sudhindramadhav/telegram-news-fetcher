import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_webpage(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            print("Successfully fetched the webpage.")
            return response.text
        else:
            print("Failed to fetch the webpage. Status code:", response.status_code)
            return None

    def extract_headlines(self, html_content):
        headlines_list= []
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            headlines = soup.find_all('figcaption')

            if headlines:
                print("Entertainment Headlines:")
                for headline in headlines[:10]:
                    headlines_list.append(headline.text.strip())
                    print(headline.text.strip())
                    print()
            else:
                pass
        else:
            pass
        return headlines_list
# Creating an instance of the WebScraper class
web_scraper = WebScraper("https://timesofindia.indiatimes.com/education")

# Fetching the webpage content
html_content = web_scraper.fetch_webpage()

# Extracting headlines from the fetched webpage content
web_scraper.extract_headlines(html_content)
