#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Please provide a directory path as an argument."
    exit 1
fi

directory="$1"

if [[ "$2" == "--python" ]]; then
  localPy="$3"
else
  localPy="python3"
fi
# Activate virtual environment
source pyrag_index_env/bin/activate
echo "======================================================"
echo "Starting Chroma index for $directory"
$localPy ./chromaDBScripts/handleGenerateInex.py "$directory"
wait $!
# Add the directory to the vector_index array in index_config.json
jq --arg dir "$directory" '.vector_index += [{dir: $dir, type: "chromadb"}]' index_config.json > tmp.$.json && mv tmp.$.json index_config.json

exit 0
