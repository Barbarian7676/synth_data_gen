import os
from api_interaction import APIInteraction
from code_utils import CodeUtilities
from wiki_utils import WikipediaArticleExtractor

dataset_location = "instruct_dataset.jsonl"

wiki_links = ["https://en.wikipedia.org/wiki/Jack_Dorsey"]


for wiki in wiki_links:
    article_content = WikipediaArticleExtractor.get_article_from_url(wiki)
    top_facts = APIInteraction.generate_top_facts(article_content)
    summaries = APIInteraction.generate_summaries(article_content)
    CodeUtilities.write_to_dataset(article_content,top_facts,dataset_location)
    CodeUtilities.write_to_dataset(article_content,summaries,dataset_location)



