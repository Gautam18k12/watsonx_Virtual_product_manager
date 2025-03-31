import json
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

async def generate_response(llm, query, department_results):
    """
    Generate a comprehensive business report based on the processed data.
    
    Args:
        llm: The language model instance.
        query (str): The original natural language query.
        department_results (dict): The processed data from departments.
    
    Returns:
        A tuple (final_response, error) where error is None if successful.
    """
    if not department_results:
        return await fallback_response(llm, query)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are a senior business analyst. Create a detailed report with these sections:\n\n"
                "1. KEY FINDINGS:\n"
                "   - Present all requested metrics clearly with proper formatting.\n"
                "   - Include comparisons and highlight key statistics.\n\n"
                "2. KEY INSIGHTS:\n"
                "   - Analyze what the numbers mean in a business context.\n"
                "   - Identify patterns, trends, and anomalies with potential causes.\n\n"
                "3. RECOMMENDATIONS:\n"
                "   - Provide 3-5 actionable business recommendations prioritized by impact.\n"
                "   - Include implementation considerations.\n\n"
                "4. CONCLUSION:\n"
                "   - Summarize key takeaways, suggest next steps, and share final thoughts.\n\n"
                "Data: {data}\n\n"
                "Current Date: {current_date}"
            )
        ),
        ("human", "Original Query: {query}")
    ])
    
    try:
        response = await (prompt | llm).ainvoke({
            "query": query,
            "data": json.dumps(department_results, indent=2),
            "current_date": datetime.now().strftime("%Y-%m-%d")
        })
        # Handle both cases: if response is a string, or if it's an object with a `content` attribute.
        response_text = response if isinstance(response, str) else response.content
        return response_text, None
    except Exception as e:
        return await fallback_response(llm, query)

async def fallback_response(llm, query):
    """
    Generate a fallback response by directly analyzing the query.
    
    Args:
        llm: The language model instance.
        query (str): The original query.
    
    Returns:
        A tuple (final_response, error) where error is None if successful.
    """
    fallback_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "Generate a concise business report with the following sections:\n"
                "1. KEY FINDINGS\n"
                "2. INSIGHTS\n"
                "3. RECOMMENDATIONS\n"
                "4. CONCLUSION\n\n"
                "If data is limited, provide high-level insights."
            )
        ),
        ("human", "Query: {query}")
    ])
    
    try:
        response = await (fallback_prompt | llm).ainvoke({
            "query": query
        })
        response_text = response if isinstance(response, str) else response.content
        return response_text, None
    except Exception as e:
        return f"An error occurred during fallback response generation: {str(e)}", str(e)
