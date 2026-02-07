from graph.neo4j_client import Neo4jClient
from graph.schema import NODE_COLORS


async def get_repo_graph(neo4j: Neo4jClient, repo_id: str) -> dict:
    nodes_query = """
    MATCH (r:Repo {id: $repo_id})
    OPTIONAL MATCH (r)-[:HAS_FILE]->(f:File)
    OPTIONAL MATCH (f)-[:CONTAINS]->(fn:Function)
    OPTIONAL MATCH (f)-[:CONTAINS]->(c:Class)
    RETURN 
        collect(DISTINCT {id: r.id, label: r.name, type: 'Repo'}) as repos,
        collect(DISTINCT {id: f.path, label: f.path, type: 'File', language: f.language}) as files,
        collect(DISTINCT {id: fn.name + ':' + fn.file_path, label: fn.name, type: 'Function', 
                         start_line: fn.start_line, end_line: fn.end_line}) as functions,
        collect(DISTINCT {id: c.name + ':' + c.file_path, label: c.name, type: 'Class',
                         start_line: c.start_line, end_line: c.end_line}) as classes
    """
    
    edges_query = """
    MATCH (r:Repo {id: $repo_id})-[:HAS_FILE]->(f:File)
    OPTIONAL MATCH (f)-[:CONTAINS]->(fn:Function)
    OPTIONAL MATCH (f)-[:CONTAINS]->(c:Class)
    OPTIONAL MATCH (c)-[:HAS_METHOD]->(m:Function)
    OPTIONAL MATCH (fn)-[:CALLS]->(called:Function)
    OPTIONAL MATCH (f)-[:IMPORTS]->(mod:Module)
    RETURN 
        collect(DISTINCT {source: r.id, target: f.path, type: 'HAS_FILE'}) as repo_files,
        collect(DISTINCT {source: f.path, target: fn.name + ':' + fn.file_path, type: 'CONTAINS'}) as file_functions,
        collect(DISTINCT {source: f.path, target: c.name + ':' + c.file_path, type: 'CONTAINS'}) as file_classes,
        collect(DISTINCT {source: c.name + ':' + c.file_path, target: m.name + ':' + m.file_path, type: 'HAS_METHOD'}) as class_methods,
        collect(DISTINCT {source: fn.name + ':' + fn.file_path, target: called.name + ':' + called.file_path, type: 'CALLS'}) as function_calls
    """

    nodes_result = await neo4j.execute_query(nodes_query, {"repo_id": repo_id})
    edges_result = await neo4j.execute_query(edges_query, {"repo_id": repo_id})
    
    nodes = []
    edges = []
    
    if not nodes_result or len(nodes_result) == 0:
        return {"nodes": [], "edges": []}
    
    if nodes_result:
        data = nodes_result[0]
        for repo in data.get("repos", []):
            if repo.get("id"):
                nodes.append({
                    "id": repo["id"],
                    "data": {"label": repo["label"]},
                    "type": "repo",
                    "style": {"backgroundColor": NODE_COLORS["Repo"]}
                })
        for file in data.get("files", []):
            if file.get("id"):
                nodes.append({
                    "id": file["id"],
                    "data": {"label": file["label"].split("/")[-1], "fullPath": file["label"]},
                    "type": "file",
                    "style": {"backgroundColor": NODE_COLORS["File"]}
                })
        for func in data.get("functions", []):
            if func.get("id"):
                nodes.append({
                    "id": func["id"],
                    "data": {"label": func["label"], "startLine": func.get("start_line"), "endLine": func.get("end_line")},
                    "type": "function",
                    "style": {"backgroundColor": NODE_COLORS["Function"]}
                })
        for cls in data.get("classes", []):
            if cls.get("id"):
                nodes.append({
                    "id": cls["id"],
                    "data": {"label": cls["label"], "startLine": cls.get("start_line"), "endLine": cls.get("end_line")},
                    "type": "class",
                    "style": {"backgroundColor": NODE_COLORS["Class"]}
                })

    if edges_result:
        data = edges_result[0]
        for edge_type in ["repo_files", "file_functions", "file_classes", "class_methods", "function_calls"]:
            for edge in data.get(edge_type, []):
                if edge.get("source") and edge.get("target"):
                    edges.append({
                        "id": f"{edge['source']}-{edge['target']}",
                        "source": edge["source"],
                        "target": edge["target"],
                        "type": edge.get("type", "default")
                    })

    return {"nodes": nodes, "edges": edges}


async def search_nodes(neo4j: Neo4jClient, repo_id: str, query: str) -> list:
    search_query = """
    MATCH (n)
    WHERE n.repo_id = $repo_id 
    AND (n.name CONTAINS $query OR n.path CONTAINS $query)
    RETURN n.name as name, labels(n)[0] as type, n.file_path as file_path,
           n.start_line as start_line, n.end_line as end_line
    LIMIT 50
    """
    results = await neo4j.execute_query(search_query, {"repo_id": repo_id, "query": query})
    return results


async def get_node_by_id(neo4j: Neo4jClient, repo_id: str, node_id: str) -> dict:
    query = """
    MATCH (n {repo_id: $repo_id})
    WHERE n.name + ':' + n.file_path = $node_id OR n.path = $node_id OR n.id = $node_id
    RETURN n, labels(n)[0] as type
    LIMIT 1
    """
    result = await neo4j.execute_query(query, {"repo_id": repo_id, "node_id": node_id})
    if result:
        return result[0]
    return {}
