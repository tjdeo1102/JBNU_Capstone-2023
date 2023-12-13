from qgis.core import QgsVectorLayer, QgsField, QgsFeature, QgsGeometry, QgsPointXY, QgsProject, QgsRasterLayer
from qgis.PyQt.QtCore import QVariant
from PIL import Image

def real_world_size(tif_file_path):
    # 래스터 레이어 생성
    raster_layer = QgsRasterLayer(tif_file_path, 'outputt')

    # 래스터 레이어가 성공적으로 로드되었는지 확인
    if not raster_layer.isValid():
        print('레이어를 로드할 수 없습니다.')
    else:
        # 래스터 레이어의 extent 가져오기
        extent = raster_layer.extent()

        # 최소 및 최대 X 및 Y 좌표 가져오기
        min_x = extent.xMinimum()
        min_y = extent.yMinimum()
        max_x = extent.xMaximum()
        max_y = extent.yMaximum()
        x = max_x - min_x
        y = max_y - min_y
        

    # 래스터 레이어 제거 (옵션)
    QgsProject.instance().removeMapLayer(raster_layer)
    return min_x, min_y, max_x, max_y, x, y

def picture_world_size(tif_file_path):
    # TIF 파일 열기
    tif_image = Image.open(tif_file_path)

    # 이미지의 너비와 높이 가져오기
    image_width, image_height = tif_image.size

    # 해상도 가져오기 (DPI 또는 DPM)
    dpi_x, dpi_y = tif_image.info.get('dpi', (None, None))

    # 픽셀 크기 계산 (1인치 또는 1밀리미터 당 픽셀 수)
    if dpi_x is not None and dpi_y is not None:
        pixel_size_x = 25.4 / dpi_x  # 1인치 = 25.4 밀리미터
        pixel_size_y = 25.4 / dpi_y  # 1인치 = 25.4 밀리미터
    else:
        pixel_size_x = None
        pixel_size_y = None

    # 이미지 닫기
    tif_image.close()
    return image_width, image_height

def fix_position(x_or_y, point,tif_file_path):
    real_world_min_x, real_world_min_y, real_world_max_x, real_world_max_y, real_world_width, real_world_height = real_world_size(tif_file_path)

    picture_world_width, picture_world_height =  picture_world_size(tif_file_path)
    print(f'picture_world_width: {picture_world_width}')
    print(f'picture_world_height: {picture_world_height}')

    if x_or_y == 'x':
        x_value_diff = real_world_width * point / picture_world_width
        x_value = real_world_min_x + x_value_diff
        return x_value
    elif x_or_y == 'y':
        y_value_diff = real_world_height * point / picture_world_height 
        y_value = real_world_max_y - y_value_diff
        return y_value
    else:
        print("좌표 수정중 오류 발생")
        return None   

##csv에서 포인트 정보 추출해서 레이어 추가##
def create_point_layer_from_csv(csv_path, input_tif_folder, target_crs='EPSG:5186', optional_point = 0):
    # CSV 파일에서 데이터 읽기
    with open(csv_path, 'r') as file:
        # CSV 파일의 첫 줄은 헤더 정보로 간주
        header = file.readline().strip().split(',')

        # 필드 인덱스 찾기
        x_index = header.index('x')
        y_index = header.index('y')
        class_index = header.index('class')
        pic_name_index = header.index('pic_name')
        x_min_index = header.index('x_min')
        y_min_index = header.index('y_min')
        x_max_index = header.index('x_max')
        y_max_index = header.index('y_max')
        

        # 레이어 생성
        layer = QgsVectorLayer(f'Point?crs={target_crs}', 'PointsLayer', 'memory')
    

        # 필드 정의
        layer_fields = [QgsField('origin_file', QVariant.String),
                        QgsField('class', QVariant.String),
                        QgsField('x', QVariant.Double),
                        QgsField('y', QVariant.Double),
                        QgsField('x_min', QVariant.Double),
                        QgsField('y_min', QVariant.Double),
                        QgsField('x_max', QVariant.Double),
                        QgsField('y_max', QVariant.Double),
                        ]

        layer.dataProvider().addAttributes(layer_fields)
        layer.updateFields()

        # CSV 파일에서 데이터 읽어와서 레이어에 추가
        for line in file:

            data = line.strip().split(',')

            # 클래스, x, y 값 추출
            pic_name = data[pic_name_index]
            class_value = data[class_index]
            x_value = float(data[x_index])
            y_value = float(data[y_index])
            x_min = float(data[x_min_index])
            y_min = float(data[y_min_index])
            x_max = float(data[x_max_index])
            y_max = float(data[y_max_index])
          
            tif_file_path= input_tif_folder +  "/" + str(data[pic_name_index]) + ".tif"
            
            if optional_point == 0: #기존 segmentation의 중심좌표를 가져오는 경우
                x_value = fix_position('x',x_value,tif_file_path)

                y_value = fix_position('y',y_value,tif_file_path)
            else:
                x_value = fix_position('x', (x_min+x_max)/2, tif_file_path) ##bbox의 중심좌표
                y_value = fix_position('y', (y_min+y_max)/2, tif_file_path)


            print(f'y_value: {y_value}')
            print(f'x_value: {x_value}')
            # 속성 설정

            f = QgsFeature()
            f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(x_value, y_value)))
            f.setFields(layer.fields())
            f['class'] = class_value
            f['x'] = x_value
            f['y'] = y_value
            f['origin_file'] = pic_name+'.tif'
            f['x_min'] = x_min
            f['y_min'] = y_min
            f['x_max'] = x_max
            f['y_max'] = y_max

            

            # 레이어에 포인트 추가
            if layer.isValid():
                layer.startEditing()
                layer.addFeature(f)
                layer.commitChanges()

        layer.updateExtents()
        # QGIS에 레이어 추가

        if layer.isValid():
            QgsProject.instance().addMapLayer(layer)
            print("Points layer added")
            return layer
        else:
            print("Error Points layer.")