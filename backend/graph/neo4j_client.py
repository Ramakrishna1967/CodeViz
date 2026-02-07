from neo4j import AsyncGraphDatabase
from typing import Optional
import logging
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

logger = logging.getLogger(__name__)


class Neo4jClient:
    _instance: Optional["Neo4jClient"] = None
    _driver = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not NEO4J_URI or not NEO4J_PASSWORD:
            raise ValueError("NEO4J_URI and NEO4J_PASSWORD must be set")
        self._driver = AsyncGraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        logger.info("Neo4j driver initialized")

    async def close(self):
        if self._driver:
            await self._driver.close()

    async def execute_query(self, query: str, parameters: dict = None):
        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            return await result.data()

    async def execute_write(self, query: str, parameters: dict = None):
        async with self._driver.session() as session:
            result = await session.run(query, parameters or {})
            summary = await result.consume()
            return summary.counters

    async def create_repo_node(self, repo_id: str, name: str, url: str):
        query = """
        MERGE (r:Repo {id: $repo_id})
        SET r.name = $name, r.url = $url, r.analyzed_at = datetime()
        RETURN r
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "name": name,
            "url": url
        })

    async def create_file_node(self, repo_id: str, path: str, language: str, size: int, content_hash: str):
        query = """
        MATCH (r:Repo {id: $repo_id})
        MERGE (f:File {path: $path, repo_id: $repo_id})
        SET f.language = $language, f.size = $size, f.hash = $content_hash
        MERGE (r)-[:HAS_FILE]->(f)
        RETURN f
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "path": path,
            "language": language,
            "size": size,
            "content_hash": content_hash
        })

    async def create_function_node(self, repo_id: str, file_path: str, name: str, 
                                    start_line: int, end_line: int, params: str, return_type: str):
        query = """
        MATCH (f:File {path: $file_path, repo_id: $repo_id})
        MERGE (fn:Function {name: $name, file_path: $file_path, repo_id: $repo_id})
        SET fn.start_line = $start_line, fn.end_line = $end_line,
            fn.params = $params, fn.return_type = $return_type
        MERGE (f)-[:CONTAINS]->(fn)
        RETURN fn
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "file_path": file_path,
            "name": name,
            "start_line": start_line,
            "end_line": end_line,
            "params": params,
            "return_type": return_type
        })

    async def create_class_node(self, repo_id: str, file_path: str, name: str,
                                 start_line: int, end_line: int):
        query = """
        MATCH (f:File {path: $file_path, repo_id: $repo_id})
        MERGE (c:Class {name: $name, file_path: $file_path, repo_id: $repo_id})
        SET c.start_line = $start_line, c.end_line = $end_line
        MERGE (f)-[:CONTAINS]->(c)
        RETURN c
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "file_path": file_path,
            "name": name,
            "start_line": start_line,
            "end_line": end_line
        })

    async def create_method_relationship(self, repo_id: str, class_name: str, 
                                          function_name: str, file_path: str):
        query = """
        MATCH (c:Class {name: $class_name, file_path: $file_path, repo_id: $repo_id})
        MATCH (fn:Function {name: $function_name, file_path: $file_path, repo_id: $repo_id})
        MERGE (c)-[:HAS_METHOD]->(fn)
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "class_name": class_name,
            "function_name": function_name,
            "file_path": file_path
        })

    async def create_call_relationship(self, repo_id: str, caller_name: str, 
                                        callee_name: str, caller_file: str):
        query = """
        MATCH (caller:Function {name: $caller_name, file_path: $caller_file, repo_id: $repo_id})
        MATCH (callee:Function {name: $callee_name, repo_id: $repo_id})
        MERGE (caller)-[:CALLS]->(callee)
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "caller_name": caller_name,
            "callee_name": callee_name,
            "caller_file": caller_file
        })

    async def create_import_relationship(self, repo_id: str, file_path: str, module_name: str):
        query = """
        MATCH (f:File {path: $file_path, repo_id: $repo_id})
        MERGE (m:Module {name: $module_name, repo_id: $repo_id})
        MERGE (f)-[:IMPORTS]->(m)
        """
        return await self.execute_write(query, {
            "repo_id": repo_id,
            "file_path": file_path,
            "module_name": module_name
        })
