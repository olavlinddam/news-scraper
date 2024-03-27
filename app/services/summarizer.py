import app.services.scrapers.fcbarcelona.fcbarcelonadk as fcb_scraper
import requests

articles = fcb_scraper.get_articles()
rapid_api_url = "https://textanalysis-text-summarization.p.rapidapi.com/text-summarizer-text"

headers = {
    "content-type": "application/x-www-form-urlencoded",
    'X-RapidAPI-Key': '561684489amsh6e7c7f74ac44883p120bd8jsn91f875378d32',
    "X-RapidAPI-Host": "textanalysis-text-summarization.p.rapidapi.com"
}

full_text = ("  Robert Lewandowski og Polen sikrede sig tirsdag en plads ved sommerens EM i Tyskland, da man efter et sandt drama slog Wales i den afgørende play-off kamp. Polakkerne sikrede sig EM-billetten med en sejr efter straffesparkskonkurrence.Der blev tale om en sand gyser, da Robert Lewandowski og det polske landshold tirsdag aften mødte Wales i den afgørende play-off kamp om en plads ved EM i Tyskland til sommer. Her skulle man afgøre det hele i straffesparkskonkurrence, hvor der kun blev brændt en enkelt gang.Den ordinære kamp var intens, dramatisk og nervøs fra begge landshold, og begge mandskaber havde kun få chancer til at bringe sig i front. Der blev derfor ikke scoret i de første 90 minutter, hvorfor man måtte i forlænget spilletid.I den forlængede spilletid blev der heller ikke scoret og dermed skulle det hele afgøres i en straffesparkskonkurrence. Her lagde Lewandowski ud med en scoring, hvorefter der blev scoret på de næste otte straffespark. På det sidste straffespark til Wales brændte Daniel James dog og dermed blev det Polen, som stjal den sidste plads ved EM.Dermed får 35-årige Robert Lewandowski lov til at føre an i hvad der med stor sandsynlighed bliver hans sidste EM for Polen. Her står det allerede klart, at Polen skal spille i gruppe med Frankrig, Holland og Østrig.")

for a in articles:
    payload = {
        "sentnum": "2",
        "text": a.content
    }
    response = requests.post(rapid_api_url, data=payload, headers=headers)
    print(response.json())
