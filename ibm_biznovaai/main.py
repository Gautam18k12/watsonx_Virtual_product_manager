import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from ibm_biznovaai import data_processing, query_interpreter, department_processor, response_generator

# Import the required WatsonX LLM and configuration details.
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from langchain_ibm import WatsonxLLM

# Retrieve credentials and configuration from environment variables
API_KEY = os.getenv("API_KEY")
PROJECT_ID = os.getenv("PROJECT_ID")
MODEL_ID = os.getenv("MODEL_ID", "ibm/granite-3-8b-instruct")
URL = os.getenv("URL")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.7))
MIN_NEW_TOKENS = int(os.getenv("MIN_NEW_TOKENS", 5))
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", 1000))
DECODING_METHOD = os.getenv("DECODING_METHOD", "greedy")

# Initialize your WatsonX LLM with environment variables
llm = WatsonxLLM(
    model_id=MODEL_ID,
    url=URL,
    apikey=API_KEY,
    project_id=PROJECT_ID,
    params={
        GenParams.DECODING_METHOD: DECODING_METHOD,
        GenParams.TEMPERATURE: TEMPERATURE,
        GenParams.MIN_NEW_TOKENS: MIN_NEW_TOKENS,
        GenParams.MAX_NEW_TOKENS: MAX_NEW_TOKENS,
    },
)

# Load datasets once at startup.
datasets = data_processing.load_datasets()

async def execute_query(query: str):
    """
    Execute the full analysis pipeline: interpret query, process departments, and generate response.
    This function prints real-time progress messages so the user sees which agent is active.
    """
    # Query Interpretation Agent
    print("Agent: Query Interpreter is thinking...", flush=True)
    interpretation, error = await query_interpreter.interpret_query(llm, query)
    if error:
        print("Error in query interpretation:", error, flush=True)
        return f"Error in query interpretation: {error}"
    print("Agent: Query Interpreter completed.", flush=True)

    # Department Processing Agent
    print("Agent: Department Processor is processing data...", flush=True)
    department_results, error = department_processor.process_departments(datasets, interpretation)
    if error:
        print("Error in processing departments:", error, flush=True)
        return f"Error in processing departments: {error}"
    print("Agent: Department Processor completed.", flush=True)

    # Response Generation Agent
    print("Agent: Response Generator is generating response...", flush=True)
    final_response, error = await response_generator.generate_response(llm, query, department_results)
    if error:
        print("Error in generating response:", error, flush=True)
        return f"Error in generating response: {error}"
    print("Agent: Response Generator completed.", flush=True)

    return final_response

def main():
    """
    Main entry point for running the application.
    Prompts the user for a query at runtime and displays progress messages along with the final response.
    """
    async def run_query():
        print("=" * 60)
        print("BUSINESS ANALYTICS REPORTING SYSTEM")
        print("=" * 60)
        # Prompt the user for input
        query = input("Please enter your query: ").strip()
        if not query:
            print("No query provided. Exiting.")
            return
        print("\n" + "-" * 60)
        print(f"QUERY: {query}")
        print("-" * 60)
        response = await execute_query(query)
        print("\nFINAL RESPONSE:")
        print(response)
        print("-" * 60)

    # Run the asynchronous query.
    try:
        asyncio.run(run_query())
    except RuntimeError as e:
        # Fallback if an event loop is already running (e.g., in some notebook environments)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_query())

if __name__ == "__main__":
    main()
