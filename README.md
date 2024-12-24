# SQL Injection Analysis Agent

An intelligent multi-agent system designed to explore SQL injection vulnerabilities in web applications, specifically targeting WebGoat v2023.8. This project is part of the B649/I590 Cyber Defense course.

## Features

- Autonomous SQL injection vulnerability exploration
- Pattern-based table and column analysis
- Priority-based search strategy
- Intelligent response analysis
- Comprehensive error handling

## Prerequisites

- Python 3.8+
- WebGoat v2023.8
- OpenAI API Key

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:
```env
OPENAI_API_KEY=your_api_key_here
HOST=127.0.0.1  # Default WebGoat host
PORT=8080       # Default WebGoat port
WEBGOAT=your_webgoat_session_cookie
```

## Project Structure

```
/
├── sql_injection_tools/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── table_enumerator.py  # Database table discovery
│   ├── column_enumerator.py # Table column analysis
│   └── data_extractor.py    # Data extraction tools
├── sql_injection_agent.py   # Main agent implementation
├── requirements.txt         # Project dependencies
└── .env                     # Environment configuration
```

## Usage

Run the main agent:
```bash
python sql_injection_agent.py
```

## Features

- Multi-agent LLM-powered system using LangChain
- Intelligent pattern matching for database structure analysis
- Priority-based table exploration
- Comprehensive error handling and logging
- Safe mode for payload generation

## Presentation Video

[![SQL Injection Agent Presentation](https://img.youtube.com/vi/O9Bq4YBJCsw/0.jpg)](https://youtu.be/O9Bq4YBJCsw)

Click the image above to watch the project presentation and demonstration.

## Security Notes

- This tool is for educational purposes only
- Only use on systems you have permission to test
- Follow ethical hacking practices
- Do not use on production systems

## Dependencies

- langchain
- langchain-openai
- openai
- python-dotenv
- requests

## License

For educational use only. Part of B649/I590 Cyber Defense course.
