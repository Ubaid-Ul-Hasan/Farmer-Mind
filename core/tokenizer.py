import re
from typing import List


STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "i", "me", "my", "we", "our", "you", "your", "he", "she", "it",
    "they", "them", "their", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "at", "by", "for", "in", "of",
    "on", "to", "up", "and", "as", "but", "or", "nor", "so", "yet",
    "if", "then", "than", "too", "very", "just", "not", "with", "about",
    "how", "when", "where", "why", "from", "into", "after", "before",
    "much", "many", "some", "any", "all", "its", "also", "get", "got",
    "plant", "crop", "farm", "farmer", "field",
}


def tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def extract_crop_name(tokens: List[str], known_crops: List[str]) -> str | None:
    for token in tokens:
        if token in known_crops:
            return token
    return None
