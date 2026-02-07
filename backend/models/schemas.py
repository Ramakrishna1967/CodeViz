from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RepoNode(BaseModel):
    id: str
    name: str
    url: str
    analyzed_at: Optional[datetime] = None


class FileNode(BaseModel):
    path: str
    language: str
    size: int
    hash: str
    repo_id: str


class FunctionNode(BaseModel):
    name: str
    file_path: str
    start_line: int
    end_line: int
    params: str = ""
    return_type: str = ""
    repo_id: str


class ClassNode(BaseModel):
    name: str
    file_path: str
    start_line: int
    end_line: int
    repo_id: str


class GraphNode(BaseModel):
    id: str
    data: dict
    type: str
    style: Optional[dict] = None
    position: Optional[dict] = None


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "default"


class GraphData(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]


class AnalyzeRequest(BaseModel):
    github_url: str = Field(..., description="GitHub repository URL")


class AnalyzeResponse(BaseModel):
    repo_id: str
    status: str
    node_count: int


class ChatRequest(BaseModel):
    repo_id: str
    message: str


class ChatResponse(BaseModel):
    response: str
    references: list[dict] = []


class ExplainResponse(BaseModel):
    explanation: str
    code: str


class SearchResult(BaseModel):
    name: str
    type: str
    file_path: Optional[str] = None
    start_line: Optional[int] = None
    end_line: Optional[int] = None


class SearchResponse(BaseModel):
    results: list[SearchResult]
