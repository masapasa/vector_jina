from jina import requests, Flow
from docarray import DocumentArray
import pprint

class MyExecutor(Executor):
    @requests
    def test(self, docs: DocumentArray, **kwargs):
        pprint(docs)


flow = Flow().add(uses=MyExecutor)

with flow as f:
    f.post(on="/index", inputs=docs, show_progress=True)