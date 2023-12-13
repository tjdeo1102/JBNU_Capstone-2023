import processing

##범위로 레이어 추출##
def extract_layer_by_extent(input_layer, reference_layer):
    # 프로세스 실행
    result = processing.run("qgis:extractbyextent", {
        'INPUT': input_layer,
        'EXTENT': reference_layer,
        'CLIP': True,
        'OUTPUT': 'memory:'
    })

    # 추출된 결과 레이어를 추가
    output_layer = result['OUTPUT']
    if output_layer.isValid():
        print("Extract layer")
        return output_layer
    else:
        print("Error Extract layer.")