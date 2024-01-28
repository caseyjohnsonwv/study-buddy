import json
from typing import List, Tuple
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import gradio as gr
import env
from utils.vectordb import VectorDB

COURSE = VectorDB('HMG6228', force_recreate=True)
CHAT_MODEL = ChatOpenAI(model='gpt-3.5-turbo', temperature=0, api_key=env.OPENAI_API_KEY, organization=env.OPENAI_ORG_ID)

SYSTEM_TEMPLATE = """
    You are a helpful study assistant who examines educational materials to answer questions.
    Given the context below, beneath the triple backticks, answer the human's question.
    Cite the associated filename and page or slide number (if applicable) when answering so the human can read further.
    Format outputs into lists and tables as appropriate for readability.
    Always prefer the context below over your pre-existing knowledge.
    ```
""".replace('\t', '').strip()

def chat_function(message:str, history:List[Tuple[str, str]]):
    messages = []
    # retrieve context
    retrieved_docs = COURSE.search(message, k=5)
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
    res = CHAT_MODEL.invoke(input=messages)
    return res.content

interface = gr.ChatInterface(chat_function)
interface.launch()
