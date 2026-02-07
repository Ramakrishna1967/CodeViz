import os
import hashlib
import uuid
import shutil
import stat
import logging
from pathlib import Path
from typing import Optional
from git import Repo as GitRepo
import tree_sitter_python
import tree_sitter_javascript
import tree_sitter_typescript
from tree_sitter import Language, Parser

from config import TEMP_CLONE_DIR, SUPPORTED_LANGUAGES, MAX_FILE_SIZE_BYTES, MAX_FILES_PER_REPO
from graph.neo4j_client import Neo4jClient
from parsers.languages import get_language_config

logger = logging.getLogger(__name__)


def remove_readonly(func, path, excinfo):
    """Error handler for shutil.rmtree to handle read-only files on Windows"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

PARSERS = {}


def init_parsers():
    global PARSERS
    
    python_lang = Language(tree_sitter_python.language())
    js_lang = Language(tree_sitter_javascript.language())
    ts_lang = Language(tree_sitter_typescript.language_typescript())
    
    python_parser = Parser(python_lang)
    js_parser = Parser(js_lang)
    ts_parser = Parser(ts_lang)
    
    PARSERS = {
        "python": {"parser": python_parser, "language": python_lang},
        "javascript": {"parser": js_parser, "language": js_lang},
        "typescript": {"parser": ts_parser, "language": ts_lang},
    }


def get_parser(language: str):
    if not PARSERS:
        init_parsers()
    return PARSERS.get(language)


def extract_repo_name(github_url: str) -> str:
    url = github_url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    parts = url.split("/")
    return parts[-1] if parts else "unknown"


def clone_repository(github_url: str) -> tuple[str, str]:
    repo_id = str(uuid.uuid4())[:8]
    repo_name = extract_repo_name(github_url)
    clone_path = os.path.join(TEMP_CLONE_DIR, repo_id)
    
    os.makedirs(TEMP_CLONE_DIR, exist_ok=True)
    
    logger.info(f"Cloning {github_url} to {clone_path}")
    GitRepo.clone_from(github_url, clone_path, depth=1)
    
    return repo_id, clone_path


def get_file_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()[:16]


def get_language_from_extension(file_path: str) -> Optional[str]:
    ext = os.path.splitext(file_path)[1]
    return SUPPORTED_LANGUAGES.get(ext)


def collect_files(repo_path: str) -> list[dict]:
    files = []
    count = 0
    
    for root, dirs, filenames in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules" and d != "__pycache__"]
        
        for filename in filenames:
            if count >= MAX_FILES_PER_REPO:
                break
                
            file_path = os.path.join(root, filename)
            rel_path = os.path.relpath(file_path, repo_path)
            language = get_language_from_extension(filename)
            
            if not language:
                continue
                
            try:
                size = os.path.getsize(file_path)
                if size > MAX_FILE_SIZE_BYTES:
                    continue
                    
                with open(file_path, "rb") as f:
                    content = f.read()
                
                files.append({
                    "path": rel_path,
                    "full_path": file_path,
                    "language": language,
                    "size": size,
                    "hash": get_file_hash(content),
                    "content": content.decode("utf-8", errors="ignore")
                })
                count += 1
            except Exception as e:
                logger.warning(f"Failed to read {file_path}: {e}")
                
    return files


def parse_file(file_info: dict) -> dict:
    language = file_info["language"]
    content = file_info["content"]
    parser_info = get_parser(language)
    
    if not parser_info:
        return {"functions": [], "classes": [], "imports": [], "calls": []}
    
    parser = parser_info["parser"]
    lang = parser_info["language"]
    config = get_language_config(language)
    
    tree = parser.parse(content.encode())
    root = tree.root_node
    
    result = {
        "functions": [],
        "classes": [],
        "imports": [],
        "calls": []
    }
    
    result["functions"] = extract_functions(root, content, lang, config)
    result["classes"] = extract_classes(root, content, lang, config)
    result["imports"] = extract_imports(root, content, lang, config)
    result["calls"] = extract_calls(root, content, lang, config)
    
    return result


def extract_functions(root, content: str, lang, config: dict) -> list[dict]:
    functions = []
    query_str = config.get("function_query", "")
    if not query_str:
        return functions
        
    try:
        query = lang.query(query_str)
        captures = query.captures(root)
        
        current_func = {}
        for node, name in captures:
            if name == "function.name":
                current_func["name"] = content[node.start_byte:node.end_byte]
            elif name == "function.params":
                current_func["params"] = content[node.start_byte:node.end_byte]
            elif name == "function.return_type":
                current_func["return_type"] = content[node.start_byte:node.end_byte]
            elif name == "function.def":
                current_func["start_line"] = node.start_point[0] + 1
                current_func["end_line"] = node.end_point[0] + 1
                if current_func.get("name"):
                    functions.append({
                        "name": current_func.get("name", "anonymous"),
                        "params": current_func.get("params", "()"),
                        "return_type": current_func.get("return_type", ""),
                        "start_line": current_func["start_line"],
                        "end_line": current_func["end_line"]
                    })
                current_func = {}
    except Exception as e:
        logger.warning(f"Failed to extract functions: {e}")
        
    return functions


def extract_classes(root, content: str, lang, config: dict) -> list[dict]:
    classes = []
    query_str = config.get("class_query", "")
    if not query_str:
        return classes
        
    try:
        query = lang.query(query_str)
        captures = query.captures(root)
        
        current_class = {}
        for node, name in captures:
            if name == "class.name":
                current_class["name"] = content[node.start_byte:node.end_byte]
            elif name == "class.def":
                current_class["start_line"] = node.start_point[0] + 1
                current_class["end_line"] = node.end_point[0] + 1
                if current_class.get("name"):
                    classes.append({
                        "name": current_class["name"],
                        "start_line": current_class["start_line"],
                        "end_line": current_class["end_line"]
                    })
                current_class = {}
    except Exception as e:
        logger.warning(f"Failed to extract classes: {e}")
        
    return classes


def extract_imports(root, content: str, lang, config: dict) -> list[str]:
    imports = []
    query_str = config.get("import_query", "")
    if not query_str:
        return imports
        
    try:
        query = lang.query(query_str)
        captures = query.captures(root)
        
        for node, name in captures:
            import_text = content[node.start_byte:node.end_byte]
            import_text = import_text.strip("'\"")
            if import_text and import_text not in imports:
                imports.append(import_text)
    except Exception as e:
        logger.warning(f"Failed to extract imports: {e}")
        
    return imports


def extract_calls(root, content: str, lang, config: dict) -> list[str]:
    calls = []
    query_str = config.get("call_query", "")
    if not query_str:
        return calls
        
    try:
        query = lang.query(query_str)
        captures = query.captures(root)
        
        for node, name in captures:
            if name == "call.name":
                call_name = content[node.start_byte:node.end_byte]
                if call_name and call_name not in calls:
                    calls.append(call_name)
    except Exception as e:
        logger.warning(f"Failed to extract calls: {e}")
        
    return calls


async def parse_repository(github_url: str, neo4j: Neo4jClient) -> tuple[str, list]:
    import asyncio
    
    repo_name = extract_repo_name(github_url)
    loop = asyncio.get_event_loop()
    repo_id, clone_path = await loop.run_in_executor(None, clone_repository, github_url)
    
    try:
        await neo4j.create_repo_node(repo_id, repo_name, github_url)
        
        files = await loop.run_in_executor(None, collect_files, clone_path)
        logger.info(f"Found {len(files)} files to parse")
        
        all_nodes = []
        
        for file_info in files:
            await neo4j.create_file_node(
                repo_id,
                file_info["path"],
                file_info["language"],
                file_info["size"],
                file_info["hash"]
            )
            all_nodes.append({"type": "file", "path": file_info["path"]})
            
            parsed = await loop.run_in_executor(None, parse_file, file_info)
            
            for func in parsed["functions"]:
                await neo4j.create_function_node(
                    repo_id,
                    file_info["path"],
                    func["name"],
                    func["start_line"],
                    func["end_line"],
                    func["params"],
                    func.get("return_type", "")
                )
                all_nodes.append({"type": "function", "name": func["name"]})
            
            for cls in parsed["classes"]:
                await neo4j.create_class_node(
                    repo_id,
                    file_info["path"],
                    cls["name"],
                    cls["start_line"],
                    cls["end_line"]
                )
                all_nodes.append({"type": "class", "name": cls["name"]})
            
            for imp in parsed["imports"]:
                await neo4j.create_import_relationship(repo_id, file_info["path"], imp)
        
        logger.info(f"Created {len(all_nodes)} nodes for repo {repo_id}")
        return repo_id, all_nodes
        
    finally:
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, onerror=remove_readonly)
