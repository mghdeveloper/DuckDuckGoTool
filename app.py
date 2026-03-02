#!/usr/bin/env python3
from flask import Flask, request, jsonify
from ddgs import DDGS

app = Flask(__name__)

class DuckDuckGoTool:
    def ddg_search_web(self, query: str, max_results: int = 5):
        """
        Perform a web search using DuckDuckGo (DDGS v9.x)
        """
        try:
            with DDGS() as ddgs:
                # ddgs.text() now returns a generator of dictionaries
                results = ddgs.text(query, max_results=max_results)
                return list(results)
        except Exception as e:
            print(f"Search error: {e}")
            return []

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    max_results = int(request.args.get("max_results", 5))

    if not query:
        return jsonify({"error": "No query provided"}), 400

    tool = DuckDuckGoTool()
    results = tool.ddg_search_web(query, max_results)

    simplified = [
        {
            "title": r.get("title", "No title"),
            "url": r.get("href", "No link"),
            "description": r.get("body", "No description")
        }
        for r in results
    ]

    return jsonify({"results": simplified})

@app.route("/")
def home():
    return """
    <h1>DuckDuckGo Search API</h1>
    <p>Use <code>/search?q=your+query&max_results=5</code> to search.</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
