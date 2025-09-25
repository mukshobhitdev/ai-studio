
# Multiagent App

A modular Python application featuring multiple AI-powered agents for specialized tasks, including medical, research, stock market, travel, and document analysis. The project is designed for extensibility and easy integration of new agents and tools.

## Features

- **AI Agents**: Specialized agents for:
  - Medical information and data analysis
  - Research and literature review
  - Stock market data and analysis
  - Travel planning and recommendations
  - Document processing and summarization

- **Extensible Tools**: Each agent is supported by a set of tools for data retrieval, memory, and domain-specific operations.

- **SQLite Database**: Stores conversation history for context-aware interactions.

## Project Structure

```
ai_agents/
	doc_agent.py
	medical_agent.py
	research_agent.py
	stocks_agent.py
	travel_agent.py
data/
	medical_data.py
	stock_data.py
	travel_data.py
tools/
	doc_tools.py
	medical_tools.py
	memory_tools.py
	research_tools.py
	stocks_tools.py
	travel_tools.py
main.py
conversations.db
requirements.txt
```

- `ai_agents/`: Core agent logic for each domain.
- `data/`: Domain-specific datasets and data handling.
- `tools/`: Utility modules and tools for each agent.
- `main.py`: Application entry point.
- `conversations.db`: SQLite database for storing conversations.

## Getting Started

### Prerequisites

- Python 3.8+
- (Recommended) Create a virtual environment

### Installation

1. Clone the repository:
   ```powershell
   git clone <your-repo-url>
   cd multiagent_app
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv mulagentenv
   .\mulagentenv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Running the Application

```powershell
python main.py
```

## Adding New Agents or Tools

- Add new agent logic in `ai_agents/`.
- Add supporting tools in `tools/`.
- Register new agents and tools in `main.py`.

## License

[MIT License](LICENSE) (or specify your license)
