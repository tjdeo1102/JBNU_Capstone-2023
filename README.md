# 2023-2 전북대학교 SW 캡스톤디자인 2023

해당 프로젝트는 **한국국토정보공사**(이하 [LX](https://www.lx.or.kr/kor.do)) x 팀 온새미로가 함께 진행했습니다.([Link](https://www.jbyonhap.com/news/articleView.html?idxno=412660&page=3&total=368217))

## 팀 온새미로

|성명|역할|
|:---:|:---:|
| [오주형](https://github.com/OH-JUHYONG) |   PM, AI모델 설계    |
| [소부승](https://github.com/bootkorea) | 데이터 전처리, AI모델 설계 |
| [김지성](https://github.com/zs0057) |  자료 정리 , QGIS 개발  |
| [곽성대](https://github.com/tjdeo1102) | 데이터 후처리, QGIS 개발 |

---

## 주제
### 고정밀 영상을 활용한 소하천 불법 점용 탐지 기법 개발
---
## 목적
### 하천 환경에 대한 국유지 무단 점용과 무분별한 사용으로 인한 피해를 최소화하기 위해 고정밀 영상과 AI 를 활용하여 하천의 불법 점용 의심 지역을 탐지
---
## 필요성
+ 하천의 불법 점유 및 무단 사용은 행정 관리 비용을 증가시키는 주요 요인 중 하나
+ 기존에는 각 시에서 불법 객체가 있다는 보고를 받고, 해당 구역이 하천 지목인지, 그리고 하천 지목에
보고 받은 불법 객체가 있는지, 실제로 불법 객체가 맞는지 사람이 모두 판단해야 하는 수고로움

![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/32a0161f-3138-4160-8622-887f3cb781d2)


: AI 모델과 QGIS 를 통해 해당 구역이 하천 지목인지 직접 확인할 필요가 없고, 하천 지목 위에 불법 객체가 있는지 알려줘 불법 점용 의심 지역을 확인

---

## 1. 전체 과정

![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/6f72dff2-bf0a-49a3-b364-f30eae4db030)

---

## 2. 무단 점용 기준 설정
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/015ad2dc-2ae3-486b-b081-936503a96a01)

![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/94fda3d8-1973-443c-bbed-7ee0ff3fe635)

+ 무단 점용에 대한 기준은 최대한 객관적인 사실에 근거하기 위해 법적 근거와 공문을 바탕으로 설정
+ 각 시의 공문에서 [「하천법」 제 33 조](https://glaw.scourt.go.kr/wsjo/lawod/sjo192.do?lawodNm=%ED%95%98%EC%B2%9C%EB%B2%95&jomunNo=33&jomunGajiNo=0) [위반 사례](https://www.siheung.go.kr/main/saeol/gosi/view.do?seCode=01&&notAncmtMgtNo=64066&mId=0401040100)를 참고
+ 공문의 내용 중 ‘불법 행위 내용’에 주목
	+ 지목이 하천으로 되어있으면 하천 용도로 쓰여야 한다는 의미
	+ 하천의 용도로 쓰여야 하는 곳에 해당 무단 점유물이 있어서 불법 점유다 라는 내용으로 해석
   + 위 내용에 근거해 불법 점유 기준을 정함

: 불법 점유의 근거가 되는 무단 점유 항목들과 불법 탐지 모델을 학습시키기 위한 데이터인 [아산시 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71387)의 레이블 중 가장 유사한 **경작지(004)**, **비닐하우스(005)**, **가건물(006)**, **천막(008)** 을 불법 객체로 정의

---

## 3. AI 불법 탐지 모델 설계
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/6b281661-936f-461c-b7f0-9c320b027fc8)

+ 모델을 학습하기 위해 사용한 데이터는 AI-HUB에 있는 [아산시 데이터](https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=71387)
+ 최종 단계에서 [QGIS](https://qgis.org/ko/site/forusers/download.html#)에 활용하기 위해 좌표계 정보 필요
  
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/ef5feac1-e042-447e-a771-436c295e7726)

+ 아산시 데이터는 9개의 레이블로 구성, 무단 점용의 기준이 되는 불법 객체의 내용을 반영해 데이터 전처리
+ 모델 학습시 적용한 데이터는 135,000장, 동일한 조건에서 모델을 학습
+ 학습 완료 후 여러 가지 성능 지표 이용해 모델의 성능 평가

: 가장 좋은 성능을 보여준 [**YOLOv8**](https://github.com/ultralytics/ultralytics)을 최종 모델로 선정

---

## 4. 불법 탐지
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/9f32c695-1e5d-44ef-b8e5-372f186cd44f)

+ 완성된 불법 탐지 모델을 통해 검출된 불법 객체들의 bounding box 좌표 정보와 polygon 좌표의 무게 중심을 추출하여 **csv 파일**에 저장
+ csv 파일을 지리 정보를 활용할 수 있는 [QGIS](https://qgis.org/ko/site/forusers/download.html#)에 넘김
+ 최종 단계에서 불법 점용 의심 지역을 알려주기 위해 QGIS에서 **2개의 지리 정보**(위 그림 참고) 사용

![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/e0ee4490-ce55-4727-8c51-2ec07e689be6)

+ 위 그림은 QGIS에서 2개의 지리 정보를 불러온 화면
+ 모델을 통해 검출된 **_불법 객체 정보를 담은 csv 파일_** 이 QGIS에 전달
+ 최종적으로 csv 파일에 있는 불법 객체가 **_하천 지목이라는 지리 정보에 위치_** 하면 불법 점용 의심 지역으로 판단

---

## 설치

1. 먼저 첫번째 트랙을 위해 VSCode에서 터미널에서 다음의 과정으로 Conda 가상환경을 준비해줍니다. (Conda가 설치되었다고 가정)

```"
conda create -n [가상환경명] python=3.8
```
```"
conda activate [가상환경명]
```
   
3. 다음의 필요한 라이브러리들을 설치해줍니다. (파이토치에 관한 설치는 따로 해주셔야 합니다.)

```"
pip install shapely
```
```"
pip install ultralytics
```
   
5. QGIS 3.34 버전을 설치해야 합니다. [다음](https://download.qgis.org/downloads/)의 링크를 통해 설치해주세요.
   
6. 사전에 드론맵을 준비해주세요(별도로 구해야됨, TIF파일 형식만 지원)
   
7. 드론맵에 해당되는 지역의 행정데이터(토지소유정보, DBF파일 형식만 지원)를 다음의 [링크](http://openapi.nsdi.go.kr/nsdi/index.do)를 통해 다운받습니다.
   
---
## 과정

### 첫번째 트랙
+ 1_YOLO폴더의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/blob/main/1_YOLO/README.md)를 참고해주세요.
   

### 두번째 트랙
+ 2_QGIS폴더의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/tree/main/2_QGIS)를 참고해주세요.

---

## 결과
두가지 유형을 담고있는 파일이 저장됩니다.

### 결과 이미지 예시
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/0e706b94-774f-4f22-9de8-bab7bcd33fd9)

(왼쪽의 사진은 모든 과정을 거쳐서 나온 결과 이미지, 오른쪽은 원본 이미지입니다.)
 + 파란색 배경: 하천 지목(필지의 지목이 하천인 곳)을 나타냅니다.
 + 초록색 박스: AI 모델에 의해 예측된 객체의 박스를 나타냅니다.
 + 빨간색 박스: 초록색 박스 중, 하천 지목에 있는 경우 불법 점용 의심 지역을 나타냅니다.

### 불법 의심 객체 정보를 담은 CSV파일
![image](https://github.com/tjdeo1102/JBNU_Capstone-2023/assets/90824684/29b7e4da-4c63-4e3e-8ca5-c07f2e9a7387)

   + 파일: 검출된 객체가 있는 이미지 파일
   + 필지 고유번호: 검출된 객체가 포함된 필지의 고유번호
   + 법정동명: 검출된 객체가 포함된 필지의 법정동명
   + 검출된 물체 번호: 모델에 의해 예측된 라벨 번호
   + 지목코드: 검출된 객체가 포함된 지목의 코드
   + 지목명: 검출된 객체가 포함된 지목의 이름
   + Reason: 검출된 객체가 불법인 이유

---

## 라이센스

MIT ([LICENCE파일](https://github.com/tjdeo1102/JBNU_Capstone-2023/blob/main/LICENSE) 참고)

---

## 버그 리포트

[Issues](https://github.com/tjdeo1102/JBNU_Capstone-2023/issues)를 이용해주세요.
