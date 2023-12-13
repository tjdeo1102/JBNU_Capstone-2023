import os
import processing
from qgis.core import QgsRasterLayer, QgsProject, QgsVectorLayer


##레이어들 병합하고 qgis에 추가##
def Calculate_All_Extent_tif_files(folder_path):
    # 폴더 내의 TIF 파일 목록 가져오기
    tif_files = [f for f in os.listdir(folder_path) if f.endswith('.tif')]

    # 레이어 객체들을 저장할 리스트
    raster_layers = []

    # 각 TIF 파일을 레이어로 변환하고 리스트에 추가
    for tif_file in tif_files:
        tif_path = os.path.join(folder_path, tif_file)
        layer_name = os.path.splitext(tif_file)[0]  # 파일 이름에서 확장자를 제외한 부분을 레이어 이름으로 사용
        
        # QGIS 래스터 레이어를 생성하고 추가
        raster_layer = QgsRasterLayer(tif_path, layer_name, 'gdal')
        if raster_layer.isValid():
            raster_layers.append(raster_layer)
        else:
            print(f"Error loading layer: {layer_name}")

    # Layers 정보 추출 알고리즘 실행
    if raster_layers:
        alg_params = {
            'LAYERS': raster_layers,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }

        res = processing.run("native:exportlayersinformation", alg_params)

        if res['OUTPUT'].isValid():
            print("Merged layer added to QGIS project.")
            QgsProject.instance().addMapLayer(res['OUTPUT'])
            return res['OUTPUT']
        else:
            print("Error loading merged layer.")
    else:
        print("No valid raster layers to merge.")