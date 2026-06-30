from dotenv import load_dotenv
from mem0 import MemoryClient
import logging
import json

load_dotenv()
user_name = "David"
mem0 = MemoryClient()


def add_memory():
    messages_formatted = [
        {"role": "user", "content": "I really like Linkin Park."},
        {"role": "assistant", "content": "That is a good choice."},
        {"role": "user", "content": "I think so too."},
        {"role": "assistant", "content": "What is your favorite song by them?"},
    ]
    # use the user_name variable rather than a hardcoded string
    mem0.add(messages_formatted, user_id=user_name)


def get_memory_by_query():
    # build the query using f-string interpolation
    query = f"What are {user_name}'s preferences?"
    results = mem0.search(query, user_id=user_name)

    memories = [
        {
            "memory": result.get("memory"),
            "updated_at": result.get("updated_at"),
        }
        for result in results or []
    ]

    memories_str = json.dumps(memories, ensure_ascii=False)
    print(f"Memories: {memories_str}")
    return memories_str


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # add sample memory before attempting to search
    add_memory()
    get_memory_by_query()

