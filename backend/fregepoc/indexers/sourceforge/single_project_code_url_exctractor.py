class SingleProjectCodeUrlExtractor:
    @staticmethod
    def extract(soup):
        if not soup:
            return

        code_urls = set()
        for span in soup.find_all("span"):
            if span.text == "Code":
                code_urls.add(span.find_parents("a")[0]["href"][1:])

        return code_urls
