import tcvectordb
from tcvectordb.model.collection import Embedding
from tcvectordb.model.document import Document, Filter, SearchParams
from tcvectordb.model.enum import FieldType, IndexType, MetricType, ReadConsistency,EmbeddingModel
from tcvectordb.model.index import Index, VectorIndex, FilterIndex, HNSWParams
import numpy as np

#create a database client object
client = tcvectordb.VectorDBClient(url='http://lb-mxc7no1z-r32z5gdisey6cfo7.clb.ap-beijing.tencentclb.com:20000', username='root', key='1tWQUtu0nLPgOwjjd0qyEPe0mN4lzfzc3Rc0An8D', read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
# create a database
# db = client.create_database(database_name='db-xiaoyu')

# print(db.database_name)

# list databases
# db_list = client.list_databases()
#
#
# for db in db_list:
#          print(db.database_name)


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
# print(vars(coll))

coll = db.collection('image-xiaoyu')

data = np.loadtxt(open("./reverse_image_search/reverse_image_search.csv","rb"),delimiter=",",skiprows=1,usecols=[0,1,2])

# 写入数据。
# 参数 build_index 为 True,指写入数据同时重新创建索引。
res = coll.upsert(
            documents=[
                Document(id='0011', image_info="一群小鱼。", image_url='./goldfish'),
                Document(id='0012', image_info="很凶猛的鳄鱼~", image_url='./African_crocodile'),
                Document(id='0013', image_info="甄士隐梦幻识通灵，贾雨村风尘怀闺秀。", image_url='曹雪芹', bookName='红楼梦', page=23)
            ],
            build_index=False
        )


doc_lists = coll.searchByText(
                 embeddingItems=['天下大势，分久必合，合久必分'],
                 filter=Filter(Filter.In("bookName", ["三国演义", "西游记"])),
                 params=SearchParams(ef=200),
                 limit=3,
                 retrieve_vector=False,
                 output_fields=['bookName','author']
             )
# printf
for i, docs in enumerate(doc_lists.get("documents")):
                for doc in docs:
                        print(doc)
