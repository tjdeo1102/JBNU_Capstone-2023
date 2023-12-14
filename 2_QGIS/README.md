# 두번째 트랙 과정
---

QGIS의 플러그인을 이용하여 예측된 객체의 불법 여부를 판단하는 과정입니다.

미리 설치된 QGIS에서 플러그인 설치 후, 해당 플러그인을 실행해서 진행됩니다.

QGIS 3.34가 정상적으로 설치되어야 다음 과정 수행이 가능합니다.

또한, 모든 데이터의 좌표계가 EPSG:5186으로 재투영해주어야 됩니다. 해당 방법은 다음 [링크](https://docs.qgis.org/3.34/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html?highlight=native%20reprojectlaye)를 참고하세요.

본문의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/blob/main/README.md)의 설치를 완료했다면 다음 과정을 수행해주세요.

## 과정
---

1. 미리 설치해둔 QGIS 3.34 을 실행합니다.

2. 상단의 플러그인-플러그인 관리 및 설치-ZIP 파일에서 설치 순으로 들어갑니다.

3. lllegar_checker.zip의 경로를 설정하고 플러그인 설치를 합니다.

4. 다시 상단의 플러그인-lllegalAreaChecker-lllegalAreaChecker 순으로 들어갑니다.

5. 나타난 팝업창에서 다음의 설명에 맞게 경로를 설정합니다.
   
   + Input Image: 예측할 원래 이미지들이 있는 경로입니다.
          
   + Check Opt
     
      + Bounding Box Centroid: 예측된 바운딩 박스의 무게중심을 기준으로 불법 객체를 판단합니다.
      + Polygon Box Centroid: 예측된 폴리곤 박스의 무게중심을 기준으로 불법 객체를 판단합니다.
        
   + Input dbf: 행정데이터(토지소유정보)가 있는 폴더 경로입니다.
     
   + Input model: 첫번째 트랙의 결과로 나온 Prediction폴더 경로입니다.
     
   + Output Path: 최종 결과를 저장할 경로입니다.

6. 확인을 눌러 작업을 시작합니다.

7. 최종 결과로 예측된 이미지들과 이미지들의 정보가 저장된 csv가 출력됩니다.
