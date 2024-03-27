from dotenv import load_dotenv
load_dotenv()

import os
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
SERVER_HOST = os.getenv('SERVER_HOST') or '0.0.0.0'
SERVER_PORT = int(os.getenv('SERVER_PORT') or '80')
