import requests
from bs4 import BeautifulSoup


class SingleProjectGitUrlExtractor:
    @staticmethod
    def extract(soup):
        code_urls = set()

        if not soup:
            return code_urls

        for li in soup.find_all('ul', {'class': 'dropdown'})[0]('li'):
            try:
                a = li('a')[0]
                if a('span')[0].text.startswith('Git'):
                    href_link = a['href']
                    if href_link.startswith('/p'):
                        url = f'https://sourceforge.net/{href_link[1:]}'

                        response = requests.get(url)
                        soup = BeautifulSoup(response.text, 'html.parser')

                        for link in soup.find_all('div', {'class': 'list card'}):
                            element = link('a')[0]
                            cleaned_link = element['href']
                            if cleaned_link.startswith('/p'):
                                code_urls.add((element.text, cleaned_link[1:]))
            except:
                pass

        return code_urls
