import json
from typing import List, Dict
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
import os
from langchain_core.documents import Document
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")



# 데이터 로드 함수
def load_json_data(file_path: str) -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

#데이터 처리 및 문서 생성 함수
def process_data(data, data_type) -> List[Document]:
    documents =[]
    for i, item in enumerate(data):
        if data_type == 'singleturn':
            documents.append(Document(
                page_content=f'질문 : {item['input']}\n 답변 : {item['output']}',
                metadata={'type':'singleturn','role':'상담사'}
            ))
        elif data_type == 'multiturn':
            conversation='\n'.join([f'{turn['Speaker']}:{turn['Text']}'for turn in item])
            documents.append(Document(
                page_content=conversation,
                metadata={'type':'multiturn', 'conversation_id':str(i)}
            ))
    return documents

#벡터 저장소 생성 함수
def create_vectorstores(documents) -> FAISS:
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002 ")
    return FAISS.from_documents(documents, embeddings)

#검색 함수
def search_vectorstore(vectorsotore, query, k):
    return vectorsotore.similarity_search(query, k=k)

#챗봇 응답 생성
def generate_response(query, context):
    llm = ChatOpenAI(model='gpt-4o', api_key=api_key)
    context_text='\n\n'.join([doc.page_content for doc in context])
    prompt =f""" 다음은 이전 상담 내용입니다.
    {context_text}

    사용자 질문 : {query}

    위의 상담내용을 참고하여 사용자의 질문에 대해 공감적이고 도움이 되는 답변을 제공해주세요.
    답변을 제공하면서 마지막에는 사용자에게 다시 질문을 해서 문제점을 파악하는데 도움을 주면서
    대화를 계속 이어나가도록 하세요. """

    response = llm.predict(prompt)
    return response

#streamlit
def main():
    st.title('심리 상담 챗봇')
    st.subheader('오늘도 정말 고생 많으셨습니다.')

    if 'vectorstore'not in st.session_state:
        st.write('잠시만 기다려 주세요...')

        #데이터 로드
        singleturn_data = load_json_data('./total_kor_counsel_bot.jsonl')
        multiturn_data = load_json_data('./total_kor_multiturn_counsel_bot.jsonl')

        #문서 생성
        singleturn_data