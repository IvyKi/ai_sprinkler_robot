# Ai를 활용한 산불방지 스프링쿨러 로봇시스템(이하 스프링쿨러)
- 2024년 한국공학대학교 임베디드 경진대회 본선 출품작
- 개발기간: 2024.07.09 ~


## 프로젝트 개요
- 본 프로젝트는 산의 환경정보를 수집하고, 화재 발생 조건을 충족할 시 스프링쿨러를 작동시켜 화재 발생 가능성을 줄여 화재예방에 기여하는 시스템을 제공하는 서비스입니다.
- 스프링쿨러는 Raspberry Pi 4 board에 python 파일을 탑재하여 구동하고, supabase를 이용한 서버리스 아키텍쳐를 활용하고 있습니다.


## 기능 개발 요구사항
- 본 프로젝트 팀이 개발하고자 하는 기능 사항은 다음과 같습니다.
1. 검증된 과거 데이터를 분석하여 화재 발생율이 높았던 specific point 산출. Raspberry Pi 4 board, Temperature and Humidity Sensor 를 통해 current data 수집. 비교 알고리즘 작성.
2. point와 current 가 동일한 시점에 스프링쿨러 동작 프로토콜 실행.
   2.1. 무선 통신으로 연결된 안드로이드 어플리케이션에 Notification Trigger
3. 로봇시스템 탑재 -> 모터제어
  3.1. 장애물 감지(OpenCV)
   3.2. 좌표 설정 및 스프링쿨러 조준 발사


### AUTHORS
- 기나혜(Ki nahye): Softwware developing, Project Manager | kinahae0331@tukorea.ac.kr
- 김하연(Kim HaYeon) : | khy0228@tukorea.ac.kr
