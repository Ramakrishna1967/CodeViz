# CodeViz AI - The Complete Guide

## 1. High-Level Architecture
**CodeViz AI** is a bridge between your codebase and your understanding. It turns lines of code into a navigable map and an intelligent conversation partner.

```mermaid
graph TD
    User([User])
    subgraph "Frontend (Next.js)"
        UI[Web Interface]
        GraphVis[Graph Visualizer]
        ChatUI[Chat Panel]
    end
    
    subgraph "Backend (FastAPI)"
        API[API Gateway]
        Parser[Tree-sitter Parser]
        RAG[RAG Engine]
    end
    
    subgraph "Information Storage"
        DB[(Neo4j Graph DB)]
        LLM[Gemini 2 Pro]
    end

    User -->|1. Paste URL| UI
    UI -->|2. Request Analysis| API
    API -->|3. Clone & Scan| Parser
    Parser -->|4. Store Nodes| DB
    
    User -->|5. Ask Question| ChatUI
    ChatUI -->|6. Chat Request| API
    API -->|7. Retrieve Context| DB
    API -->|8. Generate Answer| LLM
```

---

## 2. Core Workflow: From Code to Graph (The "Analyze" Process)
This is what happens when you click "Analyze". It's a pipeline that transforms raw text into a structured knowledge graph.

```mermaid
sequenceDiagram
    participant U as User
    participant BE as Backend (FastAPI)
    participant FS as File System
    participant TS as Tree-sitter (Parser)
    participant DB as Neo4j

    U->>BE: POST /analyze (github_url)
    BE->>FS: git clone (to temp_repos/)
    BE->>DB: Create (Repo) Node
    
    loop Every File in Repo
        BE->>FS: Read File
        BE->>TS: Parse Syntax Tree (AST)
        TS-->>BE: Extract Functions, Classes, Calls
        
        BE->>DB: MERGE (File) Node
        BE->>DB: MERGE (Function) Nodes
        BE->>DB: MERGE Relationships (CALLS, IMPORTS)
    end
    
    BE->>FS: Delete temp files
    BE-->>U: Analysis Complete {repo_id}
```

**Explanation:**
1.  **Clone**: The server temporarily downloads the code.
2.  **Parse**: It uses `Tree-sitter`, a library that understands code syntax. It doesn't just read lines; it understands "This is a function named `process_data` taking arguments `x` and `y`".
3.  **Graphing**: It pushes these entities to Neo4j. If `Function A` calls `Function B`, a physical link is created in the database.

---

## 3. Core Workflow: RAG Chat (The "Ask" Process)
How does the AI know about *your* specific code? It uses **Retrieval Augmented Generation (RAG)**.

```mermaid
flowchart LR
    Question[User Question] --> API
    API -->|1. Search| DB[(Neo4j)]
    DB -->|2. Return Context| Context[Relevant Files & Functions]
    
    Context --> Prompt
    Question --> Prompt
    
    Prompt[Combined Prompt] --> LLM[Gemini 2 Pro]
    LLM -->|3. Answer| Response
    Response --> User
```

**Why this matters:**
Standard ChatGPT doesn't know your private code. CodeViz fixes this by looking up the *exact* functions and classes related to your question in the Graph Database and feeding them to Gemini before it answers.

---

## 4. The Data Model (Graph Schema)
This is how your code is stored in the database.

```mermaid
classDiagram
    class Repo {
        url
        name
    }
    class File {
        path
        language
    }
    class Class {
        name
        start_line
    }
    class Function {
        name
        params
        return_type
    }
    
    Repo "1" --> "*" File : HAS_FILE
    File "1" --> "*" Class : CONTAINS
    File "1" --> "*" Function : CONTAINS
    Class "1" --> "*" Function : HAS_METHOD
    Function "*" --> "*" Function : CALLS
    File "*" --> "*" File : IMPORTS
```

---

## 5. Technical Deep Dive (Key Components)

### Backend (`/backend`)
*   **`main.py`**: The traffic controller. It receives requests and delegates them.
*   **`parsers/treesitter.py`**: The "Translator". It converts raw text (code) into data (functions/classes).
*   **`graph/neo4j_client.py`**: The "Librarian". It knows how to organize this data into the shelf (database) so it can be found later.

### Frontend (`/frontend`)
*   **`GraphViewer.tsx`**: The "Map". uses React Flow to draw the nodes. It calculates layout so files look like a grid and functions sit inside them.
*   **`ChatPanel.tsx`**: The "Interface". It handles the conversation state and streaming responses.

