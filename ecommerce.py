#%%%
with open("/home/aswin/data/icecat-products-w_price-19k-20201127/icecat-products-w_price-19k-20201127.json") as file:
  da = DocumentArray.from_json(file.read())
# %%
da.summary()
# %%
da[0]
# %%
from docarray import DocumentArray, Document
import json

da = DocumentArray()
  
with open('/home/aswin/data/icecat-products-w_price-19k-20201127/icecat-products-w_price-19k-20201127.json') as f:
    jdocs = json.load(f)
for doc in jdocs:
    d = Document(text=doc['title'], tags=doc)
    da.append(d)
da[0]
# %%
from jina import Flow
f = Flow()

f = Flow().add(uses='jinahub+sandbox://TransformerSentenceEncoder/latest').add(uses='jinahub://SimpleIndexer/latest', install_requirements=True)

with f:
  f.index(da)
# %%
