import os
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import Document
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def load_jsonl(file_path):
    """JSONL 파일을 읽어 리스트로 반환"""
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            try:
                data.append(json.loads(line.strip()))
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError: {e} on line {i} in file {line}")
    return data


# 문서 처리 함수 (singleton/multiturn 구분)
def process_data(data, data_type):
    documents = []
    for item in data:
        if data_type == "singlturn":
            documents.append(
                Document(
                    page_content=f"질문: {item['input']}\n답변: {item['output']}",
                    metadata={"type": "singleton", "role": "상담사"},
                )
            )
        elif data_type == "multiturn":
            conversation = "\n".join(
                [f"{turn['speaker']}: {turn['utterance']}" for turn in item]
            )
            documents.append(
                Document(page_content=conversation, metadata={"type": "multiturn"})
            )
    return documents


# 벡터 저장소 생성 함수
def create_vectorstore(documents) -> FAISS:
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    return FAISS.from_documents(documents, embeddings)


# 데이터 벡터화 처리 함수
# 메인 처리 함수
def main():
    # 데이터 로드
    singleton_data = load_jsonl("./total_kor_counsel_bot.jsonl")
    multiturn_data = load_jsonl("./total_kor_multiturn_counsel_bot.jsonl")

    # 문서 생성
    singleton_docs = process_data(singleton_data, "singleton")
    multiturn_docs = process_data(multiturn_data, "multiturn")
    all_docs = singleton_docs + multiturn_docs

    # 벡터 저장소 생성 및 저장
    vectorstore = create_vectorstore(all_docs)
    vectorstore.save_local("faiss_counseling_index")
    print("벡터 저장소가 성공적으로 생성되고 저장되었습니다.")


if __name__ == "__main__":
    main()
