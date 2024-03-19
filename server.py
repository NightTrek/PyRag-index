from flask import Flask, request, jsonify
from init import init

from vaultAPI.retrival_test import retrive_chunks, ask_question
from chromaDBScripts.createIndexFromFolder import query_chroma

app = Flask(__name__)


default_dir = 'mini-arxiv-pdfs' # Default directory to index

client = init() # set the environment variables

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    print("========= DATA: =============")
    # print(request)
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
    
    print ("========= RAG CONTEXT: =============")
    # vault_response = retrive_chunks(prompt)
    # print("============= Vault responded =============")
    # print(vault_response)
    chroma_response = query_chroma(prompt, 'arxiv-pdfs')
    print("============= Chroma responded =============")
    print(chroma_response)
    print("========= Request: =============")

    # if vault_response is None:
    #     print("Vault returned None")
    #     vault_response = ""
    if chroma_response is None:
        print("Chroma returned None")
        chroma_response = ""
    

    completion = client.chat.completions.create(
    model='anthropic/claude-3-sonnet',
    messages=[
        {"role": "user", "content": "CONTEXT: " + str(chroma_response) + " || QUESTION: " + prompt},
    ]
)

    response_data = {
        "id": completion.id,
        "object": completion.object,
        "created": completion.created,
        "model": completion.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": completion.choices[0].message.role,
                    "content": completion.choices[0].message.content
                },
                "logprobs": "null",
                "finish_reason": completion.choices[0].finish_reason
            }
        ],
        "usage": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        },
        "system_fingerprint": "fp_4f2ebda25a"
    }

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(port=3592)