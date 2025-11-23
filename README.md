# InnoCore AI - 研创·智核

Intelligent Research Innovation Assistant based on HelloAgent framework

## Quick Start

### 1. Installation

```bash
# Install core dependencies
python install.py

# Or install manually
pip install fastapi uvicorn python-multipart python-dotenv pydantic httpx requests
```

### 2. Configuration

Create `.env` file:
```bash
cp .env.example .env
# Edit .env file and add your OpenAI API key
```

### 3. Run Application

```bash
python run.py
```

### 4. Access

- Main Application: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Features

- 🕵️ **Hunter Agent**: Literature search and monitoring
- 🧠 **Miner Agent**: Deep paper analysis and insight extraction
- ✍️ **Coach Agent**: Writing assistance and style improvement
- 🔎 **Validator Agent**: Citation verification and formatting

## Project Structure

```
innocore_ai/
├── agents/          # AI agents
├── api/            # REST API routes
├── core/           # Core functionality
├── models/         # Data models
├── services/       # Business logic
├── utils/          # Utilities
├── frontend/       # Web interface
├── main.py         # Main application entry
├── run.py          # Simple run script
├── install.py      # Installation script
└── requirements-core.txt  # Core dependencies
```

## Requirements

- Python 3.8+
- OpenAI API key
- Redis (optional, for caching)

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
python run.py
```

## License

MIT License