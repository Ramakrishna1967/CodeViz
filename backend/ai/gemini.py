import logging
import asyncio
from typing import Optional
import google.generativeai as genai

from config import GEMINI_API_KEY
from ai.prompts import ANSWER_QUESTION, EXPLAIN_CODE, SUMMARIZE_CODEBASE
from graph.neo4j_client import Neo4jClient
from graph.queries import get_node_by_id

logger = logging.getLogger(__name__)


class GeminiClient:
    _instance: Optional["GeminiClient"] = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY must be set")
        genai.configure(api_key=GEMINI_API_KEY)
        self._model = genai.GenerativeModel("gemini-2.0-flash")
        logger.info("Gemini client initialized")

    async def generate(self, prompt: str) -> str:
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                self._model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            raise

    async def get_codebase_context(self, neo4j: Neo4jClient, repo_id: str) -> str:
        query = """
        MATCH (r:Repo {id: $repo_id})
        OPTIONAL MATCH (r)-[:HAS_FILE]->(f:File)
        OPTIONAL MATCH (f)-[:CONTAINS]->(fn:Function)
        OPTIONAL MATCH (f)-[:CONTAINS]->(c:Class)
        RETURN r.name as repo_name,
               collect(DISTINCT f.path) as files,
               collect(DISTINCT {name: fn.name, file: fn.file_path, type: 'function'}) as functions,
               collect(DISTINCT {name: c.name, file: c.file_path, type: 'class'}) as classes
        """
        result = await neo4j.execute_query(query, {"repo_id": repo_id})
        
        if not result:
            return "No codebase information available."
        
        data = result[0]
        files = [f for f in data.get("files", []) if f]
        functions = [f for f in data.get("functions", []) if f.get("name")]
        classes = [c for c in data.get("classes", []) if c.get("name")]
        
        context_parts = [
            f"Repository: {data.get('repo_name', 'Unknown')}",
            f"\nFiles ({len(files)}):",
        ]
        
        for f in files[:50]:
            context_parts.append(f"  - {f}")
        
        if functions:
            context_parts.append(f"\nFunctions ({len(functions)}):")
            for fn in functions[:30]:
                context_parts.append(f"  - {fn['name']} in {fn['file']}")
        
        if classes:
            context_parts.append(f"\nClasses ({len(classes)}):")
            for c in classes[:20]:
                context_parts.append(f"  - {c['name']} in {c['file']}")
        
        return "\n".join(context_parts)

    async def answer_question(self, repo_id: str, question: str, neo4j: Neo4jClient) -> tuple[str, list]:
        context = await self.get_codebase_context(neo4j, repo_id)
        
        repo_query = "MATCH (r:Repo {id: $repo_id}) RETURN r.name as name"
        repo_result = await neo4j.execute_query(repo_query, {"repo_id": repo_id})
        repo_name = repo_result[0]["name"] if repo_result else "Unknown"
        
        prompt = ANSWER_QUESTION.format(
            repo_name=repo_name,
            context=context,
            question=question
        )
        
        response = await self.generate(prompt)
        
        references = self._extract_references(response)
        
        return response, references

    async def explain_node(self, repo_id: str, node_id: str, neo4j: Neo4jClient) -> tuple[str, str]:
        node_data = await get_node_by_id(neo4j, repo_id, node_id)
        
        if not node_data:
            return "Node not found.", ""
        
        node = node_data.get("n", {})
        node_type = node_data.get("type", "unknown")
        
        file_path = node.get("file_path", node.get("path", ""))
        element_name = node.get("name", file_path)
        start_line = node.get("start_line", 1)
        end_line = node.get("end_line", 1)
        
        code = f"[Code from {file_path}:{start_line}-{end_line}]"
        
        language = "python"
        if file_path.endswith((".js", ".jsx")):
            language = "javascript"
        elif file_path.endswith((".ts", ".tsx")):
            language = "typescript"
        
        prompt = EXPLAIN_CODE.format(
            file_path=file_path,
            element_name=element_name,
            element_type=node_type,
            start_line=start_line,
            end_line=end_line,
            language=language,
            code=code,
            context="Part of the analyzed codebase"
        )
        
        explanation = await self.generate(prompt)
        
        return explanation, code

    def _extract_references(self, text: str) -> list[dict]:
        import re
        references = []
        pattern = r'\[([^:]+):(\d+)-(\d+)\]'
        matches = re.findall(pattern, text)
        
        for match in matches:
            references.append({
                "file": match[0],
                "start_line": int(match[1]),
                "end_line": int(match[2])
            })
        
        return references
