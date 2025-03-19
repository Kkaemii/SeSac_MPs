from ultralytics import YOLO


# 모델 학습 시작
def train_yolo(data_path, model_path, epochs, batch_size):
    print("YOLO 학습 시작...\n")
    model = YOLO(model_path)  # 모델 로드
    model.train(
        data=data_path,
        epochs=epochs,
        batch=batch_size,
        patience=patience,
        device=device,
    )


# 예측 함수
def predict_yolo(model_weights, source_path, conf=0.25, save_results=True):
    print("YOLO 예측 시작...\n")
    model = YOLO(model_weights)  # 학습된 가중치 로드
    results = model.predict(
        source=source_path, conf=conf, device=device, save=save_results
    )
    return results


# 결과는 predict 폴더에서 확인 가능

if __name__ == "__main__":
    # 학습 파라미터 설정
    data_yaml_path = "./assets/data.yaml"  # 데이터셋 YAML 파일 경로
    initial_model_path = "yolov8n.pt"  # YOLO 초기 모델 (사전학습된 가중치)
    epochs = 100  # 학습 에포크 수
    batch_size = -1  # 배치 크기
    patience = 300  # 10회이상 loss변화 없으면 작업 종료
    device = 0  # gpu 사용

    # 예측 파라미터 설정
    trained_weights_path = "./runs/detect/train3_patience_5_epochs_27/weights/best.pt"  # 학습된 가중치 경로
    image_or_folder_path = "./assets/test_set"  # 예측할 이미지 또는 폴더 경로

    # image_or_folder_path = "./assets/test/images"

    # 원하는 작업 실행 (주석 해제하여 사용)

    # Step 1: YOLOv8 학습 실행
    # train_yolo(data_yaml_path, initial_model_path, epochs, batch_size)

    # Step 2: YOLOv8 예측 실행
    predict_yolo(trained_weights_path, image_or_folder_path)


## 리팩토링 후

from ultralytics import YOLO


class YOLOTrainer:
    def __init__(self, device=0):
        """
        YOLOTrainer 클래스 초기화
        :param device: 사용할 디바이스 (GPU: 0, CPU: 'cpu')
        """
        self.device = device

    def train(self, data_path, model_path, epochs, batch_size, patience):
        """
        YOLO 모델 학습 함수
        :param data_path: 데이터셋 YAML 파일 경로
        :param model_path: 초기 모델 경로 (사전학습된 가중치)
        :param epochs: 학습 에포크 수
        :param batch_size: 배치 크기
        :param patience: 학습 중단 조건 (loss 변화 없을 시)
        """
        print("YOLO 학습 시작...\n")
        model = YOLO(model_path)  # 모델 로드
        model.train(
            data=data_path,
            epochs=epochs,
            batch=batch_size,
            patience=patience,
            device=self.device,
        )

    def predict(self, model_weights, source_path, conf=0.25, save_results=True):
        """
        YOLO 예측 함수
        :param model_weights: 학습된 가중치 경로
        :param source_path: 예측할 이미지 또는 폴더 경로
        :param conf: confidence threshold (신뢰도 임계값)
        :param save_results: 결과 저장 여부
        :return: 예측 결과 객체
        """
        print("YOLO 예측 시작...\n")
        model = YOLO(model_weights)  # 학습된 가중치 로드
        results = model.predict(
            source=source_path,
            conf=conf,
            device=self.device,
            save=save_results,
        )
        return results


if __name__ == "__main__":
    # 파라미터 설정
    data_yaml_path = "./assets/data.yaml"  # 데이터셋 YAML 파일 경로
    initial_model_path = "./yolov8n.pt"  # YOLO 초기 모델 (사전학습된 가중치)
    epochs = 100  # 학습 에포크 수
    batch_size = -1  # 배치 크기
    patience = 300  # loss 변화 없을 시 작업 종료 조건

    trained_weights_path = "./runs/detect/train3_patience_5_epochs_27/weights/best.pt"  # 학습된 가중치 경로
    image_or_folder_path = "./assets/test_set"  # 예측할 이미지 또는 폴더 경로

    # YOLOTrainer 인스턴스 생성 및 작업 실행
    yolo_trainer = YOLOTrainer(device=0)

    # Step 1: YOLOv8 학습 실행 (주석 해제하여 사용)
    # yolo_trainer.train(data_yaml_path, initial_model_path, epochs, batch_size, patience)

    # Step 2: YOLOv8 예측 실행 (주석 해제하여 사용)
    results = yolo_trainer.predict(trained_weights_path, image_or_folder_path)
