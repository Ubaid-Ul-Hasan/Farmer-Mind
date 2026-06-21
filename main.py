import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.tokenizer import tokenize, extract_crop_name
from core.intent_detector import detect_intent
from core.reasoning_engine import reason
from core.response_generator import generate
from utils.loader import load


BANNER = "FarmerMind "
SEPARATOR = "-" * 50


def _print_step(message: str) -> None:
    print(f"  {message}")
    time.sleep(0.3)


def _get_known_crops() -> list[str]:
    return list(load("crops.json").keys())


def process_query(query: str) -> None:
    print()
    print("Processing...")
    tokens = tokenize(query)
    _print_step("Intent detected...")

    known_crops = _get_known_crops()
    crop_name = extract_crop_name(tokens, known_crops)
    intent = detect_intent(tokens)

    _print_step("Retrieving knowledge...")
    _print_step("Generating response...")
    print()

    data = reason(intent, tokens, crop_name)
    response = generate(intent, data, query)

    print(f"Intent: {intent}")
    print()
    print("Answer:")
    print(response)
    print()
    print(SEPARATOR)


def run() -> None:
    print(BANNER)
    print(SEPARATOR)
    print("Agricultural knowledge assistant.")
    print("Type 'exit' or 'quit' to stop.")
    print(SEPARATOR)

    while True:
        print()
        print("Question:")
        try:
            query = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            print("Session ended.")
            break

        if not query:
            continue

        if query.lower() in ("exit", "quit"):
            print("Session ended.")
            break

        process_query(query)


if __name__ == "__main__":
    run()
