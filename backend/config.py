import os
from pathlib import Path
from dotenv import load_dotenv

# Try loading .env from backend folder first, then project root
backend_env = Path(__file__).parent / '.env'
root_env = Path(__file__).parent.parent / '.env'

if backend_env.exists():
    load_dotenv(dotenv_path=backend_env)
elif root_env.exists():
    load_dotenv(dotenv_path=root_env)
else:
    load_dotenv()  # Try default locations

NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")

TEMP_CLONE_DIR = os.getenv("TEMP_CLONE_DIR", "./temp_repos")

SUPPORTED_LANGUAGES = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
}

MAX_FILE_SIZE_BYTES = 1_000_000
MAX_FILES_PER_REPO = 5000
