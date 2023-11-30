import tcvectordb
import numpy as np
from tcvectordb.model.collection import Embedding
from tcvectordb.model.document import Document, Filter, SearchParams
from tcvectordb.model.enum import FieldType, IndexType, MetricType, ReadConsistency,EmbeddingModel
from tcvectordb.model.index import Index, VectorIndex, FilterIndex, HNSWParams

client = tcvectordb.VectorDBClient(url='http://lb-mxc7no1*******', username='root', key='1tWQU*******', read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
db = client.database('db-xiaoyu')

# -- index config
index = Index(
    FilterIndex(name='id', field_type=FieldType.String, index_type=IndexType.PRIMARY_KEY),
    VectorIndex(name='vector', dimension=768, index_type=IndexType.HNSW,
                metric_type=MetricType.COSINE, params=HNSWParams(m=16, efconstruction=200))
)

# Embedding config
ebd = Embedding(vector_field='vector', field='image_info', model=EmbeddingModel.BGE_BASE_ZH)

# create a collection
coll = db.create_collection(
    name='image-xiaoyu',
    shard=1,
    replicas=0,
    description='this is a collection of test embedding',
    embedding=ebd,
    index=index
)

coll = db.collection('image-xiaoyu')

data = np.genfromtxt('./reverse_image_search/reverse_image_search.csv', delimiter=',', skip_header=1, usecols=[0, 1, 2], dtype=None)
print(data[0])
first_row = data[0]
column1 = first_row[0]
column2 = first_row[1]
column3 = first_row[2]

print(column1)  # 输出第一列的值
print(column2.decode())  # 输出第二列的值
print(column3.decode())  # 输出第三列的值

doc_list = []
for row in data:
    id_row = str(row[0])
    image_url = row[1].decode()
    image_info = row[2].decode()
    doc_list.append(Document(id=id_row,image_url=image_url,image_info=image_info))

res = coll.upsert(
            documents=doc_list,
            build_index=True
        )


doc_lists = coll.searchByText(
                 embeddingItems=['gold'],
                 params=SearchParams(ef=200),
                 limit=3,
                 retrieve_vector=False,
                 output_fields=['image_url','image_info']
             )
# printf
for i, docs in enumerate(doc_lists.get("documents")):
                for doc in docs:
                        print(type(doc["image_url"]))