import csv
from collections import defaultdict


def run():
    try:
        # --- 1. 데이터 로드 ---
        # input.csv 파일 로드
        with open('input/input_data.csv', mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            next(reader)  # 헤더 행 읽기

            # 긴 컬럼명 대신 사용할 새로운 컬럼명 지정
            clean_headers = ['타임스탬프', '이메일', '성명', '학번', '학년', '1지망', '2지망', '3지망']

            # 데이터를 딕셔너리 리스트로 변환
            applicants_data = []
            for row in reader:
                # 일부 행의 컬럼 수가 부족할 경우를 대비하여 슬라이싱
                applicants_data.append(dict(zip(clean_headers, row[:len(clean_headers)])))

        # seat_result.csv 파일 로드
        with open('output/seat_result.csv', mode='r', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            results_data = [dict(zip(['성명', '학번뒤2자리', '열람실', '좌석번호'], row)) for row in reader]

        students_2nd = []
        students_3rd = []
        students_grad = []
        for student in applicants_data:
            if student.get('학년') in ['1학년', '2학년']:
                students_2nd.append(student)
            elif student.get('학년') in ['3학년', '수료생']:
                students_3rd.append(student)
            elif student.get('학년') in ['졸업생']:
                students_grad.append(student)

        # --- 3. 당첨자 정보 결합 (Merge) ---
        results_lookup = {result['성명'] + result['학번뒤2자리']: result['열람실'] for result in results_data}

        merged_winners_2nd = []
        merged_winners_3rd = []
        merged_winners_grad = []

        for applicant in students_2nd:
            applicant_name = applicant.get('성명') + applicant.get('학번')[-2:]
            if applicant_name in results_lookup:
                # 당첨된 경우, 신청 정보에 배정된 열람실 정보 추가
                winner_info = applicant.copy()
                winner_info['배정된 열람실'] = results_lookup[applicant_name]
                merged_winners_2nd.append(winner_info)

        for applicant in students_3rd:
            applicant_name = applicant.get('성명') + applicant.get('학번')[-2:]
            if applicant_name in results_lookup:
                # 당첨된 경우, 신청 정보에 배정된 열람실 정보 추가
                winner_info = applicant.copy()
                winner_info['배정된 열람실'] = results_lookup[applicant_name]
                merged_winners_3rd.append(winner_info)

        for applicant in students_grad:
            applicant_name = applicant.get('성명') + applicant.get('학번')[-2:]
            if applicant_name in results_lookup:
                # 당첨된 경우, 신청 정보에 배정된 열람실 정보 추가
                winner_info = applicant.copy()
                winner_info['배정된 열람실'] = results_lookup[applicant_name]
                merged_winners_grad.append(winner_info)

        # --- 4. 통계 계산 ---
        # 전체 열람실 목록 추출
        all_rooms_2nd = set()
        for student in students_2nd:
            all_rooms_2nd.add(student['1지망'])
            all_rooms_2nd.add(student['2지망'])
            all_rooms_2nd.add(student['3지망'])
        for result in results_data:
            all_rooms_2nd.add(result['열람실'])
        all_rooms_2nd.discard(None)  # None 값 제거

        all_rooms_3rd = set()
        for student in students_3rd:
            all_rooms_3rd.add(student['1지망'])
            all_rooms_3rd.add(student['2지망'])
            all_rooms_3rd.add(student['3지망'])
        for result in results_data:
            all_rooms_3rd.add(result['열람실'])
        all_rooms_3rd.discard(None)  # None 값 제거

        all_rooms_grad = set()
        for student in students_grad:
            all_rooms_grad.add(student['1지망'])
            all_rooms_grad.add(student['2지망'])
            all_rooms_grad.add(student['3지망'])
        for result in results_data:
            all_rooms_grad.add(result['열람실'])
        all_rooms_grad.discard(None)  # None 값 제거

        # 통계 저장을 위한 딕셔너리 초기화
        stats = {room + "_2": defaultdict(int) for room in all_rooms_2nd}
        stats.update({room + "_3": defaultdict(int) for room in all_rooms_3rd})
        stats.update({room + "_g": defaultdict(int) for room in all_rooms_grad})

        # 1지망 지원자 수 계산
        for student in students_2nd:
            key = student['1지망'] + "_2"
            if key in stats:
                stats[key]['1지망 지원자 수'] += 1

        # 1지망 지원자 수 계산
        for student in students_3rd:
            key = student['1지망'] + "_3"
            if key in stats:
                stats[key]['1지망 지원자 수'] += 1

        # 1지망 지원자 수 계산
        for student in students_grad:
            key = student['1지망'] + "_g"
            if key in stats:
                stats[key]['1지망 지원자 수'] += 1

        # 당첨자 통계 계산
        for winner in merged_winners_2nd:
            assigned_room = winner['배정된 열람실']
            key = assigned_room + "_2"

            if key not in stats: continue

            if winner['1지망'] == assigned_room:
                stats[key]['1지망 당첨자 수'] += 1
            elif winner['2지망'] == assigned_room:
                stats[key]['2지망 당첨자 수'] += 1
            elif winner['3지망'] == assigned_room:
                stats[key]['3지망 당첨자 수'] += 1
            else:
                stats[key]['지망X 당첨자 수'] += 1

        for winner in merged_winners_3rd:
            assigned_room = winner['배정된 열람실']
            key = assigned_room + "_3"

            if key not in stats: continue

            if winner['1지망'] == assigned_room:
                stats[key]['1지망 당첨자 수'] += 1
            elif winner['2지망'] == assigned_room:
                stats[key]['2지망 당첨자 수'] += 1
            elif winner['3지망'] == assigned_room:
                stats[key]['3지망 당첨자 수'] += 1
            else:
                stats[key]['지망X 당첨자 수'] += 1

        for winner in merged_winners_grad:
            assigned_room = winner['배정된 열람실']
            key = assigned_room + "_g"

            if key not in stats: continue

            if winner['1지망'] == assigned_room:
                stats[key]['1지망 당첨자 수'] += 1
            elif winner['2지망'] == assigned_room:
                stats[key]['2지망 당첨자 수'] += 1
            elif winner['3지망'] == assigned_room:
                stats[key]['3지망 당첨자 수'] += 1
            else:
                stats[key]['지망X 당첨자 수'] += 1

        # --- 5. 결과 출력 ---
        print("--- 열람실 신청 및 배정 결과 통계 ---")
        # 열람실 이름으로 정렬하여 출력
        for room in sorted(stats.keys()):
            data = stats[room]
            # 1지망 탈락자가 있으나 다른 당첨자가 있는 경우에만 출력
            # 3학년, 졸업생은 할당 좌석 1,2,3지망에 모두 떨어지더라도 다른 학년 좌석에서 1지망에 당첨될 수 있음
            if sum(data.values()) > 0 and data['1지망 지원자 수'] > data['1지망 당첨자 수'] and (
                    data['2지망 당첨자 수'] > 0 or data['3지망 당첨자 수'] > 0 or data['지망X 당첨자 수'] > 0):
                print(f"\n[ {room} ]")
                print("  - 1지망 지원자 / 1지망 당첨자 / 2지망 당첨자 / 3지망 당첨자 / 지망X 당첨자: " +
                      f"{data['1지망 지원자 수']} /  {data['1지망 당첨자 수']} /  {data['2지망 당첨자 수']} / "+
                      f"{data['3지망 당첨자 수']} / {data['지망X 당첨자 수']}")

    except FileNotFoundError as e:
        print(f"오류: '{e.filename}' 파일을 찾을 수 없습니다. 스크립트와 같은 폴더에 있는지 확인해주세요.")
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}")


def main():
    run()


if __name__ == "__main__":
    run()
