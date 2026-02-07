import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CodeViz AI",
    description="AI-powered codebase visualization and understanding platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    version: str


class AnalyzeRequest(BaseModel):
    github_url: str


class AnalyzeResponse(BaseModel):
    repo_id: str
    status: str
    node_count: int


class ChatRequest(BaseModel):
    repo_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    references: list[dict]


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    from parsers.treesitter import parse_repository
    from graph.neo4j_client import Neo4jClient
    
    try:
        neo4j = Neo4jClient()
        repo_id, nodes = await parse_repository(request.github_url, neo4j)
        return AnalyzeResponse(
            repo_id=repo_id,
            status="completed",
            node_count=len(nodes)
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/graph/{repo_id}")
async def get_graph(repo_id: str):
    from graph.neo4j_client import Neo4jClient
    from graph.queries import get_repo_graph
    
    try:
        neo4j = Neo4jClient()
        graph_data = await get_repo_graph(neo4j, repo_id)
        return graph_data
    except Exception as e:
        logger.error(f"Failed to fetch graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
async def chat_with_codebase(request: ChatRequest):
    from ai.gemini import GeminiClient
    from graph.neo4j_client import Neo4jClient
    
    try:
        neo4j = Neo4jClient()
        gemini = GeminiClient()
        response, refs = await gemini.answer_question(
            request.repo_id, 
            request.message, 
            neo4j
        )
        return ChatResponse(response=response, references=refs)
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/explain")
async def explain_code(repo_id: str, node_id: str):
    from ai.gemini import GeminiClient
    from graph.neo4j_client import Neo4jClient
    
    try:
        neo4j = Neo4jClient()
        gemini = GeminiClient()
        explanation, code = await gemini.explain_node(repo_id, node_id, neo4j)
        return {"explanation": explanation, "code": code}
    except Exception as e:
        logger.error(f"Explain failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
async def search_codebase(repo_id: str, query: str):
    from graph.neo4j_client import Neo4jClient
    from graph.queries import search_nodes
    
    try:
        neo4j = Neo4jClient()
        results = await search_nodes(neo4j, repo_id, query)
        return {"results": results}
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
