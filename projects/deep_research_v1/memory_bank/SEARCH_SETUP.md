# Google Search API Setup Guide

This guide explains how to set up and test the Google Search functionality in this project.

## Required API Credentials

You need two things from Google:

1. **GOOGLE_API_KEY** - Your Google Cloud API Key
2. **GOOGLE_CSE_ID** - Your Custom Search Engine ID

## Step-by-Step Setup

### 1. Get Google API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Custom Search API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click on it and press "Enable"
4. Create an API Key:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

### 2. Create Custom Search Engine (CSE)

1. Go to [Programmable Search Engine](https://programmablesearchengine.google.com/)
2. Click "Add" or "Create a new search engine"
3. In the "Sites to search" section:
   - Enter a test site (e.g., `www.example.com`)
   - **Important**: After creation, go to "Setup" > "Basics"
   - Enable "Search the entire web" option
4. Save and note your **Search Engine ID** (also called `cx`)

### 3. Set Environment Variables

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
$env:GOOGLE_CSE_ID="your-cse-id-here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your-api-key-here
set GOOGLE_CSE_ID=your-cse-id-here
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
export GOOGLE_CSE_ID="your-cse-id-here"
```

**Or create a `.env` file:**
```
GOOGLE_API_KEY=your-api-key-here
GOOGLE_CSE_ID=your-cse-id-here
```

## Response Format

The `run_search_queries()` function returns a list where each element corresponds to one search query. Each element is a list of result dictionaries with the following structure:

```python
[
    {
        "title": "Result Title",
        "link": "https://example.com/page",
        "snippet": "A brief description of the result...",
        # Additional fields may include:
        # "displayLink": "example.com",
        # "htmlTitle": "HTML formatted title",
        # "htmlSnippet": "HTML formatted snippet",
        # "pagemap": {...}  # If available
    },
    ...
]
```

The function returns: `List[List[Dict[str, Any]]]` - one list per query, each containing result dictionaries.

## Testing

Run the test script to see the function in action:

```bash
python test/test_search.py
```

The test script will:
- Check if credentials are set
- Test single query searches
- Test multiple parallel queries
- Test with SearchQuery dataclass objects
- Display the response format

## Example Usage

```python
import asyncio
from src.search.search_query import run_search_queries, SearchQuery

async def example():
    # Using string queries
    results = await run_search_queries(
        ["Python async programming", "LangChain tutorial"],
        num_results=5
    )
    
    # Using SearchQuery objects
    queries = [
        SearchQuery(search_query="Google Search API"),
        SearchQuery(search_query="LangGraph framework")
    ]
    results = await run_search_queries(queries, num_results=3)
    
    # results is a list: [results_for_query1, results_for_query2, ...]
    for i, query_results in enumerate(results):
        print(f"Query {i+1} found {len(query_results)} results")
        for result in query_results:
            print(f"  - {result['title']}: {result['link']}")

asyncio.run(example())
```

## Free Tier Limits

Google Custom Search API has a free tier:
- **100 search queries per day**
- After that, paid plans are available

Keep this in mind when testing!

