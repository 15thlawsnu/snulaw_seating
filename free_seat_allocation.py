import csv
import random
import sort_free_seat
from datetime import datetime
import pandas as pd

def convert_winner_xlsx_to_csv(xlsx_file, csv_file):
    df = pd.read_excel(xlsx_file, engine='openpyxl')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')

# ==========================
# [상수] 오늘 날짜
# ==========================
TODAY = '2025. 8. 23'   # 반드시 2025. 1. 1 형태

# 랜덤 시드 고정 (YYYYMMDD 숫자로 변환)
seed_str = TODAY.replace(' ', '').replace('.', '')  # '2025. 8. 23' → '2025823'
random.seed(int(seed_str))

# ==========================
# 파일 경로
# ==========================
INPUT_FREE = './free/input_data_free.csv'
FREE_SEAT_FILE = './free/free_seat.csv'
WINNER_FILE_XLSX = './free/seat_drawer_result.xlsx'
WINNER_FILE_CSV = './free/seat_drawer_result.csv'

# XLSX → CSV 변환 (1회용)
convert_winner_xlsx_to_csv(WINNER_FILE_XLSX, WINNER_FILE_CSV)

# 이후 기존 CSV 함수 그대로 사용
WINNER_FILE = WINNER_FILE_CSV

OUTPUT_FREE_ALLOC = f'./free/free_seat_allocation_{TODAY.replace(" ", "").replace(".", "_")}.csv'
OUTPUT_FREE_SEAT = './free/free_seat.csv'
OUTPUT_RESULT = './free/seat_drawer_result.csv'

# ==========================
# CSV 읽기 함수
# ==========================
def read_winner_csv(filename):
    """당첨 내역 읽기"""
    winner = {}
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['이름'], row['학번뒤2자리'])
            winner[key] = row  # 좌석 등 정보 그대로
    return winner

def read_free_seat(filename):
    """머리말 없는 free seat csv 읽기"""
    seats = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            seats.append([row[0], int(row[1])])
    return seats

def read_input_data_free(filename, winner_dict):
    """신청 내역 읽기. 오늘 날짜만, 당첨자만, 응답 시간도 오늘 기준"""
    data = {}
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        headers = next(reader)  # 첫행 무시
        for row in reader:
            if len(row) < 8:
                continue
            timestamp = row[0].strip()
            email = row[1].strip()  # 무시
            apply_date = row[2].strip()
            name = row[3].strip()
            stdid = row[4].strip()
            seat_room = row[5].strip()
            pref1 = row[6].strip()
            pref2 = row[7].strip() if len(row) > 8 else ''
            pref3 = row[8].strip() if len(row) > 9 else ''

            # 오늘 날짜 필터
            if TODAY not in apply_date or TODAY not in timestamp:
                continue

            # 당첨 내역 존재 여부 (학번 뒤 2자리 int로 통일)
            try:
                stdid_int = int(stdid)  # "05" → 5
            except ValueError:
                continue  # 숫자가 아니면 무시

            # winner_dict 키도 학번 int로 통일
            winner_dict_int = {(k[0], int(k[1])): v for k, v in winner_dict.items()}

            key = (name, stdid_int)
            if key not in winner_dict_int:
                continue
            # 당첨 좌석과 일치 여부
            if winner_dict_int[key]['열람실'] != seat_room:
                continue

            # 같은 이름+학번 중 최신 timestamp만 저장
            timestamp_clean = timestamp.replace('오전', 'AM').replace('오후', 'PM')
            ts_obj = datetime.strptime(timestamp_clean, '%Y. %m. %d %p %I:%M:%S')
            if key not in data or ts_obj > data[key]['_ts']:
                data[key] = {
                    'name': name,
                    'stdid': stdid_int,
                    'seat_room': seat_room,
                    'pref': [pref1, pref2, pref3],
                    '_ts': ts_obj,
                    'original_seat': winner_dict_int[key]['좌석번호']
                }
    return data


# ==========================
# free seat 검증
# ==========================
def validate_free_seat_vs_winner(free_seat, winner_dict):
    """
    free_seat에 있는 좌석이 winner_dict에 이미 사용 중인지 검증.
    발견 시 에러 발생.
    """
    conflict_list = []
    winner_seats = {(v['열람실'], int(v['좌석번호'])) for v in winner_dict.values()}
    for room, seat in free_seat:
        if (room, seat) in winner_seats:
            conflict_list.append(f"{room} {seat}")
    if conflict_list:
        raise ValueError(f"[ERROR] free_seat.csv에 이미 당첨된 좌석이 존재합니다: {conflict_list}")


# ==========================
# 유효한 free seat만 남기기
# ==========================
def validate_preferences(input_data, free_seat):
    free_dict = {f"{s[0]}_{s[1]}": True for s in free_seat}
    for k, v in input_data.items():
        new_pref = []
        for p in v['pref']:
            if p.isdigit() and f"{v['seat_room']}_{int(p)}" in free_dict:
                new_pref.append(int(p))
            else:
                new_pref.append(None)
        v['pref'] = new_pref

# ==========================
# 1~3지망 배정
# ==========================
def allocate_preferences(input_data, free_seat):
    """
    한 지망씩 순회하며 남은 신청자만 배정.
    배정 성공 시, 원래 좌석은 new_free_seat로 추가.
    """
    free_pool = {(s[0], s[1]): True for s in free_seat}  # 현재 free seat pool
    allocation_result = []
    final_free_seat = []
    allocated_keys = set()  # 배정 완료 학생 키

    for pref_idx in range(3):
        keys = [k for k in input_data.keys() if k not in allocated_keys]
        random.shuffle(keys)
        for key in keys:
            seat_room = input_data[key]['seat_room']
            pref = input_data[key]['pref'][pref_idx]
            if pref is None:
                continue
            seat_key = (seat_room, pref)
            if free_pool.get(seat_key, False):
                print(f"[+] {input_data[key]['name']}({input_data[key]['stdid']}) 배정: {pref_idx+1}지망 {input_data[key]['seat_room']} {input_data[key]['original_seat']} -> {pref}")
                # 배정 결과 기록
                allocation_result.append({
                    'name': input_data[key]['name'],
                    'stdid': input_data[key]['stdid'],
                    'seat_room': input_data[key]['seat_room'],
                    'prev_seat': input_data[key]['original_seat'],
                    'new_seat': pref
                })
                # free pool 업데이트
                free_pool[seat_key] = False
                # 원래 자리 new_free_seat에 추가 (배정 후 생긴 자유좌석)
                final_free_seat.append([seat_room, int(input_data[key]['original_seat'])])
                # 학생 데이터 업데이트
                input_data[key]['original_seat'] = pref
                allocated_keys.add(key)  # 이후 지망 순회에서 제외
                # pref 값 초기화
                input_data[key]['pref'][pref_idx] = None

    # 최종 free seat 리스트: pool 중 남은 것 + 배정으로 생긴 좌석
    for key, avail in free_pool.items():
        if avail:
            final_free_seat.append([key[0], key[1]])
    return allocation_result, final_free_seat


# ==========================
# 최종 CSV 출력
# ==========================
def save_allocation_csv(result, filename):
    # 공통 헤더 정의
    headers = ['성명', '학번뒤2자리', '열람실', '변경전좌석', '변경후좌석']

    # CSV 저장
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in result:
            writer.writerow([
                r['name'],
                r['stdid'],
                r['seat_room'],
                r['prev_seat'],
                r['new_seat']
            ])

    # XLSX 저장 (빈 데이터도 헤더 유지)
    rows = [
        [r['name'], r['stdid'], r['seat_room'], r['prev_seat'], r['new_seat']]
        for r in result
    ]
    df = pd.DataFrame(rows, columns=headers)
    xlsx_filename = filename.replace('.csv', '.xlsx')
    df.to_excel(xlsx_filename, index=False, engine='openpyxl')

    print(f"[+] {xlsx_filename} 생성 완료")
def update_free_seat_csv(free_seat_list, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for s in free_seat_list:
            writer.writerow([s[0], s[1]])

def update_winner_seat_csv(input_data, winner_dict, filename):
    """좌석만 최신 배정 값으로 업데이트"""
    rows = []
    with open(WINNER_FILE, 'r', encoding='utf-8-sig') as f:
        reader = list(csv.DictReader(f))
        for row in reader:
            key = (row['이름'], row['학번뒤2자리'])
            if key in input_data:
                row['좌석번호'] = str(input_data[key]['original_seat'])
            rows.append(row)

    # 원래 순서 유지
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=reader[0].keys())
        writer.writeheader()
        writer.writerows(rows)


# ==========================
# main
# ==========================
def main():
    winner_dict = read_winner_csv(WINNER_FILE)
    free_seat = read_free_seat(FREE_SEAT_FILE)

    validate_free_seat_vs_winner(free_seat, winner_dict)

    input_data = read_input_data_free(INPUT_FREE, winner_dict)
    print(f"[*] 신청 데이터: {len(input_data)} 명")

    validate_preferences(input_data, free_seat)
    allocation_result, new_free_seat = allocate_preferences(input_data, free_seat)

    print(f"[*] 배정 완료: {len(allocation_result)} 명")

    # 결과 저장
    save_allocation_csv(allocation_result, OUTPUT_FREE_ALLOC)
    update_free_seat_csv(new_free_seat, OUTPUT_FREE_SEAT)
    update_winner_seat_csv(input_data, winner_dict, OUTPUT_RESULT)
    print("[+] 모든 CSV 업데이트 완료")

if __name__ == "__main__":
    main()
    sort_free_seat.main()
