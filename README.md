**CodeViz AI** is a tool designed to visualize and understand codebases by converting them into an interactive graph. It allows users to:
- **Visualize** the structure of a GitHub repository (files, classes, functions, dependencies).
- **Chat** with the codebase using AI (Gemini 2 Pro) which has context from the graph.
- **Search** and explore code elements.

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

---

# Advanced Architecture Maps

This section contains **technical diagrams** for CodeViz AI, ranging from the high-level system view to low-level internal logic.

## 1. The "Big Picture" (System Architecture)
This shows how the pieces fit together.

```mermaid
graph TD
    %% Styling - Black and White
    classDef default fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;

    User(["👤 User"])
    
    subgraph "Frontend (Vercel)"
        UI["💻 Next.js Website"]
    end
    
    subgraph "Backend (Render)"
        API["🐍 FastAPI Server"]
        Parser["⚙️ Tree-Sitter Engine"]
    end
    
    subgraph "Cloud Services"
        Neo4j["🗄️ Neo4j Graph DB"]
        Gemini["🧠 Gemini 1.5 Pro"]
        GitHub["☁️ GitHub"]
    end

    User -->|1. Pastes Repo URL| UI
    UI -->|2. Sends Request| API
    API -->|3. Clones Code| GitHub
    API -->|4. Parses Code| Parser
    Parser -->|5. Saves Graph| Neo4j
    
    User -->|6. Asks Question| UI
    UI -->|7. Chats| API
    API -->|8. Retrieves Context| Neo4j
    API -->|9. Generates Answer| Gemini
```

## 2. The "Analysis" Pipeline (High Level)
What happens when you click **"Analyze"**?

```mermaid
sequenceDiagram
    participant U as User
    participant BE as Backend
    participant GH as GitHub
    participant TS as Parser
    participant DB as Neo4j

    Note over U, DB: Step 1: Get the Code
    U->>BE: Click "Analyze" (URL)
    BE->>GH: git clone (Download Code)
    GH-->>BE: Returns Source Files

    Note over U, DB: Step 2: Understand the Code
    loop Every File
        BE->>TS: Read File Content
        TS-->>BE: Find Functions & Classes
        
        BE->>DB: CREATE "File" Node
        BE->>DB: CREATE "Function" Node
        BE->>DB: CREATE "CALLS" Relationship
    end

    Note over U, DB: Step 3: Cleanup
    BE->>BE: Delete Downloaded Files
    BE-->>U: "Analysis Complete!"
```

## 3. The Tree-Sitter Parsing Logic (AST Extraction)
How we turn raw text into a structured graph.

```mermaid
flowchart TD
    %% Styling - Black and White
    classDef default fill:#ffffff,stroke:#000000,stroke-width:2px,color:#000000;
    classDef process fill:#ffffff,stroke:#000000,stroke-width:2px,stroke-dasharray: 5 5;

    Start(["Start Parsing"]) --> Clone["git clone to /tmp"]
    Clone --> Walk["os.walk(repo_path)"]
    
    Walk --> FileCheck{"Is valid file?"}
    FileCheck -- "No/Ignored" --> Walk
    FileCheck -- "Yes" --> DetectLang["Detect Language .py, .js, .ts"]
    
    DetectLang --> ParserSelect{"Has Parser?"}
    ParserSelect -- "No" --> Skip["Skip File"]
    ParserSelect -- "Yes" --> Parse
    
    subgraph "Tree-Sitter Parsing Core"
        Parse["Parse into AST Root"]
        
        Parse --> Q_Func["Execute Query: function.name"]
        Q_Func --> Ext_Func["Extract: Name, Line #, Params"]
        
        Parse --> Q_Class["Execute Query: class.name"]
        Q_Class --> Ext_Class["Extract: Name, Line #"]
        
        Parse --> Q_Import["Execute Query: import.from"]
        Q_Import --> Ext_Imp["Extract: Module Name"]
        
        Parse --> Q_Call["Execute Query: call.name"]
        Q_Call --> Ext_Call["Extract: Callee Name"]
    end
    
    Ext_Func --> Neo4j["Batch Create Nodes in Neo4j"]
    Ext_Class --> Neo4j
    Neo4j --> Cleanup["Delete /tmp files"]:::process
    Cleanup --> End(["Finish"])
```

## 4. The RAG "Fusion" Pipeline
How we construct the prompts for Gemini using Graph Data.

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant BE as Backend (RAG)
    participant DB as Neo4j
    participant G as Gemini 2.0

    Note over U, G: Phase 1: Context Retrieval
    U->>BE: "How does auth work?"
    BE->>DB: MATCH (r:Repo)-[:HAS_FILE]->(f) RETURN f.path LIMIT 50
    DB-->>BE: List[Files]
    BE->>DB: MATCH (f)-[:CONTAINS]->(fn:Function) RETURN fn.name LIMIT 30
    DB-->>BE: List[Functions]
    BE->>DB: MATCH (f)-[:CONTAINS]->(c:Class) RETURN c.name LIMIT 20
    DB-->>BE: List[Classes]

    Note over U, G: Phase 2: Context Construction
    BE->>BE: Create System Prompt
    Note right of BE: "You are an AI Architect..."<br/>+ Context:<br/>- File: auth.py<br/>- Function: login()<br/>- Class: User
    
    Note over U, G: Phase 3: Generation & Referencing
    BE->>G: generate_content(System Prompt + User Question)
    G-->>BE: "Auth is handled in [auth.py:10-50]..."
    
    BE->>BE: Regex Parser (r'\[(.+):(\d+)-(\d+)\]')
    Note right of BE: Extracts references:<br/>{file: "auth.py", lines: 10-50}
    
    BE-->>U: Final Response + Clickable References
```

## 5. The Neo4j Graph Schema (Entity-Relationship)
The exact structure of the database nodes and edges.

```mermaid
erDiagram
    Repository ||--|{ FileNode : "HAS_FILE"
    FileNode ||--o{ FunctionNode : "CONTAINS"
    FileNode ||--o{ ClassNode : "CONTAINS"
    FileNode ||--o{ ModuleNode : "IMPORTS"
    
    ClassNode ||--o{ FunctionNode : "HAS_METHOD"
    FunctionNode }o--o{ FunctionNode : "CALLS"

    Repository {
        string id
        string name
        string url
    }
    
    FileNode {
        string path
        string language
        int size
        string hash
    }
    
    FunctionNode {
        string name
        int start_line
        int end_line
        string params
        string return_type
    }
    
    ClassNode {
        string name
        int start_line
        int end_line
    }
    
    ModuleNode {
        string name
    }
```
=======
>>>>>>> 8ef95f5457e03e5a4957d4d5cf3c609e2b2facc5
