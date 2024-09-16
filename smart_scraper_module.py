import asyncio
import json
from scrapegraphai.graphs import SmartScraperGraph
import nest_asyncio

nest_asyncio.apply()

class SmartScraper:
    def __init__(self, llm_model="ollama/llama3", llm_base_url="http://localhost:11434",
                 embeddings_model="ollama/nomic-embed-text", embeddings_base_url="http://localhost:11434"):
        self.graph_config = {
            "llm": {
                "model": llm_model,
                "temperature": 0,
                "format": "json",
                "base_url": llm_base_url,
            },
            "embeddings": {
                "model": embeddings_model,
                "base_url": embeddings_base_url,
            },
            "verbose": True,
        }

    def scrape(self, url, prompt):
        smart_scraper_graph = SmartScraperGraph(
            prompt=prompt,
            source=url,
            config=self.graph_config
        )

        try:
            result = smart_scraper_graph.run()  # Changed from run_async to run
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    @staticmethod
    def prettify_json(result):
        if result:
            return json.dumps(result, indent=2)
        return None