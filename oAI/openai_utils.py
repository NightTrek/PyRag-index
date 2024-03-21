def convert_chunk_to_api(chunk):
    return {
                "id": chunk.id,
                "object": chunk.object,
                "created": chunk.created,
                "model": chunk.model,
                "system_fingerprint": chunk.system_fingerprint,
                "choices": [
                    {
                        "index":"0",
                        "delta":{
                            "role":chunk.choices[0].delta.role,
                            "content":chunk.choices[0].delta.content},
                        "logprobs":chunk.choices[0].logprobs,
                        "finish_reason":chunk.choices[0].finish_reason
                    }
                ],
            }

def createChunk(id="0", object="chat.completion.chunk", created=1694268190, model="gpt-3.5-turbo-0125", system_fingerprint="fp_44709d6fcb", choices):
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