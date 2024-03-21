#!/bin/bash

echo "Pinecone support not yet implemented. Exiting."
exit 1

if [ $# -eq 0 ]; then
    echo "Please provide a directory path as an argument."
    exit 1
fi

directory="$1"

python3 handleGenerateIndex.py "$directory"
