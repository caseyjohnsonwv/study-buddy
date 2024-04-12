import json
from typing import List, Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import gradio as gr
import env
from vectordb import VectorDB

KNOWLEDGEBASE = VectorDB('./courses')
CHAT_MODEL = ChatOpenAI(model='gpt-3.5-turbo', temperature=0, api_key=env.OPENAI_API_KEY, streaming=True)

SYSTEM_TEMPLATE = """
    You are a helpful study assistant who examines educational materials to answer questions.
    Given the context below, beneath the triple backticks, answer the human's question.
    Always prefer the context below over your pre-existing knowledge.
    Always double-check and justify your answer, even if it seems redundant.
    Cite the associated filenames and page/slide numbers (if applicable) when answering so the human can read further.
    You only need to cite each unique source once.
    Format outputs into lists and tables as appropriate for readability.
    ```
""".replace('\t', '').strip()

def chat_function(message:str, history:List[Tuple[str, str]], course_name:str=None):
    messages = []
    # retrieve context
    metadata_filter = {}
    if course_name:
        metadata_filter['course_name'] = course_name
    retrieved_docs = KNOWLEDGEBASE.search(phrase=message, k=10, metadata_filter=metadata_filter)
    if len(retrieved_docs) == 0:
        return 'Sorry, no relevant documents found.'
    retrieved_docs.sort(key=lambda t:t[1], reverse=True)
    context = '\n'.join([f"Context: {d[0].page_content} | Metadata: {json.dumps(d[0].metadata)}" for d in retrieved_docs])
    # prepare prompt
    messages.append(SystemMessage(content = '\n'.join([SYSTEM_TEMPLATE, context])))
    history_to_keep = min(len(history), 2)
    for u,ai in history[:history_to_keep]:
        messages.append(HumanMessage(content=u))
        messages.append(AIMessage(content=ai))
    messages.append(HumanMessage(content=message))
    # feed into chatgpt for response
    full_answer = ''
    for chunk in CHAT_MODEL.stream(input=messages):
        full_answer += chunk.content
        yield full_answer

course_names = KNOWLEDGEBASE.list_indexed_courses()
INTERFACE = gr.ChatInterface(
    chat_function,
    additional_inputs=[
        gr.Dropdown(choices=sorted(list(course_names)), label='Course'),
    ],
    additional_inputs_accordion=gr.Accordion(label='Filters', open=True),
    title='Study Buddy',
)
INTERFACE.launch(server_name=env.SERVER_HOST, server_port=env.SERVER_PORT)
