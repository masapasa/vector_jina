
from jina import Client
from docarray import Document
# from pprint import pprint

# Set up client
alex_flow_url = "grpcs://ecommerce-7f219b7384.wolf.jina.ai"  # 100 indexed
daniel_flow_url = "grpcs://ecommerce-19k-6a3ec390bd.wolf.jina.ai"
aswin_flow_url = "grpcs://b90f1b8c7d.wolf.jina.ai"
#client = Client(host=alex_flow_url)
client = Client(host=aswin_flow_url)

# Define search term
query = Document(text="dell")

# Add filters
colors = ["Black", "Blue"]
filter = {"attr_t_product_colour": {"$in": colors}}

# Use client to send search term to Flow on JCloud
results = client.search(query,
                        show_progress=True,
                        parameters={"filter": filter})

# View results
for match in results[0].matches[:2]:
  print(match.text)
  # pprint(match.tags)
  print(match.scores['cosine'])
  print("---")