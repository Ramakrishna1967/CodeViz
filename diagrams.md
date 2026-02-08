# CodeViz AI - Project Diagrams

## 1. System Architecture

```mermaid
graph TD
    User((User))
    
    subgraph "Frontend"
        Web[Next.js Website]
    end
    
    subgraph "Backend"
        API[FastAPI Server]
        Parser[Code Parser]
    end
    
    subgraph "Data & AI"
        DB[(Graph Database)]
        AI[Gemini AI]
    end
    
    User -->|Uses| Web
    Web <-->|API Calls| API
    API -->|Sends Code| Parser
    Parser -->|Saves Graph| DB
    API <-->|Reads Data| DB
    API <-->|Asks Questions| AI
```

## 2. Analysis Workflow

```mermaid
sequenceDiagram
    actor User
    participant Web
    participant API
    participant DB
    
    User->>Web: Input GitHub URL
    Web->>API: Start Analysis
    
    Note right of API: Steps happen in seconds
    API->>API: 1. Download Code
    API->>API: 2. Parse Files
    API->>DB: 3. Save to Graph
    
    API-->>Web: Analysis Complete
    Web-->>User: Show Graph
```

## 3. Chat Workflow

```mermaid
flowchart LR
    Q[User Question] --> Search
    Search[Search Database] --> Context
    Context[Found Code] --> Prompt
    Prompt[Combine Question + Code] --> AI
    AI[Gemini AI] --> Answer
    Answer[Final Answer]
```

## 4. Data Structure

```mermaid
erDiagram
    REPO ||--|{ FILE : contains
    FILE ||--o{ FUNCTION : defines
    FILE ||--o{ CLASS : defines
    CLASS ||--o{ FUNCTION : has_method
    
    REPO { string name }
    FILE { string path }
    FUNCTION { string name }
    CLASS { string name }
```
