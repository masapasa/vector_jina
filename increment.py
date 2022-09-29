from jina import DocumentArray, Executor, requests, Flow


class MyExec(Executor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.da = DocumentArray(storage='sqlite', config={'connection': 'example12345.db', 'table_name': 'mine'})

    @requests(on='/foo')
    def foo(self, docs: DocumentArray, **kwargs):
        self.da.extend(docs)

    @requests(on='/count')
    def bar(self, **kwargs):
        print(len(self.da))


f = Flow().add(uses=MyExec)

with f:
    for _ in range(10):
        f.post('/foo', DocumentArray.empty(10))
        f.post('/count')

# out of the with scope `f` is closed, let's reopen it and see if the docs are still there
with f:
    f.post('/count')