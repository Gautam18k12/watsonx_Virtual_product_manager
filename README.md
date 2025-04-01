# IBM_BizNovaAI: Virtual Product Manager

IBM_BizNovaAI is a hackathon project that leverages WatsonX, LangChain, and LangGraph to build an agentic AI-based virtual product manager. The system interprets natural language queries, processes data from multiple sources, and generates detailed business reports using a ReAct (Reasoning and Acting) approach. Additionally, the project includes functionality to visualize the workflow graph.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Workflow Diagram](#workflow-diagram)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

IBM_BizNovaAI is designed to help businesses analyze various aspects of their performance—such as sales, ratings, complaints, marketing activities, team performance, and more—by interpreting natural language queries and generating comprehensive reports. The system leverages advanced AI capabilities to explain its reasoning (via ReAct) and provide actionable insights.

---

## Features

- **Natural Language Query Interpretation:** Converts queries into structured JSON commands.
- **Data Processing:** Loads and preprocesses multiple datasets (sales, ratings, products, marketing, complaints, campaigns, teams, team performance).
- **Department-Specific Analysis:** Filters and aggregates data based on query specifications.
- **Report Generation:** Uses a ReAct approach to display the chain-of-thought reasoning and final business report.
- **Workflow Visualization:** Option to generate a diagram of the workflow using either Graphviz or alternative methods (e.g., NetworkX with Matplotlib).
- **Environment Configuration:** Securely manage API keys and settings with a `.env` file.

---

## Project Structure

```
watsonx_Virtual_product_manager/
├── ibm_biznovaai/
│   ├── __init__.py
│   ├── data_processing.py         # Loads and preprocesses CSV datasets.
│   ├── query_interpreter.py       # Interprets natural language queries.
│   ├── department_processor.py    # Processes department-specific data.
│   ├── response_generator.py      # Generates the final report with ReAct.
│   ├── main.py                    # Main entry point for running the application.
│   └── plot_workflow.py           # Script to generate a workflow diagram.
├── data/                          # Folder containing CSV data files.
│   ├── Teams_data.csv
│   ├── TeamPerformance_data.csv
│   ├── sales_data.csv
│   ├── ratings.csv
│   ├── Products_data.csv
│   ├── Marketing_data.csv
│   ├── Complaints_Data.csv
│   └── Campaigns_data.csv
├── tests/                         # (Optional) Unit tests for the modules.
├── .env                           # Environment file for credentials and configuration.
├── requirements.txt               # Python dependencies.
└── README.md                      # Project documentation.
```

---

## Requirements

- **Python 3.8+**
- **WatsonX API credentials**
- **Graphviz** (optional, for workflow visualization)
- Python packages (see [requirements.txt](requirements.txt)):
  - `langchain`
  - `langchain_community`
  - `langgraph`
  - `pandas`
  - `langchain_experimental`
  - `ibm_watson_machine_learning`
  - `langchain-ibm`
  - `python-dotenv`
  - `graphviz` (if using Graphviz for diagram rendering)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/gautam18k12/watsonx_Virtual_product_manager.git
   cd watsonx_Virtual_product_manager
   ```

2. **Create and Activate a Virtual Environment:**

   - **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Environment Variables:**

   Create a `.env` file in the project root with your WatsonX and project configuration:

   ```dotenv
   API_KEY=your_actual_api_key_here
   PROJECT_ID=your_actual_project_id_here
   MODEL_ID=ibm/granite-3-8b-instruct
   URL=https://us-south.ml.cloud.ibm.com
   TEMPERATURE=0.7
   MIN_NEW_TOKENS=5
   MAX_NEW_TOKENS=1000
   DECODING_METHOD=greedy
   ```

2. **Data Files:**

   Place your CSV files in the `data/` folder ensuring the filenames match those referenced in `data_processing.py`.

---

## Usage

### Running the Application

To run the interactive application, execute:

```bash
python -m ibm_biznovaai.main
```

You will be prompted to enter your query at runtime. The system will process your query, log the progress of each agent (e.g., Query Interpreter, Department Processor, Response Generator), and display the final report.

### Example Query

```
Total revenue generated for PROD001 and PROD002
```

---

## Workflow Diagram

To visualize the workflow graph:

1. **Using Graphviz:**
   - Ensure Graphviz is installed and its executables are added to your system’s PATH.
   - Run:
     ```bash
     python -m ibm_biznovaai.plot_workflow
     ```
   - This will generate a `workflow.dot` file and render an image (e.g., `workflow.png`).

2. **Alternative Visualization:**
   - If Graphviz is not available, consider modifying `plot_workflow.py` to use NetworkX and Matplotlib.

---

## Testing

You can write tests for each module in the `tests/` directory using frameworks like `pytest` or Python's built-in `unittest`. To run tests with pytest:

```bash
pytest tests/
```

---

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with detailed descriptions of your changes. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- [WatsonX](https://www.ibm.com/cloud/watsonx)
- [LangChain](https://github.com/hwchase17/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [Graphviz](https://graphviz.org/)
