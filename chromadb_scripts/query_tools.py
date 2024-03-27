from llama_index.llms.ollama import Ollama
from llama_index.core.base.llms.types import ChatMessage, MessageRole

# Function to take an input query and ask several addtional questions to expand the search
# right now only mistral seems to work well but its not super fast so other models may be better

def expand_query_ollama(query, min=3, max=5, model="mistral"):
    llm_ollama = Ollama(model=model, request_timeout=30.0)
    queries = llm_ollama.chat([
            ChatMessage(
                role=MessageRole.USER,
                content="Given the following prompt, generate at least " + str(min) + " new queries (max " + str(max) + ") that can be used to effectively search a vector embeddings database to find relevant information to help answer the original prompt. Focus on identifying key topics and entities from the input, and generate queries that use synonyms, related terms, and alternate phrasings to thoroughly search for pertinent information. INPUT: " + query +  "|| Format the output as a comma-separated list of the generated queries with no other formatting or text.")
        ])
    print("Mistral querry generation: " + queries.message.content)
    
    try:
        new_queries = queries.message.content.strip().split("\n")
        new_queries = [q.strip().split(". ")[1] for q in new_queries if ". " in q]
    except:
        print(f"Error parsing newline-separated list: {queries.message.content}")
        new_queries = [query]
    
    # print("New Queries" + str(new_queries))
    return new_queries


