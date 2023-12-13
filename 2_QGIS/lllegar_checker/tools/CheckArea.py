from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant
import pandas as pd
import processing
import os
from PIL import Image, ImageDraw

##불법 점유 판독기
def check_using_area(input_layer,input_raster_folder, output_dir):
    #클래스 id별 이름 매핑 리스트
    class_name = [None,"Water","Car","Road","Farmland","Greenhouse","Building","Bale silage","Tent","Garbage"]
    if input_layer.isValid():
        # 문제 사유 필드 생성
        new_field_name = 'reason'
        new_field_type = QVariant.String  # 필요에 따라 다른 유형 선택
        input_layer.dataProvider().addAttributes([QgsField(new_field_name, new_field_type)])

        # 필드 파일명을 오름차순 정렬
        config = input_layer.attributeTableConfig()
        config.setSortExpression('origin_file') # name of the field
        config.setSortOrder(0) # 0:ascending 1:descending

        # 필드 업데이트
        input_layer.updateFields()

        # 필드의 모든 피처(레코드)를 불러옴
        problem_area = [] #불법 지역 결과 저장할 리스트
        features = input_layer.getFeatures()
        last_area = None
        ploblem_objs = [] #해당 지역의 문제 요소 체크
        # 추출된 피처들에 대한 작업 수행
        for feature in features:
            if last_area is not None and feature is not None: #
                if last_area['origin_file'] != feature['origin_file']: #현재 지역과 지난번 지역이 다른 경우 체크 시작
                    if last_area['A19'] == '17': #하천 지목만 확인
                        for obj in ploblem_objs: #문제의 물체가 있는 경우에만 순회
                            obj['reason'] = f"하천 지역에서 {class_name[int(obj['class'])]}이(가) 검출"
                            problem_area.append(obj)
                        ploblem_objs.clear() #저장했던 물체들 리스트 초기화

            #그외의 경우는 ploblem_num 0이고 지역이 같거나 다르거나 갱신할 요소가 없으므로 그대로 진행

            # class 필드 값 가져오기
            class_value = feature['class']

            # class 여부 검사 (여기에서 피처의 지목과 비교를 통해 불법 탐지)
            if class_value == '1': #물 클래스
                pass #현재 미구현
            elif class_value == '2': #자동차 클래스
                pass #현재 미구현
            elif class_value == '3': #도로 클래스
                pass #현재 미구현
            elif class_value == '4': #경작지 클래스
                if feature['A19'] == '17': #하천 지역이면서 경작지 있는 경우
                    ploblem_objs.append(feature)
                pass #현재 미구현
            elif class_value == '5': #비닐하우스 클래스
                if feature['A19'] == '17': #하천 지역이면서 비닐하우스 있는 경우
                    ploblem_objs.append(feature)
            elif class_value == '6': #가건물 클래스
                if feature['A19'] == '17': #하천 지역이면서 건물 있는 경우
                    ploblem_objs.append(feature)
            elif class_value == '7': #곤포 사일리지 클래스
                pass #현재 미구현
            elif class_value == '8': #천막 클래스
                if feature['A19'] == '17': #하천 지역이면서 천막 있는 경우
                    ploblem_objs.append(feature)
            elif class_value == '9': #쓰레기 클래스
                pass #현재 미구현

            #last_area 갱신 && 불법 체크 갱신
            last_area = feature
        

        # 결과 정보를 저장할 data리스트
        data = []

        if not problem_area:
            print("No features selected in the mask layer. ==> No_Problem_area")
        else:
            #tif 타일들 불러오기 
            tif_file_names = [file for file in os.listdir(input_raster_folder) if file.endswith(".tif")]
            last_tif = ""
            img = None
            draw = None
            # 각 피처에 대해 개별적으로 클립 래스터 생성
            for feature in problem_area:
                # Check if the file name matches any of the field names
                if feature['origin_file'] in tif_file_names:
                    if last_tif != feature['origin_file']: #서로 다른 물체가 이미지도 다르면, 이미지를 새롭게 갱신, 또한 저장 (이미 tif이름순 정렬 되어있음)
                        # If matched, copy the file to the output folder
                        file_name = feature['origin_file']
                        file_path = os.path.join(input_raster_folder, file_name)
                        if img != None: #처음에 img바뀌는 경우 제외, 이미지가 갱신되기전에 기존 이미지를 저장
                            output_path = os.path.join(output_dir, last_tif) #이전 이미지 경로
                            img.save(output_path)
                        last_tif = file_name #이전 이미지 경로 갱신
                        # 새로운 이미지 열기
                        img = Image.open(file_path)
                        draw = ImageDraw.Draw(img)
                    # 불법이라고 판단한 객체들, 빨간선으로 긋고 텍스트 삽입
                    draw.rectangle([feature['x_min'], feature['y_min'], feature['x_max'], feature['y_max']], outline=(255, 0, 0), width=5)

                    # 텍스트 그리기 (폰트 에러 안뜨게 하기위해)
                    text = class_name[int(feature['class'])]
                    draw.text((feature['x_min'], feature['y_min']),text , fill=(255, 255, 255))
                    
                # 넣을 필드 및 값 추가
                row_data = {
                    '파일': feature['origin_file'],
                    '필지 고유번호': feature['A0'],
                    '법정동명': feature['A2'],
                    '검출된 물체 번호': feature['class'],
                    '지목코드': feature['A19'],
                    '지목명': feature['A20'],
                    'Reason': feature['reason']
                }
                data.append(row_data)

            #마지막 draw에 대한 피처저장
            output_path = os.path.join(output_dir, last_tif) #이전 이미지 경로
            img.save(output_path)

        # 데이터프레임 생성
        df = pd.DataFrame(data)

        # CSV 파일로 저장
        csv_path = f'{output_dir}/clipped_raster_info.csv'
        df.to_csv(csv_path, index=False, encoding='euc-kr')

        print(f"CSV file saved to: {csv_path}")