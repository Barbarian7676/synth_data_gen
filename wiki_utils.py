import requests
import re
import os
import tempfile

class WikipediaArticleExtractor:
    @staticmethod
    def get_article_from_url(url):
        match = re.search(r"wikipedia\.org/wiki/(.+)", url)
        if not match:
            raise ValueError("Invalid Wikipedia URL")
        article_title = match.group(1)

        article_title = article_title.replace('_', ' ')
        api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro&explaintext&titles={article_title}&format=json"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch article information: {response.status_code}")
        article_info = response.json()

        page = next(iter(article_info["query"]["pages"].values()))
        if "missing" in page:
            raise ValueError("The article does not exist")

        text_content = page["extract"]
        
        return text_content


    @staticmethod
    def _save_text(text_content, article_title):
        temp_dir = tempfile.mkdtemp()
        article_file_path = os.path.join(temp_dir, f"{article_title}.txt")
        with open(article_file_path, "w", encoding='utf-8') as file:
            file.write(text_content)
        return article_file_path

