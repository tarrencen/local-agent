import local_agent

def main():
    print("Local agent ready! Type 'quit' to exit.")
    history = []
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit"):
            break
        result = local_agent.agent.run_sync(user_input, message_history=history)
        history =  result.all_messages()
        print(f"Agent: {result.output}\n")

if __name__ == "__main__":
    main()
