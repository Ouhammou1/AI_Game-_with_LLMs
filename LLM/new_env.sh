# 1️⃣ Install Python 3.11 (if not already installed)
brew install python@3.11

# 2️⃣ Define environment path
ENV_PATH="/Users/bouhammo/goinfre/new_env"

# 3️⃣ Create virtual environment at that path
python3.11 -m venv "$ENV_PATH"

# 4️⃣ Activate environment
source "$ENV_PATH/bin/activate"

# 5️⃣ Upgrade build tools (IMPORTANT)
pip install --upgrade pip setuptools wheel

# 6️⃣ Install modern LangChain stack
pip install langchain langchain-core langchain-community langchain-google-genai google-generativeai python-dotenv

# 7️⃣ Verify installation
python --version
pip list

echo "👉 Activate later using:"
echo "source $ENV_PATH/bin/activate"