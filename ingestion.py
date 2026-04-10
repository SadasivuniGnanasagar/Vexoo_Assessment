import re
from difflib import SequenceMatcher

# ---------- similarity ----------
def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# ---------- summary ----------
def summarize(text):
    sentences = re.split(r'[.!?]', text)
    return sentences[0]

# ---------- category ----------
def category(text):
    text = text.lower()
    if "health" in text:
        return "Health"
    elif "ai" in text or "technology" in text:
        return "Technology"
    return "General"

# ---------- keywords ----------
def keywords(text):
    words = re.findall(r'\w+', text.lower())
    return words[:8]

# ---------- sliding window ----------
def split_text(text, size=100, overlap=30):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+size])
        i += (size - overlap)
    return chunks

# ---------- routing ----------
def route_query(query):
    q = query.lower()

    # detect math expressions
    if any(op in q for op in ["+", "-", "*", "/", "%"]):
        return "math"

    elif any(word in q for word in ["calculate", "sum", "solve"]):
        return "math"

    elif "law" in q or "legal" in q:
        return "legal"

    else:
        return "general"

# ---------- BONUS modules ----------
def math_solver(query):
    try:
        # extract math expression like 6+2
        expression = re.findall(r'[0-9+\-*/%.]+', query)

        if expression:
            return eval(expression[0])

        return "Cannot solve"

    except:
        return "Cannot solve"

def legal_module(query):
    return "Legal module activated: retrieving structured legal info"

def general_module(system, query):
    return system.search(query)

# ---------- system ----------
class System:
    def __init__(self):
        self.data = []

    def ingest(self, text):
        chunks = split_text(text)

        for c in chunks:
            self.data.append({
                "raw": c,
                "summary": summarize(c),
                "category": category(c),
                "keywords": keywords(c)
            })

    def search(self, query):
        best = None
        best_score = 0

        for d in self.data:
            scores = [
                similarity(query, d["raw"]),
                similarity(query, d["summary"]),
                similarity(query, d["category"]),
                similarity(query, " ".join(d["keywords"]))
            ]

            score = max(scores)

            if score > best_score:
                best_score = score
                best = d

        return best


# ---------- run ----------
if __name__ == "__main__":
    with open("sample.txt", "r") as f:
        text = f.read()

    s = System()
    s.ingest(text)

    while True:
        q = input("\nAsk (type exit): ")

        if q == "exit":
            break

        # Routing decision
        route = route_query(q)
        print("Query Type:", route)

        # Route to correct module
        if route == "math":
            result = math_solver(q)

        elif route == "legal":
            result = legal_module(q)

        else:
            result = general_module(s, q)

        if isinstance(result, dict):
            print("\nSummary:", result["summary"])
            print("Category:", result["category"])
            print("Keywords:", result["keywords"])
        else:
            print("\nAnswer:", result)