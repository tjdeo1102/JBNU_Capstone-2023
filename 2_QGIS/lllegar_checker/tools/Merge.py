import os
import processing
from qgis.core import QgsRasterLayer, QgsProject

##행정데이터 dbf파일들 병합
def merge_dbf_files(folder_path):
    # 폴더 내의 모든 DBF 파일 경로 가져오기
    dbf_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.dbf')]

    # Merge Vector Layers 알고리즘 실행
    result = processing.run("qgis:mergevectorlayers",
                            {'LAYERS': dbf_files,
                             'OUTPUT': 'memory:'})

    # 결과 레이어 가져오기
    merged_layer = result['OUTPUT']

    if merged_layer.isValid():
        print("Merged dbf layer")
        return merged_layer
    else:
        print("Error Merged dbf layer")

##레이어들 병합하고 qgis에 추가##
def merge_tif_files(folder_path):
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

    # GDAL merge 알고리즘 실행
    if raster_layers:
        alg_params = {
            'INPUT': raster_layers,
            'PCT': False,
            'SEPARATE': False,
            'NODATA_INPUT': None,
            'NODATA_OUTPUT': None,
            'OPTIONS': '',
            'EXTRA': '',
            'DATA_TYPE': 0,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }

        res = processing.run("gdal:merge", alg_params)

        # 병합된 레스터를 QGIS 프로젝트에 추가
        merged_layer = QgsRasterLayer(res['OUTPUT'], 'merge', 'gdal')
        if merged_layer.isValid():
            QgsProject.instance().addMapLayer(merged_layer)
            print("Merged layer added to QGIS project.")
            return merged_layer
        else:
            print("Error loading merged layer.")
    else:
        print("No valid raster layers to merge.")