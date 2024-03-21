# PyRAG-Index

PyRAG-Index is a collection of basic Retrieval-Augmented Generation (RAG) implementations that primarily utilize local models for each component. It is designed to work seamlessly with mindMac and Big-AGI clients, providing a foundation for building and experimenting with RAG systems.

## Features

- Local model support: PyRAG-Index leverages local models for various parts of the RAG pipeline, enabling offline usage and reducing dependency on external services.
- ChromaDB integration: The library includes support for ChromaDB, allowing efficient storage and retrieval of document embeddings.
- VaultAPI compatibility: PyRAG-Index is compatible with VaultAPI, enabling secure storage and access to sensitive data.
- Easy installation: The library provides an installation script to simplify the setup process.

## Installation

To install PyRAG-Index, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/your-username/pyrag-index.git
   ```

2. Navigate to the project directory:
   ```
   cd pyrag-index
   ```

3. Run the installation script:
   ```
   ./install.sh
   ```

Note: After running the installation script, you need to manually install the required models through ollama. Please refer to the ollama documentation for instructions on installing the models.

you also need to provider your own API keys through the init_template script

 1. add your openAI or OpenRouter API key
 2. change the name of the init_template.py script to just init.py
 3. your ready to go.


## Usage

PyRAG-Index provides a basic API server designed to support OpenAI curl requests. You can interact with it by adding an OpenAI provider to Big-AGI locally or MindMac using the following URL:

```
http://127.0.0.1:3592
```

Once the API server is running, you can send requests to it using the standard OpenAI API format. PyRAG-Index will handle the request, perform the necessary retrieval and generation tasks, and return the response.

To start the API server, run the following command:

```
flask run --reload
```

Make sure you have installed all the required dependencies and models before running the server.

The repo contains connectors for a variety of document stores like ChromaDB you can run experiments with different rag technologies to see how it effects your retrivals. 

- ChromaDB_scripts/Query_tools.py contains functions to query ChromaDB like query_expander which takes your prompt and writes several queries based on it to increase the context retrieved.
- VaultAPI/ folder contains tools which you can use to use the Vault APIs to securely store/retrieve data. Vault is state of the art retrivals so you can test against it as a standard.



## Contributing

Contributions to PyRAG-Index are welcome! If you encounter any issues, have suggestions for improvements, or would like to contribute new features, please open an issue or submit a pull request on the GitHub repository.

## License

PyRAG-Index is released under the [MIT License](LICENSE).
