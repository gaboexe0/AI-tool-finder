import os
import time
import requests
from typing import Optional, List, Dict, Union
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LIMIT = 3
RATE_LIMIT_SECONDS = 1


class RateLimiter:
    def __init__(self, calls_per_second: int = 1):
        self.calls_per_second = calls_per_second
        self.last_call = 0

    def wait(self):
        elapsed = time.time() - self.last_call
        if elapsed < self.calls_per_second:
            time.sleep(self.calls_per_second - elapsed)
        self.last_call = time.time()


class QuotaManager:
    def __init__(self, file_path: str = ".quota"):
        self.file_path = file_path
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                data = f.read().strip().split(",")
                if len(data) == 2:
                    self.count = int(data[0])
                    self.date = data[1]
                else:
                    self.reset()
        else:
            self.reset()

    def reset(self):
        self.count = 0
        self.date = datetime.now().strftime("%Y-%m-%d")

    def increment(self):
        current_date = datetime.now().strftime("%Y-%m-%d")
        if self.date != current_date:
            self.reset()
        self.count += 1
        self.save()

    def save(self):
        with open(self.file_path, "w") as f:
            f.write(f"{self.count},{self.date}")

    def get_status(self) -> Dict[str, any]:
        return {
            "count": self.count,
            "date": self.date,
            "remaining": max(0, 100 - self.count),
        }


def enhance_query(query: str, source: str) -> str:
    source_contexts = {
        "npmjs": f"{query} npm package library best popular 2024",
        "github": f"{query} github repository stars trending best",
        "stackoverflow": f"{query} stackoverflow question answer solution best practice",
    }
    return source_contexts.get(source, query)


class ToolFinder:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SerpApi key not found. Set SERPAPI_API_KEY env variable.")

        self.rate_limiter = RateLimiter(RATE_LIMIT_SECONDS)
        self.quota_manager = QuotaManager()

    def get_quota_status(self) -> Dict[str, any]:
        return self.quota_manager.get_status()

    def search_npm(
        self, query: str, limit: int = DEFAULT_LIMIT
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:
        self.rate_limiter.wait()
        enhanced = enhance_query(query, "npmjs")
        result = self._search(enhanced, "npmjs", limit)
        self.quota_manager.increment()
        return result

    def search_github(
        self, query: str, limit: int = DEFAULT_LIMIT
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:
        self.rate_limiter.wait()
        enhanced = enhance_query(query, "github")
        result = self._search(enhanced, "github", limit)
        self.quota_manager.increment()
        return result

    def search_stackoverflow(
        self, query: str, limit: int = DEFAULT_LIMIT
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:
        self.rate_limiter.wait()
        enhanced = enhance_query(query, "stackoverflow")
        result = self._search(enhanced, "stackoverflow", limit)
        self.quota_manager.increment()
        return result

    def _search(
        self, query: str, source: str, limit: int
    ) -> Union[List[Dict[str, str]], Dict[str, str]]:
        url = "https://serpapi.com/search"
        params = {
            "q": f"{query} site:{source}.com",
            "api_key": self.api_key,
            "engine": "google",
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            results: List[Dict[str, str]] = []
            for item in data.get("organic_results", [])[:limit]:
                results.append(
                    {
                        "title": item.get("title", ""),
                        "link": item.get("link", ""),
                        "snippet": item.get("snippet", ""),
                        "source": source,
                    }
                )
            return results
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
