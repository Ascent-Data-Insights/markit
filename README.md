# Markit

A client research and lead generation tool for Ascent Data Insights.

## Description

Markit helps find and research potential clients in the Greater Cincinnati area for data science consulting services. It uses AI-powered web search to identify prospects and gather detailed research about them.

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

1. Install uv if you haven't already:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:

   ```bash
   git clone <repository-url>
   cd markit
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Set up environment variables with a .env file:
   ```bash
   ANTHROPIC_API_KEY="your-anthropic-api-key"
   ```

## Usage

### Search and Research New Clients

Find new potential clients and optionally research them:

```bash
uv run --env-file .env python main.py search-and-research
```
Optional arguments:
- `"--ai-interface`: To specify the AI interface to use (`anthropic` or `perplexity`). Default is `perplexity`.

### Research a Specific Organization

Research a specific organization by name:

```bash
uv run --env-file .env python main.py research "Company Name"
```
Optional arguments:
- `"--ai-interface`: To specify the AI interface to use (`anthropic` or `perplexity`). Default is `perplexity`.

## Requirements

- Python 3.12+
- Anthropic API key -or- Perplexity API key

## Output

Research results are saved as CSV files:

- `search-and-research` command saves to `research_results_YYYYMMDD_HHMMSS.csv`
- `research` command saves to `{organization_name}_research.csv`
