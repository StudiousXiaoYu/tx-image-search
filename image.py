import gradio as gr
import tcvectordb
from tcvectordb.model.document import SearchParams
from tcvectordb.model.enum import ReadConsistency

client = tcvectordb.VectorDBClient(url='http://lb-mxc7***',
                                   username='root', key='1tWQU*****',
                                   read_consistency=ReadConsistency.EVENTUAL_CONSISTENCY, timeout=30)
db = client.database('db-xiaoyu')
coll = db.collection('image-xiaoyu')


def similar_image_text(text):
    doc_lists = coll.searchByText(
        embeddingItems=[text],
        params=SearchParams(ef=200),
        limit=3,
        retrieve_vector=False,
        output_fields=['image_url', 'image_info']
    )
    img_list = []
    for i,docs in enumerate(doc_lists.get("documents")):
        for my_doc in docs:
            print(type(my_doc["image_url"]))
            img_list.append(str(my_doc["image_url"]))
    return img_list


def similar_image(x):
    pass


with gr.Blocks() as demo:
    gr.Markdown("使用此演示通过文本/图像文件来找到相似图片。")
    with gr.Tab("文本搜索"):
        with gr.Row():
            text_input = gr.Textbox()
            image_text_output = gr.Gallery(label="最终的结果图片").style(height='auto', columns=3)
        text_button = gr.Button("开始搜索")
    with gr.Tab("图像搜索"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Gallery(label="最终的结果图片").style(height='auto', columns=3)
        image_button = gr.Button("开始搜索")

    with gr.Accordion("努力的小雨探索AI世界!"):
        gr.Markdown("先将图片或者路径存储到向量数据库中。然后通过文本/图像文件来找到相似图片。")

    text_button.click(similar_image_text, inputs=text_input, outputs=image_text_output)
    image_button.click(similar_image, inputs=image_input, outputs=image_output)

demo.launch()

