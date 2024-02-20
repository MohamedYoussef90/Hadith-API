from exceptions import Limit_exception
import httpx
import asyncio
from typing import List
import random

class HadithAPI:
    def __init__(self, result_range: str):
        self.url_hadith_api = "https://api.hadith.sutanlab.id"
        self.available_hadith = ['muslim', 'bukhari', 'tirmidzi', 'nasai', 'abu-daud', 'ibnu-majah', 'ahmad', 'darimi', 'malik']
        self.books_endpoint = "/books"
        self.books_parameter_endpoint = "range"
        self.result_range = result_range

    def random_available_hadith(self) -> str:
        return random.choice(self.available_hadith)

    def get_keys(self, context_api) -> str:
        try:
            split_dash = self.result_range.split('-')
            message_hadith = int(split_dash[0]) - int(split_dash[1])
            random_number = random.randint(0, int(message_hadith))
            if context_api and random_number:
                get_object = context_api['data']['hadiths'][message_hadith]['arab']
                return get_object
        except Exception:
            raise Limit_exception('Error-> fetch.py::Limit_exception::70')

    def url_format(self) -> str:
        return f"{self.url_hadith_api}{self.books_endpoint}/{self.random_available_hadith()}?{self.books_parameter_endpoint}={self.result_range}"

    async def context_hadith_api(self) -> str:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self.url_format())
                if response.status_code == 200:
                    return self.get_keys(response.json())
                else:
                    # Handle different status codes or errors as you see fit
                    return f"Error: Received status code {response.status_code}"
            except httpx.RequestError as exc:
                # Handle request errors (e.g., network issues)
                return f"An error occurred while requesting {exc.request.url!r}."

if __name__ == "__main__":
    # Example usage
    hadith_api_instance = HadithAPI("1-50")
    asyncio.run(hadith_api_instance.context_hadith_api())
