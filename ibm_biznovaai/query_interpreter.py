import json
import re
from langchain_core.messages import HumanMessage, SystemMessage

def extract_valid_json_blocks(text):
    """
    Extracts all substrings from text that can be parsed as valid JSON.
    Returns a list of JSON strings.
    """
    valid_blocks = []
    # Use regex to find candidate JSON blocks (non-greedy match between { and })
    pattern = re.compile(r'\{[\s\S]*?\}')
    for match in pattern.finditer(text):
        candidate = match.group(0)
        try:
            # Try to parse the candidate to see if it is valid JSON.
            json.loads(candidate)
            valid_blocks.append(candidate)
        except json.JSONDecodeError:
            continue
    return valid_blocks

async def interpret_query(llm, query):
    """
    Interpret the user's natural language query into a structured format.
    """
    system_msg = """You are an expert query interpreter. Convert the user's query into JSON format specifying:
    
1. departments: Which datasets to query (teams, team_performance, sales, ratings, products, marketing, complaints, campaigns)
2. products: List of product IDs (e.g., PROD001-PROD007) if specified
3. metrics: Specific columns to retrieve
4. aggregation: How to process the data (sum, avg, count, list)

Return only the JSON and nothing else.

Example outputs:
For query "Total revenue for PROD001":
{
  "departments": ["sales"],
  "products": ["PROD001"],
  "metrics": ["net_revenue"],
  "aggregation": "sum"
}

For query "Complaints about PROD006":
{
  "departments": ["complaints"],
  "products": ["PROD006"],
  "metrics": ["issue_description"],
  "aggregation": "list"
}"""

    try:
        response = await llm.ainvoke([
            SystemMessage(content=system_msg),
            HumanMessage(content=query)
        ])
        response_text = (response if isinstance(response, str) else response.content).strip()

        # Debug: print raw response to inspect its format
        #print("DEBUG: Raw response from LLM:")
        #print(response_text)

        # Extract all valid JSON blocks from the response text.
        valid_blocks = extract_valid_json_blocks(response_text)
        if not valid_blocks:
            raise ValueError("No valid JSON block found in the response.")
        
        # For example, choose the last valid block (assuming that is the correct one).
        json_text = valid_blocks[-1]
        interpretation = json.loads(json_text)
        required_keys = {'departments', 'products', 'metrics', 'aggregation'}
        if not required_keys.issubset(interpretation.keys()):
            raise ValueError("Missing required fields in interpretation")
        return interpretation, None
    except Exception as e:
        return None, f"Interpretation failed: {str(e)}"
