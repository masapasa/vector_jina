from jina import Flow
from docarray import Document, DocumentArray
from pprint import pprint

initial_notes = [
    "I'm working on a new project!",
    "It's uses Jina!"
    "Jina is a ml ops framework for neural search"
    "You can use a database to store your index"
]

docs = DocumentArray(
    [Document(text=initial_notes[i]) for i in range(len(initial_notes))]
)

docs.summary()

flow = (
    Flow()
    .add(name="sentencer", uses="jinahub+sandbox://Sentencizer/latest")
    .add(
        name="encoder",
        uses="jinahub+docker://TransformerTorchEncoder",
        volumes=".cache/huggingface:/root/.cache/huggingface",
        uses_with={"traversal_paths": "@c"},
    )
    .add(
        name="indexer",
        uses="jinahub://SimpleIndexer",
        uses_metas={"workspace": "workspace"},
        uses_with={"traversal_right": "@c"},
    )
)

with flow as f:
    f.post(on="/index", input=docs, show_progress=True)
    resp = f.post("/search", Document(text="watch database"))
    pprint(resp.data)
    pprint(resp.data.docs)
    pprint(resp.data.docs[0].text)
    pprint(resp.data.docs[0].matches)