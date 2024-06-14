import logging
from typing import List

from app.data.models.league import League
from app.data.repository import Repository


class AdminService:
    def __init__(self, database_name: str, collection_name: str):
        self.logger = logging.getLogger(__name__)
        self.repository = Repository(database_name=database_name, collection_name=collection_name)

    async def add_leagues(self, leagues: List[League]):
        try:
            # Fetch existing league documents
            existing_league_documents = await self.repository.get_documents(0)

            # Extract names of existing leagues directly from the documents
            existing_league_names = {doc['name'] for doc in existing_league_documents}

            # Check for duplicates
            for league in leagues:
                if league.name in existing_league_names:
                    raise ValueError(f"League with name '{league.name}' already exists.")

            # Save new documents
            documents = [league.to_dict() for league in leagues]
            await self.repository.save_documents(documents)
        except Exception as e:
            self.logger.exception("Error adding leagues", str(e))
            raise Exception("Could not add leagues", str(e))