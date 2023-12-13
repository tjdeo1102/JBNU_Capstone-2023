import processing
from qgis.core import QgsProject

##인터섹션 수행
def perform_intersection(inputLayer, overlayLayer):
    # 알고리즘 파라미터 설정
    params = {
        'INPUT': inputLayer,
        'OVERLAY': overlayLayer,
        'OUTPUT': 'memory:'
    }

    # qgis:intersection 알고리즘 실행
    res = processing.run("qgis:intersection", params)

    # 결과 레이어를 QGIS에 추가
    result_layer = res['OUTPUT']

    if result_layer.isValid():
        QgsProject.instance().addMapLayer(result_layer)
        print("Intersection layer added to QGIS project.")
        return result_layer
    else:
        print("Error loading Intersection layer.")
    