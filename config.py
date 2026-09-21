import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
FRONTEND_URL=os.getenv("FRONTEND_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
TEST_DATABASE_URL=os.getenv("TEST_DATABASE_URL")
if not SECRET_KEY:
    raise ValueError("SECRET key is not configured")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured")
if not FRONTEND_URL:
    raise ValueError("FRONTEND_URL is not configured")
