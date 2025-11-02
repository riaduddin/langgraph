from langchain_community.utilities.google_search import GoogleSearchAPIWrapper
import asyncio
from dataclasses import asdict, dataclass
from typing import Dict, Any, List, Union
# just to handle objects created from LLM reponses
@dataclass
class SearchQuery:
        search_query: str
        def to_dict(self) -> Dict[str, Any]:
                return asdict(self)

google_search = GoogleSearchAPIWrapper()

async def run_search_queries(
        search_queries: List[Union[str, SearchQuery]],
        num_results: int = 5,
        include_raw_content: bool = False
) -> List[Dict[str, Any]]:
        search_tasks = []
        for query in search_queries:
                # Handle both string and SearchQuery objects
                # Just in case LLM fails to generate queries as:
                # class SearchQuery(BaseModel):
                #       search_query: str
                if isinstance(query, SearchQuery):
                        query_str = query.search_query
                else:
                        query_str = str(query) # text query
                try:
                        # get results from google search async (in parallel) for each search query
                        # GoogleSearchAPIWrapper doesn't have raw_results_async, so we wrap it
                        async def run_google_search(query: str, num: int):
                                # Run the synchronous search in an executor
                                loop = asyncio.get_event_loop()
                                results = await loop.run_in_executor(
                                        None,
                                        lambda: google_search.results(query, num_results=num)
                                )
                                return results
                        
                        search_tasks.append(
                                run_google_search(query_str, num_results)
                        )
                except Exception as e:
                        print(f"Error creating search task for query '{query_str}': {e}")
                        continue
        # Execute all searches concurrently and await results
        try:
                if not search_tasks:
                        return []
                search_docs = await asyncio.gather(*search_tasks, return_exceptions=True)
                # Filter out any exceptions from the results
                valid_results = [
                        doc for doc in search_docs
                        if not isinstance(doc, Exception)
                ]
                return valid_results
        except Exception as e:
                print(f"Error during search queries: {e}")
                return []