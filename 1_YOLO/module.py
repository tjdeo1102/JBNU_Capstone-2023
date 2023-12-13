import os
import csv
import cv2 as cv
import numpy as np
from shapely.geometry import Polygon, Point

class PolygonCenter:
    def __init__(self, input_Predict_path):
        # 입력 디렉토리 경로, 모델 예측시 저장되는 폴더로 자도 매핑
        self.input_directory_path = os.path.join(input_Predict_path,'labels')
        # 이미지 디렉토리 경로, 모델 예측시 저장되는 폴더로 자도 매핑
        self.images_directory = os.path.join(input_Predict_path,'labels')
        # 출력 CSV 파일 경로
        self.output_csv_path = os.path.join(input_Predict_path,'output.csv')
        # CSV 파일에 저장할 데이터 리스트 초기화
        self.csv_data = [['id', 'pic_name', 'class', 'x', 'y' , 'x_min', 'y_min', 'x_max', 'y_max']]
        # id를 1부터 시작하기 위한 카운터
        self.id_counter = 1

    # 수정된 draw_contour_on_mask 함수
    def draw_contour_on_mask(self, size, poly, color=255):
        mask = np.zeros(size, dtype='uint8')
        coords = np.array(poly.exterior.xy).T.astype(np.int32)
        cnt = coords.reshape((-1, 1, 2))
        cv.fillPoly(mask, [cnt], color)
        return mask

    def get_furthest_point_from_edge_cv2(self, cnt):
        cnt = np.array(cnt)
        cnt = cnt.reshape(-1, 2)
        poly = Polygon(map(tuple, cnt))
        mask = self.draw_contour_on_mask((793, 793), poly)
        dist_img = cv.distanceTransform(mask, distanceType=cv.DIST_L2, maskSize=5).astype(np.float32)
        cy, cx = np.where(dist_img==dist_img.max())
        cx, cy = cx.mean(), cy.mean()
        return cx, cy

    def run(self):
        for txt_file_name in os.listdir(self.input_directory_path):
            if txt_file_name.endswith('.txt'):
                txt_file_path = os.path.join(self.input_directory_path, txt_file_name)
                image_name = os.path.splitext(txt_file_name)[0]

                with open(txt_file_path, 'r') as txt_file:
                    for idx, line in enumerate(txt_file, start=1):
                        parts = line.strip().split()
                        category_id, counts, bbox = int(parts[0]), list(map(float, parts[1:-5])) , list(map(float, parts[-4:]))
                        # Polygon 좌표를 이용하여 Polygon 내의 점 계산
                        point_x, point_y = self.get_furthest_point_from_edge_cv2(counts)
                        x1,y1,x2,y2 = bbox
                        # CSV 데이터에 추가
                        self.csv_data.append([self.id_counter, image_name, category_id, point_x, point_y, x1,y1,x2,y2])
                        self.id_counter += 1
       
        # CSV 파일로 저장
        with open(self.output_csv_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(self.csv_data)
        print(f"CSV file has been saved to {self.output_csv_path}")

        #csv 경로 반환
        return self.output_csv_path
