import os
import streamlit as st
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_openai.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


# 벡터 저장소 로드
def load_vectorstore(vectorstore_path):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)
    return FAISS.load_local(
        vectorstore_path, embeddings, allow_dangerous_deserialization=True
    )


# 검색 함수
def search_vectorstore(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)


def generate_response(query, context, chat_history=None):
    llm = ChatOpenAI(model="gpt-4o", api_key=api_key)
    context_text = "\n\n".join([doc.page_content for doc in context])

    # 대화 기록이 있는 경우 포함
    history_text = ""
    if chat_history and "chat_history" in chat_history:
        history = chat_history["chat_history"]
        if history:
            history_text = "\n".join([f"{msg.type}: {msg.content}" for msg in history])

    prompt = f""" 다음은 이전 상담 내용입니다.
    {context_text}
    
    이전 대화 기록:
    {history_text}

    사용자 질문 : {query}

    위의 상담내용과 이전 대화 기록을 참고하여 사용자의 질문에 대해 공감적이고 도움이 되는 답변을 제공해주세요.
    답변을 제공하면서 마지막에는 사용자에게 다시 질문을 해서 문제점을 파악하는데 도움을 주면서
    대화를 계속 이어나가도록 하세요. 
    
    답변의 길이는 2-3줄 이내로 짧게 요약해서 사용자에게 보내주세요

    만약 질문자의 질문이 검색결과 내에 없다면 다른 다른 질문으로 유도하세요
    """

    response = llm.predict(prompt)
    return response


# Streamlit 메인 함수
def main():
    st.title("마음케어 AI \n 당신의 감정을 이해하는 심리 상담 파트너")
    st.subheader("오늘도 정말 고생 많으셨습니다.😊")

    # 메모리 초기화
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = StreamlitChatMessageHistory()

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=st.session_state.chat_history,
        return_messages=True,
    )

    # 벡터 저장소 로드
    if "vectorstore" not in st.session_state:
        vectorstore_path = "./faiss_counseling_index"
        vectorstore = load_vectorstore(vectorstore_path)
        st.session_state.vectorstore = vectorstore
    else:
        vectorstore = st.session_state.vectorstore

    # 대화 기록 출력
    for message in st.session_state.chat_history.messages:
        if message.type == "human":
            with st.chat_message("user"):
                st.markdown(message.content)
        elif message.type == "ai":
            with st.chat_message("assistant"):
                st.markdown(message.content)

    # 사용자 입력창
    user_input = st.chat_input("당신의 마음을 이야기 해 주세요 🥰")

    if user_input:
        # 사용자 메시지 표시
        with st.chat_message("user"):
            st.markdown(user_input)

        # 사용자 메시지를 메모리에 추가
        st.session_state.chat_history.add_user_message(user_input)

        with st.spinner("답변 생성중입니다 잠시만 기다려주세요."):
            # 응답 생성
            relevant_docs = search_vectorstore(st.session_state.vectorstore, user_input)

            # 메모리에서 대화 기록 가져오기
            chat_history = memory.load_memory_variables({})

            if not relevant_docs:
                assistant_response = "관련 문서를 찾을 수 없습니다."
            else:
                # 수정된 generate_response 함수 호출 (아래 참조)
                assistant_response = generate_response(
                    user_input, relevant_docs, chat_history
                )

        # 어시스턴트 메시지 표시
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # 어시스턴트 메시지를 메모리에 추가
        st.session_state.chat_history.add_ai_message(assistant_response)


# Streamlit 실행
if __name__ == "__main__":
    main()
