import yolo_prediction,module,os

#예측할 이미지가 있는 폴더
input_orgin_tif_folder = ""

#예측된 이미지를 저장할 폴더
output_folder = ""

#사용할 모델 가중치 (yolo8)
model_pth = os.path.join(os.path.dirname(os.path.realpath(__file__)),"best.pt")

############디텍션할 모델 생성 및 예측 결과 저장###########
input_predict_folder = yolo_prediction.Prediction(model_pth,input_orgin_tif_folder,output_folder).predict()

############결과 파일, 폴리곤 비주얼 중심좌표로 변환해서 저장#########
csv_path = module.PolygonCenter(input_predict_folder).run()