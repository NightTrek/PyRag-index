def convert_chunk_to_api(chunk):
    return {
                "id": chunk.id,
                "object": chunk.object,
                "created": chunk.created,
                "model": chunk.model,
                "system_fingerprint": chunk.system_fingerprint,
                "choices": [
                    {
                        "index":chunk.choices[0].index,
                        "delta":{
                            "role":chunk.choices[0].delta.role,
                            "content":chunk.choices[0].delta.content},
                        "logprobs":chunk.choices[0].logprobs,
                        "finish_reason":chunk.choices[0].finish_reason
                    }
                ],
            }

def createChunk(choices, id="0", object="chat.completion.chunk", created=1694268190, model="gpt-3.5-turbo-0125", system_fingerprint="fp_44709d6fcb"):
    return {
            "id": id,
            "object": object,
            "created": created,
            "model": model,
            "system_fingerprint": system_fingerprint,
            "choices": choices
            }

def createChoices(role, content, logprobs, finish_reason):
    return [
            {
                "index":"0",
                "delta":{
                    "role": role,
                    "content": content},
                "logprobs": logprobs,
                "finish_reason": finish_reason
            }
        ],


def create_chat_message_chunk(message):
    choice = createChoices(role="assistant", content=message, logprobs="null", finish_reason="None")
    return createChunk(choices=choice)

def send_chat_message(message):
    return {
        "id": "gen-4Ya6uSF9iAkdWXlpIvOuhhkVdBmR",
        "object": "chat.completion",
        "created": 1677652288,
        "model": "gpt-3.5-turbo-0125",
        "system_fingerprint": "None",
        "choices": [{
            "index": 0,
            "message": {
            "role": "assistant",
            "content": message,
            },
            "logprobs": "null",
            "finish_reason": "stop"
        }],
        "usage": {
            "prompt_tokens": 9,
            "completion_tokens": 12,
            "total_tokens": 21
        }
    }


# ChatCompletionChunk(id='gen-4Ya6uSF9iAkdWXlpIvOuhhkVdBmR',
#                     choices=[
#                         Choice(
#                             delta=ChoiceDelta(
#                                         content='.',
#                                         function_call=None,
#                                         role='assistant',
#                                         tool_calls=None),
#                             finish_reason=None,
#                             index=0,
#                             logprobs=None)],
#                     created=1711063003,
#                     model='anthropic/claude-3-sonnet',
#                     object='chat.completion',
#                     system_fingerprint=None)