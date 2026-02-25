# SG Transport Route Recommender

An AI-powered Singapore transport route recommender built with Google Gemini ADK and Streamlit. Enter any two locations in Singapore and get comprehensive route recommendations across all transport modes.

## Features

- **MRT/LRT Routes** — Station-to-station directions, line transfers, fares (EZ-Link/SimplyGo)
- **Bus Routes** — SBS Transit/SMRT bus services, stop numbers, fare estimates
- **Taxi & Ride-Hailing** — Metered taxi fares, Grab/Gojek estimates, ERP surcharges
- **Cycling & Walking** — Distance, time estimates, park connectors, shared bike availability

All results are compiled into a comparison table with a recommended best route.

## Tech Stack

- **[Google Gemini ADK](https://github.com/google/adk-python)** — Multi-agent orchestration with Gemini 2.5 Flash
- **[Streamlit](https://streamlit.io/)** — Web UI
- **[uv](https://github.com/astral-sh/uv)** — Python package management

## Architecture

```
root_agent (travel_agent)
└── transport_workflow_agent (SequentialAgent)
    ├── mrt_agent          — MRT/LRT routes & fares
    ├── bus_agent           — Public bus routes & fares
    ├── taxi_agent          — Taxi & Grab/Gojek fares
    └── cycle_walk_agent    — Cycling & walking options
```

Each sub-agent uses Google Search to fetch real-time Singapore transport data.

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)
- A Google API key with Gemini API access

### Installation

```bash
git clone https://github.com/alfredang/sgtransport.git
cd sgtransport
uv sync
```

### Configuration

Create a `.env` file in the project root:

```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_google_api_key_here
```

### Run

```bash
uv run streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## Usage

1. Enter a **Start Location** (e.g. Jurong East)
2. Enter an **End Location** (e.g. Changi Airport)
3. Click **Find Best Route**
4. Review the comparison table and recommended route

## License

MIT
