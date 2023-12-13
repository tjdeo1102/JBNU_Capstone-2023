import processing
from qgis.core import QgsRasterLayer,QgsProcessingFeatureSourceDefinition
import os

#-b 1 -b 2 -b 3 -burn 0 -burn 0 ==> 기존 burn in 30


def PaintArea(input_vec_layer, input_raster_folder ,field_id ,field_value):
    #먼저 필드 아이디와 필드 value에 해당되는 지역만 선택
    parameter_dictionary = {
        'INPUT': input_vec_layer,
        'FIELD': field_id,
        'METHOD': 0,
        'OPERATOR': 0,
        'VALUE': field_value
    }
    processing.run("qgis:selectbyattribute", parameter_dictionary)

    sel = processing.run("qgis:saveselectedfeatures", {'INPUT': input_vec_layer, 'OUTPUT': 'TEMPORARY_OUTPUT' })

    sel_area = sel['OUTPUT']
    #sel_area = input_vec_layer
    
    #영역의 경계선을 그리기 위해 위에서 구했던 선택영역의 경계선을 만든다.
    parameter_dictionary3 = {
                'INPUT': sel_area,
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
    res = processing.run("native:boundary", parameter_dictionary3)

    #선이 가늘기 때문에, 버퍼를 이용해 선을 두껍게 만든다.
    parameter_dictionary4 = {
                'INPUT': res['OUTPUT'],
                'DISTANCE': 0.3,
                'OUTPUT': 'TEMPORARY_OUTPUT'
            }
    res2 = processing.run("native:buffer", parameter_dictionary4)
    
    #위의 결과로 선택된 영역을 tif에 칠해준다.
    tif_files = [f for f in os.listdir(input_raster_folder) if f.endswith('.tif')]

    for tif in tif_files:
        tif_path = os.path.join(input_raster_folder, tif)
        # QGIS 래스터 레이어를 생성하고 추가
        raster_layer = QgsRasterLayer(tif_path, tif_path, 'gdal')
        if raster_layer.isValid():
            #래스터화의 기능을 이용해 두 레스터 오버랩
            parameter_dictionary2 = {
                'INPUT': sel_area,
                'INPUT_RASTER': raster_layer,
                'BURN': 0,
                'ADD': True,
                'EXTRA': '-b 1 -b 2 -b 3 -burn 0 -burn 40'
            }
            processing.run("gdal:rasterize_over_fixed_value", parameter_dictionary2)

            parameter_dictionary5 = {
                'INPUT': res2['OUTPUT'],
                'INPUT_RASTER': raster_layer,
                'BURN': 255,
                'ADD': True,
                'EXTRA': '-b 3'
            }
            processing.run("gdal:rasterize_over_fixed_value", parameter_dictionary5)

        else:
            print(f"Error loading layer: {raster_layer}")



    