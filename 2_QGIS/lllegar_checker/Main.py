from .tools import NewPointAssign,Merge,Extract,CheckArea,CsvToPoints,Intersection,LeftJoin,CalculatorAllArea,PaintArea
import os

################################################
################메인부분#########################
################################################
class lllegalCheckMain():
    def __init__(self,input_img,input_dbf,input_model_out ,output_dir, check_op):

        # 원본 레스터들 있는 폴더
        self.input_orgin_tif_folder = input_img

        # 모델에서 나온 이미지(입력될 tif)들 있는 폴더
        self.input_predict_folder = os.path.join(input_model_out,"images")

        # 행정 데이터 dbf가 있는 폴더
        self.input_dbf_folder = input_dbf

        # 점 CSV 파일 경로
        self.csv_path = os.path.join(input_model_out,"output.csv")

        # 불법 결과가 저장될 폴더
        self.output_folder = output_dir

        # 불법 탐지 기준 (0: 세그멘테이션 무게중심 1: 바운딩박스 중점)
        self.check_op = check_op

    def run(self):

        ############레스터 좌표 부여#####################
        NewPointAssign.add_coordinates_to_output(self.input_orgin_tif_folder,self.input_predict_folder)

        # ############레스터 병합 부분#####################
        # tif_merge=Merge.merge_tif_files(self.input_predict_folder)

        ##############레스터 전체 크기 계산 부분############ --> 레스터를 합치지 않아도 전체 레스터를 계산할 방법을 찾음
        tifs_Inf = CalculatorAllArea.Calculate_All_Extent_tif_files(self.input_predict_folder)

        ############지적도 파일들 병합(벡터 병합) 부분#############
        dbf_merge = Merge.merge_dbf_files(self.input_dbf_folder)

        ############사진 크기만큼 지적도 레이어를 추출#####################
        extract_layer = Extract.extract_layer_by_extent(dbf_merge, tifs_Inf)

        ############주어진 점의 좌표와 클래스 이름에 따라 점 생성###########
        points_layer = CsvToPoints.create_point_layer_from_csv(self.csv_path,self.input_predict_folder,target_crs='EPSG:5186', optional_point=self.check_op) ##optional 인자는 0:세그멘테이션 중점, 1: 바운딩박스 중점

        ############점레이어를 지적도레이어랑 인터섹션해서 각 점의 지역 정보 추출###########
        intersection_result = Intersection.perform_intersection(points_layer, extract_layer)

        ############전체레이어와 인터섹션 레이어와 조인해서 모든 레이어의 점 포함 여부 테이블 생성#################
        leftjoin_result = LeftJoin.left_join_layers(
            extract_layer,
            intersection_result,
            'A0',
            'A0',
            ["origin_file","class","x","y","x_min","y_min","x_max","y_max"]#pointsLayer에서 살릴 필드들만 적기
        )

        #############조인된 테이블에서 지목, 클래스에 따라서 불법점유 판독 및 결과 저장#####################
        CheckArea.check_using_area(leftjoin_result, self.input_predict_folder , self.output_folder)

        ############결과 레스터 좌표 부여#####################
        NewPointAssign.add_coordinates_to_output(self.input_orgin_tif_folder,self.output_folder)

        ############하천지목 경계 표시#######################
        PaintArea.PaintArea(extract_layer,self.output_folder,'A19','17')
