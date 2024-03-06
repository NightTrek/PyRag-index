import os
import time
import inspect

from ragatouille import RAGPretrainedModel
from llama_index import SimpleDirectoryReader

def debug(message):
    caller = inspect.currentframe().f_back
    print(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {caller.f_code.co_filename}:{caller.f_lineno} - {message}")
# Override the built-in print function
def custom_print(*args, **kwargs):
    # Convert args to a string message
    message = ' '.join(str(arg) for arg in args)
    # Call debug with this message
    debug(message)

# Assign the custom print to replace the built-in print
# builtins.print = custom_print


def watch_for_commands():
    debug("Watching for commands. Type '/exit' to stop.")
    try:
        while True:
            message = input()
            if message.startswith("/"):
                if message == "/exit":
                    debug("Exiting command watch.")
                    break
                else:
                    debug(f"Command received: {message}")
            else:
                debug("Not a command. Ignoring.")
    except KeyboardInterrupt:
        debug("\nInterrupted by user. Exiting.")

if __name__ == "__main__":
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

    if os.path.exists("arxiv-pdfs/arxiv-index"):
        debug("Loading existing index...")
        RAG.from_index("arxiv-pdfs/arxiv-index")
    else:
        debug("Indexing documents...")
        documents = SimpleDirectoryReader("mini-arxiv-pdfs").load_data(show_progress=True, num_workers=12)
                
        RAG.index(
            documents,
            None,
            None,
        )


    watch_for_commands()

