# CodeViz AI

AI-powered codebase visualization and understanding platform.

## Features

- Analyze any GitHub repository
- Interactive graph visualization with React Flow
- AI-powered chat to ask questions about the codebase
- Search functions and classes
- Code explanations powered by Gemini 2 Pro

## Tech Stack

**Frontend:**
- Next.js 15
- React 19
- TypeScript
- TailwindCSS
- React Flow

**Backend:**
- Python 3.12+
- FastAPI
- Tree-sitter (code parsing)
- Neo4j (graph database)
- Gemini 2 Pro API

## Project Structure

```
codeviz/
├── frontend/           # Next.js application
│   ├── app/           # Pages and layouts
│   ├── components/    # React components
│   └── lib/           # API client and utilities
├── backend/           # FastAPI server
│   ├── parsers/       # Tree-sitter code parsing
│   ├── graph/         # Neo4j client and queries
│   ├── ai/            # Gemini integration
│   └── models/        # Pydantic schemas
└── .env.example       # Environment variables template
```

## Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Neo4j Aura account (free tier)
- Gemini API key

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy .env.example to .env and fill in your credentials
cp ../.env.example .env

# Run the server
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
GEMINI_API_KEY=your_gemini_api_key
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/analyze` | POST | Analyze a GitHub repository |
| `/graph/{repo_id}` | GET | Get graph data for visualization |
| `/chat` | POST | Chat with AI about the codebase |
| `/explain` | GET | Get AI explanation for a code element |
| `/search` | GET | Search functions and classes |

## Usage

1. Open the app at `http://localhost:3000`
2. Paste a GitHub repository URL
3. Wait for analysis to complete
4. Explore the interactive graph
5. Click nodes to see code explanations
6. Use the chat to ask questions

## Supported Languages

- Python
- JavaScript
- TypeScript

## License

MIT
