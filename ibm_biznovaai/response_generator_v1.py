import json
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate

async def generate_response(llm, query, department_results):
    """
    Generate a comprehensive business report using the ReAct approach.
    The output includes a detailed chain-of-thought and a final answer.
    
    Args:
        llm: The language model instance.
        query (str): The original natural language query.
        department_results (dict): Processed data.
    
    Returns:
        A tuple (final_response, error) where error is None if successful.
    """
    if not department_results:
        return await fallback_response(llm, query)
    
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "You are a senior business analyst using the ReAct approach. First, think out loud and reason step-by-step about "
                "the data provided. Then, produce a final comprehensive report. Format your response as follows:\n\n"
                "Chain-of-Thought:\n"
                "[Your detailed reasoning here]\n\n"
                "Final Answer:\n"
                "[Your final report here]\n\n"
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
        response_text = response if isinstance(response, str) else response.content
        return response_text, None
    except Exception as e:
        return await fallback_response(llm, query)

async def fallback_response(llm, query):
    fallback_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            (
                "Using the ReAct approach, think out loud first and then provide a concise report. "
                "Output your chain-of-thought reasoning followed by the final answer in this format:\n\n"
                "Chain-of-Thought:\n"
                "[Your reasoning]\n\n"
                "Final Answer:\n"
                "[Your answer]"
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
