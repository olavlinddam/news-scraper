import requests

rapid_api_url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer-text"

headers = {
    "content-type": "application/x-www-form-urlencoded",
    'X-RapidAPI-Key': '561684489amsh6e7c7f74ac44883p120bd8jsn91f875378d32',
    "X-RapidAPI-Host": "textanalysis-text-summarization.p.rapidapi.com"
}


def summarize(articles):
    for a in articles:
        payload = {
            "sentnum": "1",
            "text": a.content
        }
        response = requests.post(rapid_api_url, data=payload, headers=headers)
        response_data = response.json()
        a.content = " ".join(response_data["sentences"])

    return articles

