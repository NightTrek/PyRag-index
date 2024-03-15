from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

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

    print("========= Request: =============")
    print(f"Model: {model}")
    print(f"Prompt: {prompt}")
    print(f"Temperature: {temperature}")

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

    # Make a request to the OpenAI API
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {os.environ["OPENAI_API_KEY"]}'
        },
        json={
            'model': 'gpt-3.5-turbo-instruct',
            'prompt': prompt,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
            'frequency_penalty': frequency_penalty,
            'presence_penalty': presence_penalty
        }
    )
    # print("========= Response: =============")

    # print(response.json())
    # Return the response as JSON
    return response.json()


if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] = "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" # OpenAI API key
    default_dir = 'mini-arxiv-pdfs' # Default directory to index
    
    app.run(port=3592)