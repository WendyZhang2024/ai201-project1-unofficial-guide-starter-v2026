import config
import questions as qs
from store import search

items = qs.answered()
for item in items:
    question = item["question"]
    results = search(question, top_k=config.TOP_K, corpus=config.CORPUS, variant="default")
    print(f"\nQuestion: {question}")
    for i, r in enumerate(results):
        text = getattr(r, 'text', getattr(r, 'chunk', getattr(r, 'content', None)))
        if text is None:
            print(f"  [Unknown attribute] results[{i}] attributes: {dir(r)}")
        else:
            print(f"  Chunk {i+1} length: {len(text)} chars")