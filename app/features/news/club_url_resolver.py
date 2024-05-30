from typing import List


class ClubUrlResolver:
    def __init__(self):
        self.clubs_urls = {
            "fcbarcelona": "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts",
            "manchester_united": "https://www.newsnow.co.uk/h/Sport/Football/Premier+League/Manchester+United?type=ts",
            "inter": "https://www.newsnow.co.uk/h/Sport/Football/Serie+A/Inter+Milan?type=ts",
            # Add more clubs here
        }

    def resolve_url(self, club: str) -> str:
        return self.clubs_urls.get(club.lower(), "URL not found")

    def check_club_match(self, club: str) -> str:
        return self.clubs_urls.get(club.lower(), "Club not found")

    def check_club_collection_match(self, clubs: List[str]) -> List[str] | None:
        non_matching_clubs = []
        for club in clubs:
            if club.lower() not in self.clubs_urls.keys():
                non_matching_clubs.append(club)
            
        if non_matching_clubs:
            return non_matching_clubs
        
        return None
                