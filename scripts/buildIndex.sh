#!/bin/bash

read -p "Enter the directory to index (default: files_to_index): " directory
directory=${directory:-files_to_index}

echo "Select a vector database:"
echo "1. ChromaDB"
echo "2. Pinecone"
echo "3. Milvus"
echo "4. Ragatouille"

read -p "Enter your choice (1-4): " choice

case ${choice:-1} in
  1)
    ./scripts/chromadb_index.sh "$directory"
    wait $!
    exit 0
    ;;
  2)
    ./scripts/pinecone_index.sh "$directory"
    wait $!
    ;;
  3)
    ./scripts/milvus_index.sh "$directory"
    wait $!
    ;;
  4)
    ./scripts/ragatouille_index.sh "$directory"
    wait $!
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac
