class url_resolver:
    def __init__(self):
        self.club_urls = {
            "fcbarcelona": "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts",
            # Add more clubs here
        }

    def resolve(self, club: str) -> str:
        return self.club_urls.get(club.lower(), "URL not found")

