from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

from datetime import datetime
from pathlib import Path
 
import requests

# CONSTS
HN_TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"
 
DEFAULT_MODEL = "dolphin-llama3:8b"
DEFAULT_EMBED = "nomic-embed-text"
DEFAULT_TOP_N = 10
FETCH_TIMEOUT = 10

REPORT_DIR = Path.home() / "hn_reports"

MATCHA_ASCII = r'''
                                    __________
                            ╓∞∞^"""'_________ """∞∞╖╓
                       w∩^╓╓╗▒²»`````,╔∩w∩_````└╙##▄▄▄╓^v╕
                    ▄^`╓m▀╩",▄▓╫╫▒╙╙Ü  `` ²╙+∩╓╓╓φ▄⌂╙▓ÅH╓_"ªτ
                   Å :▓Ü╫,▓▓▀Ü└`````,,,∩╕,,,````└╙╙╚▓▀Ü▓╬Φ▒∩ ╙▄
           ╓▄≡ªªªª▓ »#▌Φ▌▓╬▒░``╓▄▓▓▓▀╨```╙╩╫▓▓N#▄▄▄_╟▓▓▓▓▓░▓H ▐
         ╔^└  ____█⌐`└▓╗Å▌╫╬░╔▓▓Ñ╣▓╙`,╓╔╦╓╓_└▀Ñ▌╩▀▓▓▓▓╬╟╣▄▓▓╩ ╟
        Φ" .╔K╜""╙█╙, -╙╠▓▓Ä¥▓▓M╟▓▓▄▓▓▀`'╨▀▓▓▓M▓▓▄__▄▓▓▓╬▀╨^_Å╟
       ▐⌐ ░▓      ╙▌_F%, ╙╚╬▓▓▓▓▓▓╣▄▓M``,``│▓▄▓▓▓▀▀└└┘└ _═"─|╬
       ▐⌐¡░▓       ▌░=_ '╙ª%▄````╙╙╙▀▀#╣▀▀#▀▀╨╙╙` ``╓╓ⁿⁿ`  ,=░▌
        ▓░[▓╦      ▓░░░░░___ ¬`^"""═══════════^"""         ░░▄"
        ╙H░╠▌      ╟░░░░░░░░░==...______________...       _░░▓
         ╚▄│╩▀╦     ▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░       »░▐Ñ
          ╙Ü│╠╠╬▄╓_ ▀▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░       ░░▌
            'W╬▒╠╬╬╬╬▓H░░░░░░░░░░░░░░░░░░░░░░░░░░░░      =░╔"
                "▀▀ÑÑ╬▌K░░░░░░░░░░░░░░░░░░░░░░░░░░░      ░░▌
                   ,,╟╣▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░     :░▓≡,,_
               ▄¥╩╙░░░░▀▒╠▒░░░░░░░░░░░░░░░░░░░░░░░`     ]╬░░░░╙╙@N_
              ╬ ░░░░░╔╠╠╫▒╠╠▒H░░░░░░░░░░░░░░░░░░░=    ,╦▓Ñ╠╦░░░░░ ╙▄
             ▓  ░░░░[╠╠╠╠╬╬╫╠╠╠K▒╥░░░░░░░░░░░░░░░⌐  ,@╬╬╠╠╠╠░░░░░  ▐
             ▀  ²░░░»╫▒╠╠╠╠╬╬╬╠╠╠╠╠╠╠╠╠╠╠╠╠╠╠╠╩│= ╓╬╬Ñ╠╠╠╠╠▓░░░░`  ║
              ª╕  `░░░│▀╫╬▒╠╠╠╬╬▀▓▓╬╬╬╬╬╬╬╬╬╬]▄▄@╬╬Ñ╠╠╠╬╫╬Ñ░░░`` _A`
                ^╦  `=░░░│╙Ö▀▓▄▄▄▒╠╬╬╬╬╬╬╬╬╬╬╬Ñ╬▄▄▄Å▀ÖÖ│»░░=`  ╓C
                  'ª%╥__'^^===░░░╙╙╙╙╙╙╙╙╙╙╙╙╙╙│░░░=^^^```_╓≤M└
                        "∞∞▄▄▄                     ▄▄▄∞∞""
                              ''└"""""""""""""^''`
'''

def get_top_stories(n) -> list:
    response = requests.get(HN_TOP_STORIES_URL, timeout=FETCH_TIMEOUT)
    response.raise_for_status()
    # return the top n story IDs
    return response.json()[:n]

def get_story_details(story_id) -> dict:
    if story_id is None:
        return None
    # fetch the story details using the story ID
    response = requests.get(HN_ITEM_URL.format(id=story_id), timeout=FETCH_TIMEOUT)
    # check if the request was successful
    response.raise_for_status()
    return response.json()

def get_and_save_top_stories(n) -> list:
    story_ids = get_top_stories(n)
    stories = []
    # fetch details for each story ID and save them to a list
    for id in story_ids:
        story = get_story_details(id)
        if story:
            stories.append(story)

    return stories

def stories_to_documents(stories) -> list:
    documents = []
    for story in stories:
        sid      = story.get("id", "")
        title    = story.get("title", "No title")
        url      = story.get("url") or f"https://news.ycombinator.com/item?id={sid}"
        score    = story.get("score", 0)
        comments = story.get("descendants", 0)
        author   = story.get("by", "unknown")
        body     = story.get("text", "")

        content_parts = [
            f"Title: {title}",
            f"URL: {url}",
            f"HackerNews score: {score} points",
            f"Comments: {comments}",
            f"Posted by: {author}",
        ]
        if body:
            clean_body = (body
                .replace("<p>", "\n")
                .replace("&#x27;", "'")
                .replace("&amp;", "&")
                .replace("&lt;", "<")
                .replace("&gt;", ">"))
            content_parts.append(f"Post body:\n{clean_body[:800]}")
 
        documents.append(Document(
            text="\n".join(content_parts),
            metadata={
                "title":    title,
                "url":      url,
                "score":    score,
                "comments": comments,
                "author":   author,
                "hn_id":    str(sid),
            },
            excluded_embed_metadata_keys=["hn_id", "url"],
        ))
    return documents

def build_index(documents: list[Document], embed_model_name: str) -> VectorStoreIndex:
    embed_model = OllamaEmbedding(model_name="nomic-embed-text")
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model,
        show_progress=True,
    )
    return index


def generate_report(index: VectorStoreIndex) -> None:
    llm = Ollama(model=DEFAULT_MODEL, request_timeout=300.0)
 
    query_engine = index.as_query_engine(
        llm=llm,
        similarity_top_k=15,        
        response_mode="tree_summarize", 
    )
    
    with open("/Users/lucyang/Desktop/project/secAI/prompt.txt", "r") as f:
        prompt = f.read()
    response = query_engine.query(prompt)
    report_text = str(response)

    print(report_text)


def run_digest() -> None:
    date_str = datetime.now().strftime("%A, %B %d %Y — %I:%M %p")
    print(MATCHA_ASCII)
    print(f"{'='*60}")
    print(f"  HackerNews Morning Digest")
    print(f"  {date_str}")
    print(f"{'='*60}")
 
    # Fetch raw stories from HN API
    stories = get_and_save_top_stories(DEFAULT_TOP_N)
    if not stories:
        print("No stories fetched. Check your internet connection.")
        return
 
    # Convert to llama_index Documents
    documents = stories_to_documents(stories)

    # Embed & build vector index 
    index = build_index(documents, DEFAULT_EMBED)
 
    # Query index with LLM → morning report
    generate_report(index)
 

def main():
    run_digest()
 
if __name__ == "__main__":
    main()