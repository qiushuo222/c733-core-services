import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import request, abort

from rpc_client import PDFRankingClient

ARXIV_API_FORMAT = "http://export.arxiv.org/api/query?search_query={}&start={}&max_results={}&sortBy=relevance&sortOrder=descending"
DEFAULT_PAGESIZE = 10


app = Flask(__name__)


@app.route("/")
def hello_world():
    return {}


@app.route("/search", methods=["GET"])
def serve_search():
    keywords = request.args.get('keywords', '')
    keywords = keywords.split(" ")
    if not keywords:
        abort(404)
    
    start, max_results = request.args.get('start', '0'), request.args.get('max_results', str(DEFAULT_PAGESIZE))
    start, max_results = int(start), int(max_results)

    query_string = " ".join(keywords)
    uri = ARXIV_API_FORMAT.format("all:"+fr'"{query_string}"', start, max_results)
    resp = requests.get(uri)
    if resp.status_code != requests.codes.ok:
        abort(500)

    soup = BeautifulSoup(resp.text, "xml")

    total_results = int(soup.find("opensearch:totalResults").get_text())
    start_index = int(soup.find("opensearch:startIndex").get_text())
    items_per_page = int(soup.find("opensearch:itemsPerPage").get_text())

    query_results = []
    entries = soup.find_all("entry")
    for entry in entries:
        result = {
            "paper_page": entry.find("id").get_text(),
            "title": entry.find("title").get_text(),
            "authors": [author.find("name").get_text() for author in entry.find_all("author")],
            "pdf_link": entry.find("link", title="pdf").get("href")
        }
        query_results.append(result)
    
    ranking_client = PDFRankingClient()
    pdf_rankings = ranking_client.call([ele["pdf_link"] for ele in query_results])

    for query_result in query_results:
        query_result["score"] = pdf_rankings.get(query_result["pdf_link"], 0)

    return {
        "totalResults": total_results,
        "startIndex": start_index,
        "itemsPerPage": items_per_page,
        "results": query_results
    }
