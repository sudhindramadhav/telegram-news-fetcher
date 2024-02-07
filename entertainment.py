import requests
from bs4 import BeautifulSoup

class EntertainmentScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def fetch_webpage(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            return None

    def extract_headlines(self, html_content):
        headlines_list= []
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            headlines = soup.find_all('div', class_='WavNE')

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

# Creating an instance of the EntertainmentScraper class
entertainment_scraper = EntertainmentScraper("https://timesofindia.indiatimes.com/world")

# Fetching the webpage content
html_content = entertainment_scraper.fetch_webpage()

# Extracting headlines from the fetched webpage content
entertainment_scraper.extract_headlines(html_content)
