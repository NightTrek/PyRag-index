import sys
import time

def watch_for_commands():
    print("Watching for commands. Type '/exit' to stop.")
    try:
        while True:
            message = input()
            if message.startswith("/"):
                if message == "/exit":
                    print("Exiting command watch.")
                    break
                else:
                    print(f"Command received: {message}")
            else:
                print("Not a command. Ignoring.")
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")

if __name__ == "__main__":
    watch_for_commands()
