import json
from flask import Flask, request, jsonify, Response
from init import init

from vaultAPI.retrival_test import retrive_chunks, ask_question
from chromadb_scripts.chroma import query_chroma
from chromadb_scripts.query_tools import expand_query_ollama
from oAI.openai_utils import convert_chunk_to_api, createChunk, send_chat_message, create_chat_message_chunk
from trieve.TrieveTools import search_chunks

app = Flask(__name__)


default_dir = 'mini-arxiv-pdfs' # Default directory to index

client = init() # set the environment variables


@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    data = request.get_json()
    print("========= DATA: =============")
    print(data)

    # Extract the parameters from the request
    model = data.get('model', 'gpt-3.5-turbo-instruct')
    prompt = next((message['content'] for message in reversed(data['messages']) if message['role'] == 'user'), '')
    temperature = data.get('temperature', 0.1)
    max_tokens = data.get('max_tokens', 256)
    top_p = data.get('top_p', 1)
    frequency_penalty = data.get('frequency_penalty', 0)
    presence_penalty = data.get('presence_penalty', 0)
    stream = data.get('stream', False)

    if prompt.startswith('/'):
        command = prompt[1:].split(' ')[0]
        if command == 'help':
            return jsonify(send_chat_message("""
                Available commands:\n/
                help - Show this help message\n/
                cd <directory> - Change the directory to be indexed
                expand_query - Enable or disable llm based query expansion
            """))
        elif command == 'cd':
            directory = prompt[len(command)+2:]
            # TODO: Implement logic to change the directory to be indexed
            return jsonify(send_chat_message("TODO implement changing directory"))
        else:
            return jsonify(send_chat_message("unkown command use help for a list of commands"))
    
    if stream == False:
        # return jsonify({
        # "id": "chatcmpl-123",
        # "object": "chat.completion",
        # "created": 1677652288,
        # "model": "gpt-3.5-turbo-0125",
        # "system_fingerprint": "fp_44709d6fcb",
        # "choices": [{
        #     "index": 0,
        #     "message": {
        #     "role": "assistant",
        #     "content": "\n\nHello there, how may I assist you today?",
        #     },
        #     "logprobs": "null",
        #     "finish_reason": "stop"
        # }],
        # "usage": {
        #     "prompt_tokens": 9,
        #     "completion_tokens": 12,
        #     "total_tokens": 21
        # }
        # })
        print("========= RAG CONTEXT: =============")
        chroma_response = query_chroma(prompt, 'arxiv-pdfs')
        print("============= Chroma responded =============")
        print(chroma_response)
        print("========= Request: =============")

        if chroma_response is None:
            print("Chroma returned None")
            chroma_response = ""
        completion = client.chat.completions.create(
            model='anthropic/claude-3-sonnet',
            messages=[
                {"role": "user", "content": "CONTEXT: " + str(chroma_response) + " || QUESTION: " + prompt},
            ],
        )
        return jsonify(completion.model_dump_json())

    print("========= Request: =============")
    def generate():
        yield f"data: {json.dumps(create_chat_message_chunk('Let me research this question for a second.'))}\n\n".encode('utf-8')
        yield f"data: {json.dumps(create_chat_message_chunk('.'))}\n\n".encode('utf-8')
        yield f"data: {json.dumps(create_chat_message_chunk('.'))}\n\n".encode('utf-8')

        print("========= RAG CONTEXT: =============")
        # expanded_queries = expand_query_ollama(prompt)
        # chroma_response = []
        # for query in expanded_queries:
        #     yield f'data: {json.dumps(create_chat_message_chunk("New query: " + query))}\n\n'.encode('utf-8')
        #     chroma_response.extend(query_chroma(query, 'arxiv-pdfs'))
        # # chroma_response = query_chroma(prompt, 'arxiv-pdfs') # version without the query expander
        rag_response = search_chunks(query=prompt, limit=32)

        print("============= RAG responded =============")
        print(rag_response)
        print("========= Response STATS: =============")
        print(f"Number of chunks: {len(rag_response['score_chunks'][0])}")
        if rag_response is None:
            print("Chroma returned None")
            rag_response = ""
        for chunk in client.chat.completions.create(
            model='anthropic/claude-3-sonnet',
            messages=[
                {"role": "user", "content": "CONTEXT: " + str(rag_response) + " || QUESTION: " + prompt},
            ],
            stream=True
        ):
            yield f"data: {json.dumps(convert_chunk_to_api(chunk))}\n\n".encode('utf-8')

    return Response(generate(), mimetype='text/event-stream')

@app.route('/v1/vault', methods=['POST'])
def vaultChat():
    data = request.get_json()
    print("========= DATA: =============")
    print(data)

    # Extract the parameters from the request
    model = data.get('model', 'gpt-3.5-turbo-instruct')
    prompt = next((message['content'] for message in reversed(data['messages']) if message['role'] == 'user'), '')
    temperature = data.get('temperature', 0.1)
    max_tokens = data.get('max_tokens', 256)
    top_p = data.get('top_p', 1)
    frequency_penalty = data.get('frequency_penalty', 0)
    presence_penalty = data.get('presence_penalty', 0)
    stream = data.get('stream', False)

    if prompt.startswith('/'):
        command = prompt[1:].split(' ')[0]
        if command == 'help':
            return jsonify(send_chat_message("""
                Available commands:\n/
                help - Show this help message\n/
                cd <directory> - Change the directory to be indexed
                expand_query - Enable or disable llm based query expansion
            """))
        elif command == 'cd':
            directory = prompt[len(command)+2:]
            # TODO: Implement logic to change the directory to be indexed
            return jsonify(send_chat_message("TODO implement changing directory"))
        else:
            return jsonify(send_chat_message("unkown command use help for a list of commands"))
    
    if stream == False:
        # return jsonify({
        # "id": "chatcmpl-123",
        # "object": "chat.completion",
        # "created": 1677652288,
        # "model": "gpt-3.5-turbo-0125",
        # "system_fingerprint": "fp_44709d6fcb",
        # "choices": [{
        #     "index": 0,
        #     "message": {
        #     "role": "assistant",
        #     "content": "\n\nHello there, how may I assist you today?",
        #     },
        #     "logprobs": "null",
        #     "finish_reason": "stop"
        # }],
        # "usage": {
        #     "prompt_tokens": 9,
        #     "completion_tokens": 12,
        #     "total_tokens": 21
        # }
        # })
        print("========= RAG CONTEXT: =============")
        chroma_response = query_chroma(prompt, 'arxiv-pdfs')
        print("============= Chroma responded =============")
        print(chroma_response)
        print("========= Request: =============")

        if chroma_response is None:
            print("Chroma returned None")
            chroma_response = ""
        completion = client.chat.completions.create(
            model='anthropic/claude-3-sonnet',
            messages=[
                {"role": "user", "content": "CONTEXT: " + str(chroma_response) + " || QUESTION: " + prompt},
            ],
        )
        return jsonify(completion.model_dump_json())

    print("========= Request: =============")
    def generate():
        yield f"data: {json.dumps(create_chat_message_chunk('Let me research this question for a second.'))}\n\n".encode('utf-8')
        yield f"data: {json.dumps(create_chat_message_chunk('.'))}\n\n".encode('utf-8')
        yield f"data: {json.dumps(create_chat_message_chunk('.'))}\n\n".encode('utf-8')

        print("========= RAG CONTEXT: =============")
        # expanded_queries = expand_query_ollama(prompt)
        # chroma_response = []
        # for query in expanded_queries:
        #     yield f'data: {json.dumps(create_chat_message_chunk("New query: " + query))}\n\n'.encode('utf-8')
        #     chroma_response.extend(query_chroma(query, 'arxiv-pdfs'))
        # # chroma_response = query_chroma(prompt, 'arxiv-pdfs') # version without the query expander
        rag_response = retrive_chunks(query=prompt)

        print("============= RAG responded =============")
        print(rag_response)
        print("========= Response STATS: =============")
        print(f"Number of chunks: {len(rag_response['contexts'][0])}")
        if rag_response is None:
            print("rag returned None")
            rag_response = ""
        for chunk in client.chat.completions.create(
            model='anthropic/claude-3-sonnet',
            messages=[
                {"role": "user", "content": "CONTEXT: " + str(rag_response) + " || QUESTION: " + prompt},
            ],
            stream=True
        ):
            yield f"data: {json.dumps(convert_chunk_to_api(chunk))}\n\n".encode('utf-8')

    return Response(generate(), mimetype='text/event-stream')

@app.route('/v1/models', methods=['GET'])
def models():
    
    return jsonify({
  "object": "list",
  "data": [
        {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1686935002,
        "owned_by": "openai"
        },
  ],
  "object": "list"
})

if __name__ == '__main__':
    app.run(port=3592)