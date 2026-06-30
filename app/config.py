import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "mock_data"

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3-groq-70b-8192-tool-use-preview")

MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "10"))
MAX_TOOL_ITERATIONS: int = int(os.getenv("MAX_TOOL_ITERATIONS", "3"))
