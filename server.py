from flask import Flask, request, jsonify
from ragatouilleUtils import create_or_load_index
from init import init
import openai

app = Flask(__name__)
init() # set the environment variables

default_dir = 'mini-arxiv-pdfs' # Default directory to index
RAG = create_or_load_index(default_dir) # Create or load the index
print(RAG)



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
    results = RAG.search(query=prompt)
    print ("========= RAG CONTEXT: =============")
    print(results)

    print("========= Request: =============")
    print(f"Model: {model}")
    print("Context: " + results + "\n user:" + prompt)
    print(f"Temperature: {temperature}")
    # Make a request to the OpenAI API using the SDK
    response = openai.Completion.create(
        engine='gpt-3.5-turbo-instruct',
        prompt="Context: " + results + "\n user:" + prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
    # print("========= Response: =============")

    # print(response)
    # Return the response as JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=3592)