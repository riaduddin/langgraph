"""
Test script for the run_search_queries function using Google Search API.

Before running this script, you need to set up:
1. GOOGLE_API_KEY - Your Google API Key
2. GOOGLE_CSE_ID - Your Custom Search Engine ID

To get these credentials:
1. Go to https://console.cloud.google.com/
2. Create/select a project
3. Enable "Custom Search API"
4. Create an API Key in "Credentials"
5. Go to https://programmablesearchengine.google.com/
6. Create a new search engine (select "Search the entire web")
7. Get your Search Engine ID (CSE_ID)

Set environment variables:
export GOOGLE_API_KEY="your-api-key"
export GOOGLE_CSE_ID="your-cse-id"
"""

import asyncio
import os
import json
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.search.search_query import run_search_queries, SearchQuery

async def test_search_queries():
    """Test the run_search_queries function with sample queries."""
    
    # Check if API credentials are set
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    
    if not api_key or not cse_id:
        print("❌ Error: API credentials not found!")
        print("\nPlease set the following environment variables:")
        print("  - GOOGLE_API_KEY")
        print("  - GOOGLE_CSE_ID")
        print("\nSee the top of this file for setup instructions.")
        return
    
    print("✅ API credentials found!")
    print(f"   GOOGLE_API_KEY: {api_key[:10]}...")
    print(f"   GOOGLE_CSE_ID: {cse_id}")
    print("\n" + "="*60)
    
    # Test 1: Single string query
    print("\n📝 Test 1: Single string query")
    print("-" * 60)
    query1 = "Python async programming"
    print(f"Query: {query1}")
    
    results1 = await run_search_queries([query1], num_results=3)
    print(f"\nNumber of result sets: {len(results1)}")
    if results1:
        print(f"Number of results in first set: {len(results1[0])}")
        print("\nFirst result structure:")
        if results1[0]:
            print(json.dumps(results1[0][0], indent=2))
    
    print("\n" + "="*60)
    
    # Test 2: Multiple string queries (runs in parallel)
    print("\n📝 Test 2: Multiple string queries (parallel execution)")
    print("-" * 60)
    queries2 = [
        "LangChain framework",
        "Python dataclasses",
        "AsyncIO tutorial"
    ]
    print(f"Queries: {queries2}")
    
    results2 = await run_search_queries(queries2, num_results=2)
    print(f"\nNumber of result sets: {len(results2)}")
    for i, result_set in enumerate(results2):
        print(f"\nResult set {i+1} ({len(result_set)} results):")
        if result_set:
            # Show just the title and link of first result
            first_result = result_set[0]
            print(f"  Title: {first_result.get('title', 'N/A')}")
            print(f"  Link: {first_result.get('link', 'N/A')}")
            print(f"  Snippet: {first_result.get('snippet', 'N/A')[:100]}...")
    
    print("\n" + "="*60)
    
    # Test 3: Using SearchQuery dataclass objects
    print("\n📝 Test 3: Using SearchQuery dataclass objects")
    print("-" * 60)
    queries3 = [
        SearchQuery(search_query="Google Search API"),
        SearchQuery(search_query="LangGraph framework")
    ]
    print(f"Queries: {[q.search_query for q in queries3]}")
    
    results3 = await run_search_queries(queries3, num_results=2)
    print(f"\nNumber of result sets: {len(results3)}")
    for i, result_set in enumerate(results3):
        print(f"\nResult set {i+1}:")
        if result_set:
            print(f"  First result title: {result_set[0].get('title', 'N/A')}")
    
    print("\n" + "="*60)
    
    # Show complete response format
    print("\n📋 Complete Response Format Example:")
    print("-" * 60)
    if results1 and results1[0]:
        print(json.dumps(results1[0][0], indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    print("🔍 Testing Google Search Query Function")
    print("="*60)
    asyncio.run(test_search_queries())

