import os
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageDraw

class Prediction():
    def __init__(self,model_pth,image_dir, output):
        self.model = YOLO(model_pth)
        self.image_dir = image_dir
        #원본 사진과 predict 사진 구분을 위해
        self.output_dir = os.path.join(output, 'Predict')


    def predict(self):
        # 결과를 저장할 텍스트 파일 디렉토리 생성
        labels_dir = os.path.join(self.output_dir, 'labels')
        os.makedirs(labels_dir, exist_ok=True)

        # 이미지 출력 디렉토리 생성
        output_images_dir = os.path.join(self.output_dir, 'images')
        os.makedirs(output_images_dir, exist_ok=True)

        # 이미지 파일들에 대한 추론 및 결과 저장
        for filename in os.listdir(self.image_dir):
            if filename.endswith(".tif"):
                source = os.path.join(self.image_dir, filename)

                # 소스에서 추론 실행
                results = self.model.predict(source)

                # 이미지 열기
                img = Image.open(source)
                draw = ImageDraw.Draw(img)

                # 결과를 저장할 텍스트 파일 열기
                output_file = os.path.join(labels_dir, f"{os.path.splitext(filename)[0]}.txt")
                with open(output_file, 'w') as f:
                    for result in results:
                        masks = result.masks
                        boxes = result.boxes
                        if masks is None or boxes is None:
                            continue
                        for mask, box in zip(masks, boxes):
                            polygon = mask.xy[0]
                            class_id = int(box.cls)

                            x, y, w, h = box.xyxy[0].tolist()
                            x_min, y_min, x_max, y_max = map(int, [x, y, w, h])

                            if class_id in [4,5,6,8]:
                                draw.rectangle([x_min, y_min, x_max, y_max], outline=(0, 255, 0), width=5)

                                # .txt 파일에 저장
                                f.write(f"{class_id} ")
                                for point in polygon:
                                    f.write(f"{point[0]} {point[1]} ")
                                f.write(f"bbox {x_min} {y_min} {x_max} {y_max} ")
                                f.write("\n")

                # .txt 파일 저장 후 이미지 저장
                output_image_path = os.path.join(output_images_dir, f"{os.path.splitext(filename)[0]}.tif")
                img.save(output_image_path)
        return self.output_dir