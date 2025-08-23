# Requirement
 - python3 
  
# 구성
  ## run.py
   - 메인 파일. 2024 ver에서는 그냥 이 파일 실행하면 됨
  ## check_input.py
   - 좌석수와 학생수 체크. 비선호좌석 개수 조정하여 미리 배정대상 좌석 수와 학생 수 맞출 것.
  ## seat.py 
   - 설문 데이터를 csv 형태로 입력받아 (.\input\input_data.csv) 열람실 배치 결과 출력
   - 배치 결과 구성
     - [.\output\seat_result.csv](output/seat_result.csv) : 각 인원별 3지망까지 배치된 결과
     - [.\output\seat_unmatched_student.csv](output/seat_unmatched_student.csv) : 3지망까지 배치되지 않은 사람들 리스트 (2024 ver. 비어있는게 정상)
     - [.\output\seat_unmatched_seat.csv](output/seat_unmatched_seat.csv) : 잔여 여석 리스트
  ## drawer.py 
   - 열람실 최종 배정결과 리스트를 입력받아 ([.\output\seat_result.csv](output/seat_result.csv)) 각 열람실별 사물함 랜덤 배정
   - 배치 결과
     - [.\output\seat_drawer_result.csv](output/seat_drawer_result.csv) : 최종 결과로, 이전 배치결과 엑셀 시트와 동일한 구조
     - **주의** : UTF-8형태로, 그대로 엑셀에서 열면 한글이 깨질 수 있음. ansi 인코딩으로 바꾸거나, 엑셀에서 열 때 인코딩 변환할 것 (엑셀-> 데이터->데이터 가져오기->텍스트/CSV에서 -> 파일 선택-> 인코딩 UTF-8로 변환 후 로드)
  ## [.\input\seatlist.csv](input/seatlist.csv) 
    - 열람실 좌석 리스트. 좌석 구성에 변화가 생긴다면 이 파일을 수정할 것. 형식 변환 X
  ## [.\input\input_data.csv](input/input_data.csv)
    - 입력 파일 예시

# 사용 방법
## 2024 ver.
1. 입력받은 설문 시트 그대로 csv로 출력 후 .\input\input_data.csv에 저장.
2. ``python run.py``  실행
3. output 폴더에서 seat_drawer_result.csv 확인 및 검증
4. 입력값, 결과값 무결성 검증 위해 해시값 및 파일 백업 필요

## 이하는 2023 ver.
1. 입력받은 설문 시트 그대로 csv로 출력 후 .\input\input_data.csv에 저장. 
2. ``python seat.py``  실행
3. output 폴더에서 seat_unmatched_student.csv와 seat_unmatched_seat.csv 확인하여 미반영된 사람들 수동 배치하여 seat_result.csv에 업데이트
4. output 폴더의 seat_result.csv를 input 폴더로 복사
5. ``python drawer.py`` 실행
6. 엑셀에서 ``.\output\seat_drawer_result.csv`` 불러와서 결과 확인



# 자유좌석 배정 (2025-2 신규 추가)
## 사전 준비
1. run.py를 실행하면 자동으로 열려 있는 좌석 정보가 free_seat.csv에 저장됩니다.
2. sort_free_seat.py를 실행하면 free_seat.csv가 정렬되고, 동시에 .xlsx 파일도 생성됩니다.

## 배정 예시 (8월 24일 기준)
1. Google Form 응답 기록을 CSV로 다운로드하여 free/input_data_free.csv로 교체.
2. 8월 24일 23:59까지 올라온 댓글을 모두 반영한 배치 결과 .xlsx 파일을 free/seat_drawer_result.xlsx로 교체.
3. free_seat_allocation.py의 TODAY를 '2025. 8. 24'로 수정
4. free_seat_allocation.py 실행.
5. 배정 결과 및 배치 결과 파일에 변경 사항이 반영됨.
6. 생성된 free_seat.csv와 free_seat_allocation_YYYY_M_D.csv 파일은 게시글 댓글로 공유.

## 참고사항
1. free_seat.csv와 seat_drawer_result.xlsx에 중복 좌석이 있으면 오류를 발생시키고 실행이 중단됩니다. 재실행 전 각 파일을 확인해주세요.
2. 신청자의 학번 뒷 두 자리가 05 또는 5처럼 입력되어도 정상 매칭됩니다. 이외의 잘못된 데이터는 모두 무시합니다.
3. 난수(seed)는 오늘 날짜 기준으로 고정되어 재실행 시에도 동일한 결과를 재현 가능.