from api_interaction import APIInteraction
from code_utils import CodeUtilities
from wiki_utils import WikipediaArticleExtractor
import random
from first_file import check_if_valid

from test import get_full_links_from_url
url = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/5/People/Writers_and_journalists"
try:
    full_links = get_full_links_from_url(url)
except Exception as e:
    print(str(e))



links = []
for link in full_links:
    if "en.wikipedia.org/wiki/" in link and "Category:" not in link and "User:" not in link and "File:" not in link and "Symbol:" not in link and "Wikipedia:" not in link and "Level" not in link and "Main_page" not in link and "Special:" not in link and "Portal:" not in link:
        links.append(link)
    else:
        continue
print("Links retrieved.")
print(full_links)
dataset_location = "instruct_dataset.jsonl"
model = "anthropic/claude-3-haiku"
wiki_links = links


for wiki in wiki_links:
    print(wiki)
    article_content = WikipediaArticleExtractor.get_article_from_url(wiki)
    top_10_prompt = random.choice(["What are the top 10 facts about the preceding article?", "Give me top 10 facts about that article", "Give me a top 10", "top 10 facts", "Tell me the top 10 most interesting facts in the preceding article."])
    summary_prompt = random.choice(["Give a summary of the preceding article.", "Summarize the preceding", "give a summary of the preceding wiki article", "summarize", "Summarize that wikipedia article", "give me a summary", "give me a recap of the preceding wiki article", "please summarize the preceding."])
    if article_content is not "":
        top_facts = APIInteraction.generate_top_facts(article_content, model)
        summaries = APIInteraction.generate_summaries(article_content, model)
        if check_if_valid(top_facts):
            CodeUtilities.write_to_dataset(article_content + top_10_prompt,top_facts,dataset_location)
        if check_if_valid(summaries):
            CodeUtilities.write_to_dataset(article_content + summary_prompt,summaries,dataset_location)



