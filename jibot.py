from docarray import DocumentArray, Document
from jina import Flow, Executor, requests
from config import DATA_FILE, NUM_DOCS, PORT
import click

#********** modification 04 08 2022 *******************
import logging
import boto3
import botocore
from botocore.exceptions import ClientError
import os
import glob
import json
import configparser

def readConfig():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    return config['Enriched-Data-S3']

config = readConfig()

#********************************************************

# ***************** Executor to filter out the Documents without embedding *********
#EMB_DIM = 512

class EmbeddingChecker(Executor):
    @requests
    def check(self, docs, **kwargs):
        filtered_docs = DocumentArray()
        for doc in docs:
            if doc.embedding is None:
                continue
            #if doc.embedding.shape[0] != EMB_DIM:
            #    continue
            filtered_docs.append(doc)
        return filtered_docs
    
    
#***********************************************************************************


flow = (
    Flow(protocol="http", port=PORT)
    .add(
        name="encoder",
        uses="jinahub://TransformerTorchEncoder",
        #uses_with={
         #   "pretrained_model_name_or_path": "sentence-transformers/paraphrase-mpnet-base-v2"}
        uses_with={'pretrained_model_name_or_path': 'bert-base-uncased'}
        ,
        install_requirements=True,
    )
    .add(name = "Filterout_docs_without_embeddings", 
             uses = EmbeddingChecker)
    .add(name = "Indexer",uses="jinahub://SimpleIndexer"
         ,  install_requirements=True)
    .needs_all()
)
#flow.plot()


def index(num_docs=NUM_DOCS):
    
    # ****************** modification 04 08 2022 '******************
    s3 = boto3.resource('s3')
    bucket_name = config['bucket_name']
    bucket = s3.Bucket(bucket_name)
    docs = DocumentArray()
    print(bucket_name)

    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()
        if key.endswith('.text') :
            data = body.decode('utf-8') # Decode using the utf-8 encoding
            jdata = json.loads(data)
            q_text = ""
            for item in jdata['ques']:
                for q in item:
                    q_text = q_text + " " + q
                
                docs.append(Document(text = q_text
                        ,uri = jdata['pageLink'] ,tags = jdata  ))
    #***************************************************************

    with flow:
        #docs = flow.index(docs, on_done = store_embeddings ,show_progress=True)
        flow.index(docs,show_progress=True)
        print(docs.summary)


def search_grpc(string: str):
    doc = Document(text=string)
    with flow:
        results = flow.search(doc)

    print(results[0].matches)

    for match in results[0].matches:
        print(match.text)

        
#*************** modification 05 08 2022 **************
#*******************************************************

def search():
    #with flow:
     #   flow.block()
    question = Document(text="what do you know about certificate bonuses?")

    with flow:
        results = flow.search(question)

    #print(results[0].matches[0].tags["answer"])
    for m in results[0].matches:
        answers = m.tags['body']
        for ans in answers:
        
            for key,val in ans.items() :
                if key == 'text':
                    print(val)
        print(m.uri)
        print('************************')
    
    
    
@click.command()
@click.option(
    "--task",
    "-t",
    type=click.Choice(["index", "search"], case_sensitive=False),
)
@click.option("--num_docs", "-n", default=NUM_DOCS)
def main(task: str, num_docs):
    if task == "index":
        index(num_docs=num_docs)
    elif task == "search":
        search()
    else:
        print("Please add '-t index' or '-t search' to your command")


if __name__ == "__main__":
    main()