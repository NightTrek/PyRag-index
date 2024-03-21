import json
from flask import Flask, request, jsonify, Response
from init import init

from vaultAPI.retrival_test import retrive_chunks, ask_question
from chromaDBScripts.createIndexFromFolder import query_chroma
from oAI.openai_utils import convert_chunk_to_api, createChunk, createChoices


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

    if prompt.startswith('/'):
        command = prompt[1:].split(' ')[0]
        if command == 'help':
            return jsonify({'choices': [{'text': 'Available commands:\n/help - Show this help message\n/cd <directory> - Change the directory to be indexed'}]})
        elif command == 'cd':
            directory = prompt[len(command)+2:]
            # TODO: Implement logic to change the directory to be indexed
            return jsonify({'choices': [{'text': f'Changed directory to {directory}'}]})
        else:
            return jsonify({'choices': [{'text': f'Unknown command: {command}. Use /help to see available commands.'}]})
    

    def generate():
        print("========= RAG CONTEXT: =============")
        chroma_response = query_chroma(prompt, 'arxiv-pdfs')
        print("============= Chroma responded =============")
        print(chroma_response)
        print("========= Request: =============")

        if chroma_response is None:
            print("Chroma returned None")
            chroma_response = ""
        

        for chunk in client.chat.completions.create(
            model='anthropic/claude-3-sonnet',
            messages=[
                {"role": "user", "content": "CONTEXT: " + str(chroma_response) + " || QUESTION: " + prompt},
            ],
            stream=True
        ):
            yield f"data: {json.dumps(convert_chunk_to_api(chunk))}\n\n".encode('utf-8')


    return Response(generate(), mimetype='text/event-stream')


@app.route('/v1/models', methods=['POST'])
def models():
    return {
  "object": "list",
  "data": [
    {
      "id": "stephen-colbert",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    },
  ],
  "object": "list"
}

if __name__ == '__main__':
    app.run(port=3592)