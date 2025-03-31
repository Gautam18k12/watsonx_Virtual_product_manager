# AI-Powered Virtual Product Manager

## Overview
This project implements an **AI-powered Virtual Product Manager** using **IBM watsonx.ai**, **LangChain**, and **LangGraph**. The system utilizes a **multi-agent framework** to analyze business data across various domains like **sales, marketing, customer feedback, team performance, and product sentiment**.

It allows users to ask **natural language queries**, which are processed by AI agents to retrieve structured insights, generate reports, and provide data-driven recommendations.

## Key Features
- **Natural Language Query Interpretation:** Converts user queries into structured data retrieval requests.
- **Multi-Agent Processing:** Specialized agents handle different business functions.
- **Automated Insights & Recommendations:** AI-generated reports summarize findings and suggest actions.
- **Customizable & Scalable:** Can be adapted to different industries beyond e-commerce.

## Tech Stack
- **IBM watsonx.ai** (LLM-powered query interpretation & response generation)
- **LangChain & LangGraph** (Building agent workflows and chaining)
- **Pandas** (Data processing)
- **Python & AsyncIO** (Application logic & execution)

## Installation
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd <project-folder>
   ```
2. Install dependencies:
   ```sh
   pip install langchain langchain_community langgraph pandas langchain_experimental ibm_watson_machine_learning langchain-ibm
   ```
3. Add your **IBM watsonx.ai API Key & Project ID** in the `WatsonxLLM` configuration.

## How It Works
### 1. Load Datasets
- Reads and preprocesses CSV files for **ratings, complaints, sales, marketing, and team performance**.

### 2. Query Interpretation
- Uses **IBM watsonx.ai** to convert **natural language queries** into structured JSON format.

### 3. Data Processing
- Retrieves relevant data from **multiple datasets** based on query interpretation.
- Performs aggregations like **sum, average, count, and trend analysis**.

### 4. AI-Generated Reports
- Generates structured business reports covering:
  - **Key Findings** (summarized data)
  - **Insights** (trends & patterns)
  - **Recommendations** (actionable strategies)

### 5. Workflow Execution
- Uses **LangGraph** to manage execution flow:
  - **Interpret Query → Process Data → Generate Report → Return Response**

## Example Queries
```
Total revenue generated for PROD001 and PROD002
List of complaints received for PROD005
Average customer rating for all products
```

## Running the Project
Execute the Python script:
```sh
python virtual_pm_agenticai.py
```

## Future Enhancements
- **Integration with external BI tools**
- **Real-time data processing capabilities**
- **Automated alerting system for business-critical insights**

## Contributors
- **Gautam & Team (Tech Mahindra AI Hackathon)**

## License
This project is open-source under the **MIT License**.

