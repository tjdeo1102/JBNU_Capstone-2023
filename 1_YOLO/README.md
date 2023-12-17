# 첫번째 트랙 과정
---
 YOLOV8을 이용해 이미지속 객체 탐지를 진행하는 과정입니다.
 
 미리 학습된 가중치를 이용해 예측을 하고 필요한 레이블 정보만 csv로 저장합니다.
 
 Conda환경 세팅, ultralytics, shapely가 정상적으로 설치되어야 다음 과정 수행이 가능합니다.

 본문의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/blob/main/README.md)의 설치를 완료했다면 다음 과정을 수행해주세요.


## 과정
---

1. main.py을 열어줍니다.

2. input_orgin_tif_folder에는 예측할 이미지들이 있는 폴더로 설정해줍니다.

3. output_folder에는 저장할 경로로 설정해줍니다.

4. 미리 설치해둔 가상환경을 통해 main.py를 실행해줍니다.

5. 설치 후, 저장경로에 예측된 이미지가 저장됩니다.
   
6. 또한, 이미지내의 객체 정보를 포함하는 다음과 같은 output.csv가 저장됩니다.
   ![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/57614322/b379179e-b39f-4e0d-9de4-c1f5210cfd51)


