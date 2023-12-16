# 2023-2 전북대학교 SW 캡스톤디자인 2023
---

해당 프로젝트는 LX 한국국토정보공사 x 온새미로팀과 함께 진행된 프로젝트로 하천부근 불법 점용 객체를 탐지하는 소프트웨어입니다.

소프트웨어를 제작하기 위해 YOLOV8, QGIS, pytorch, opencv, shapely가 사용되었습니다.

소프트웨어는 총 2가지 트랙으로 구분되어 진행되며, 각 과정을 수행하기 위한 환경을 만들어야 합니다.

첫번째 트랙에서는 객체를 탐지하는 과정이 진행됩니다.

두번째 트랙에서는 탐지된 객체가 불법인지 판단해주는 과정이 진행됩니다.


## 설치
---

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
   
6. 사전에 드론맵을 준비해주세요(별도로 구해야됨)
   
7. 드론맵에 해당되는 지역의 행정데이터(토지소유정보)를 다음의 [링크](http://openapi.nsdi.go.kr/nsdi/index.do)를 통해 다운받습니다.
   

## 과정
---

### 첫번째 트랙
+ 1_YOLO폴더의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/blob/main/1_YOLO/README.md)를 참고해주세요.
   
---
### 두번째 트랙
+ 2_QGIS폴더의 [README.md](https://github.com/tjdeo1102/JBNU_Capstone-2023/tree/main/2_QGIS)를 참고해주세요.

## 팀
|성명|역할|
|:---:|:---:|
| 오주형 |   PM, AI모델 설계    |
| 소부승 | 데이터 전처리, AI모델 설계 |
| 김지성 |  자료 정리 , QGIS 개발  |
| 곽성대 | 데이터 후처리, QGIS 개발 |

## 라이센스
---

MIT (LICENCE파일 참고)


## 버그 리포트
---

Issues를 이용해주세요.
