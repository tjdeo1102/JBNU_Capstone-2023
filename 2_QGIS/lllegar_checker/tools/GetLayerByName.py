from qgis.core import QgsProject

##이름으로 레이어찾기##
def get_layer_by_name(layer_name):
    # 레이어 이름으로 레이어 찾기
    layer = QgsProject.instance().mapLayersByName(layer_name)
    # 레이어가 존재하는지 확인
    if layer:
        return layer[0]
    else:
        return None