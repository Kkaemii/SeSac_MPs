from ultralytics import YOLO


# 모델 학습 시작
def train_yolo(data_path, model_path, epochs, batch_size):
    print("YOLO 학습 시작...\n")
    model = YOLO(model_path)  # 모델 로드
    model.train(data=data_path, epochs=epochs, batch=batch_size)


# 예측 함수
def predict_yolo(model_weights, source_path, conf=0.25, save_results=True):
    print("YOLO 예측 시작...\n")
    model = YOLO(model_weights)  # 학습된 가중치 로드
    results = model.predict(source=source_path, conf=conf, save=save_results)
    return results


# 결과는 predict 폴더에서 확인 가능

if __name__ == "__main__":
    # 학습 파라미터 설정
    data_yaml_path = "./assets/data.yaml"  # 데이터셋 YAML 파일 경로
    initial_model_path = "yolov8n.pt"  # YOLO 초기 모델 (사전학습된 가중치)
    epochs = 30  # 학습 에포크 수
    batch_size = 64  # 배치 크기

    # 예측 파라미터 설정
    trained_weights_path = "./runs/detect/train/weights/best.pt"  # 학습된 가중치 경로
    image_or_folder_path = "./assets/test_set"  # 예측할 이미지 또는 폴더 경로

    # 원하는 작업 실행 (주석 해제하여 사용)

    # Step 1: YOLOv8 학습 실행
    # train_yolo(data_yaml_path, initial_model_path, epochs, batch_size)

    # Step 2: YOLOv8 예측 실행
    predict_yolo(trained_weights_path, image_or_folder_path)
