import os
from datetime import datetime

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai_compatible import OpenAICompatibleProvider

class LocalAgent(Agent):
    def __init__(self, model, tools, instructions):
        super().__init__(model=model, tools=tools, instructions=instructions)

model = OpenAIChatModel(
    'google/gemma-4-e4b',
    provider=OpenAICompatibleProvider(
        'local-hardware',
        base_url='http://localhost:1234/v1'
    ),
)
NOTES_FILE = "notes.txt"

def save_notes(notes):
    """Save short note for later recall."""
    with open(NOTES_FILE, "a") as f:
        f.write(f"{datetime.now()}: {notes}\n")
        f.flush()
        os.fsync(f.fileno())
        print(f"Notes saved to {NOTES_FILE}")
        return "Note saved successfully."

def read_notes():
    """Read saved notes."""
    if not os.path.exists(NOTES_FILE):
        return "No notes found."
    with open(NOTES_FILE, "r") as f:
        notes = f.read()
        return notes

def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d at %H:%M:%S")

def calculate(expression: str) -> float:
    """Calculate the result of a mathematical expression."""
    if not set(expression) <= set("0123456789+-*/.() "):
        return "Error: Invalid characters in expression."
    try:
        result = eval(expression)
        return result
    except Exception as e:
        print(f"Error calculating expression '{expression}': {e}")
        return f"Error: {e}"

agent = Agent(
    model=model,
    tools=[save_notes, get_current_time, read_notes, calculate],
    instructions= (
        "You are a helpful assistant running locally.",
        "Use the tools provided to answer questions and perform tasks.",
        "Keep your responses concise and relevant.",
        "If you don't know the answer, it's okay to say so.",
        "Prioritize user privacy and data security.",
        "Prioritize honesty over politeness."
    ),
    # result_type="chat"


)
