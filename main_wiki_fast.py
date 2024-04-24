import threading
from test import get_full_links_from_url
from wiki_utils import WikipediaArticleExtractor
from first_file import check_if_valid
import random
from api_interaction import APIInteraction
from code_utils import CodeUtilities


def process_articles(links, model, dataset_location):
    for link in links:
        try:
            article_content = WikipediaArticleExtractor.get_article_from_url(link)
            if article_content:
                top_10_prompt = random.choice(["What are the top 10 facts about the preceding article?", "Give me top 10 facts about that article","Give me a top 10", "top 10 facts", "Tell me the top 10 most interesting facts in the preceding article."])
                summary_prompt = random.choice(["Give a summary of the preceding article.", "Summarize the preceding", "give a summary of the preceding wiki article", "summarize", "Summarize that wikipedia article", "give me a summary", "give me a recap of the preceding wiki article", "please summarize the preceding."])
                criticism_prompt = random.choice(["Criticize the preceding text", "Give a criticism of the preceding text","Critize the preceding", "Critiize that article", "critique that article"])

                top_facts = APIInteraction.generate_top_facts(article_content, model)
                summaries = APIInteraction.generate_summaries(article_content, model)
                criticism = APIInteraction.generate_criticism(article_content, model)

                if check_if_valid(top_facts):
                    CodeUtilities.write_to_dataset(article_content + top_10_prompt, top_facts, dataset_location)
                if check_if_valid(summaries):
                    CodeUtilities.write_to_dataset(article_content + summary_prompt, summaries, dataset_location)
                if check_if_valid(criticism):
                    CodeUtilities.write_to_dataset(article_content + criticism_prompt, criticism, dataset_location)
        except Exception as e:
            print(f"Error processing {link}: {str(e)}")

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def main(url, model, dataset_location):
    full_links = get_full_links_from_url(url)
    excluded_namespaces = ["Category:", "User:", "File:", "Wikipedia:", "Template:", "Special:", "Talk:", "Portal:", "Draft:", "Help:", "Module:"]
    links = [link for link in full_links if "en.wikipedia.org/wiki/" in link and not any(ns in link for ns in excluded_namespaces)]


    chunks = list(chunk_list(links, len(links) // 20 + (len(links) % 5 > 0)))
    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=process_articles, args=(chunk, model, dataset_location))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Wikipedia:Vital_articles/Level/5/Everyday_life"
    model = "anthropic/claude-3-haiku"
    dataset_location = "instruct_dataset.jsonl"
    main(url, model, dataset_location)
