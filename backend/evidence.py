import requests


def search_web(query):

    url = "https://api.duckduckgo.com/"

    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        sources = []

        if data.get("AbstractText"):
            sources.append({
                "title": data.get("Heading", "DuckDuckGo Result"),
                "url": data.get("AbstractURL", ""),
                "snippet": data.get("AbstractText", "")
            })

        for item in data.get("RelatedTopics", [])[:5]:

            if "Text" in item and "FirstURL" in item:
                sources.append({
                    "title": item["Text"][:100],
                    "url": item["FirstURL"],
                    "snippet": item["Text"]
                })

        return sources

    except Exception as error:

        return [{
            "title": "Evidence retrieval failed",
            "url": "",
            "snippet": str(error)
        }]


def create_evidence(task):

    sources = search_web(task)

    if sources and sources[0]["title"] != "Evidence retrieval failed":
        status = "retrieved"
    else:
        status = "insufficient"

    return {
        "task": task,
        "sources": sources,
        "status": status
    }