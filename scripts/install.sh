#!/bin/bash
if [[ "$1" == "--python" ]]; then
  localPy="$2"
else
    echo "No supplied --python argument, using default python3"
  localPy="python3"
fi
# Check if Python is installed
if ! command -v $localPy &> /dev/null
then
    echo "Python is not installed. Please install Python 3.10 or higher and try again."
    exit 1
fi

# Check Python version
python_version=$($localPy -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$(echo "$python_version < 3.10" | bc)" -eq 1 ]]
then 
    echo "Python version is too old. Please install Python 3.10 or higher and try again."
    exit 1
fi

# Install jq if not already installed
if ! command -v jq &> /dev/null
then
    echo "jq is not installed. Installing jq..."
    sudo apt-get install -y jq
fi

# Create virtual environment
$localPy -m venv pyrag_index_env

# Activate virtual environment
source pyrag_index_env/bin/activate

# Install llama_index and other dependencies
pip install llama_index chromadb flask llama-index-llms-ollama llama-index-vector-stores-chroma llama-index-embeddings-ollama openai requests_toolbelt

echo "Installation complete. \\n\n"
# Create JSON file with initial values
cat > index_config.json << EOF
{
    "vector_index": [],
    "lib": true
}
EOF

echo "================================================="
echo "Use the launch script to activate the server"
