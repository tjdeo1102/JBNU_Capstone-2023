import os
import processing
from qgis.core import QgsProject

##left 외부 조인
def left_join_layers(original_layer, join_layer, join_field, target_field, using_field_names_list): 
    params = {
        'INPUT': original_layer,
        'FIELD': join_field,
        'INPUT_2': join_layer,
        'FIELD_2': target_field,
        'FIELDS_TO_COPY': using_field_names_list,
        'METHOD': 0, ##1:N 조인 수행
        'OUTPUT': 'memory:'
    }

    res = processing.run("qgis:joinattributestable", params)

    # 결과 레이어를 QGIS에 추가
    result_layer = res['OUTPUT']

    if result_layer.isValid():
        QgsProject.instance().addMapLayer(result_layer)
        print("Merged left join layer added to QGIS project.")
        return result_layer
    else:
        print("Error loading Merged left join layer.")