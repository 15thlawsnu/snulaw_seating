import csv
import random

## [2024.8.] 남는좌석 배치시 학년별 좌석에 우선적으로 배치. 2024-1 민원사항 반영.
STD_TYPE_TO_SEAT_TYPE = {
    '3학년': '3학년',
    '수료생': '3학년',
    '졸업생': '졸업생',
    '1학년': '2학년',
    '2학년': '2학년'
}

## [2025.8.] 남는 좌석 배치시 노트북 허용 열람실에 우선적으로 배치
LAPTOP_NOT_ALLOWED_ZONES = [
    '15동 401호(평상)',
    '15동 401호(칸막이)',
]

def get_preferred_seat_type(std_type):
    """
    우선적으로 배정되어야 할 좌석 타입 반환 ('1학년' -> '2학년', '2학년' -> '2학년', '3학년' -> '3학년')
    dict에 없는 경우 std_type 그대로 반환
    """
    return STD_TYPE_TO_SEAT_TYPE.get(std_type, std_type)


def csv_to_dict_std(filename):
    # '김학생_2020-20000': ['1학년', '법오 큰방(칸막이)', '국산(칸막이)', '15동 404호(칸막이)']
    with open(filename, mode='rt', encoding='UTF-8') as file:
        reader = csv.reader(file)
        next(reader)
        result = {}
        for row in reader:
            row.pop(0)  # 타임스탬프
            row.pop(0)  # 이메일 주소
            key = row.pop(0) + "_" + row.pop(0)
            if len(key) > 1:
                result[key] = row
    return result


def csv_to_list_seat(filename):  # ['3학년', '15동 401호(칸막이)', '38', 'open']
    with open(filename, mode='rt', encoding='UTF-8') as file:
        reader = csv.reader(file)
        next(reader)
        result = []
        for row in reader:
            if len(row) > 1:
                result.append(row)
    return result


def std_alloc(student, seatlist, std_types, seat_types):
    """
    학생들을 좌석에 배치하는 함수
    student: {학생이름: [학년, 1지망, 2지망, 3지망, ...]}
    seatlist: [[배정 대상 학년, 열람실, 번호, 상태], ...]
    std_types: 배정 대상 학년 리스트 (예: ['3학년', '수료생', '졸업생']), 비어있으면 전체 학생 대상
    seat_types: 배정 가능한 좌석 종류 리스트 (예: ['3학년']), 비어있으면 전체 좌석 대상
    """

    result = {}  # 최종 배치 결과

    # 좌석 배정 대상이 되는 학년 학생 선별(비어있는 경우 전체 학생 대상)
    if std_types:
        curr_students = {k: v for k, v in student.items() if v[0] in std_types}
    else:
        curr_students = student.copy()

    def alloc_pref(pref_idx):
        """
        한 지망(pref_idx)에 대해 배치 처리
        pref_idx: 학생 preference index (1: 1지망, 2: 2지망, 3: 3지망)
        """
        curr_students_pref = list(curr_students.keys())  # 배정 대상 학생 명단
        random.shuffle(curr_students_pref)  # 배정 순서 섞기

        for std_key in curr_students_pref:
            std_type = curr_students.get(std_key)[0]
            ## [2025.8.] 좌석 배정 시 이전 단계 잔여 좌석도 활용하되, 학년별 좌석에 우선적으로 배치하도록 로직 수정
            preferred_seat_type = get_preferred_seat_type(std_type)

            seatlist_preferred_tmp = []  # 지망 열람실 내 현재 우선 배정 가능 좌석 목록
            seatlist_tmp = []  # 지망 열람실 내 현재 우선X 배정 가능 좌석 목록
            for seat in seatlist:
                if seat_types and seat[0] not in seat_types:  # 좌석 타입 조건이 있으나 미충족 시 생략
                    continue
                if seat[1] == curr_students[std_key][pref_idx]:
                    if seat[0] == preferred_seat_type:
                        seatlist_preferred_tmp.append(seat)  # 우선 배정 가능 좌석
                    else:
                        seatlist_tmp.append(seat)

            # 조건에 맞는 좌석이 있으면 배정
            if seatlist_preferred_tmp:
                seat = random.choice(seatlist_preferred_tmp)
                result[std_key] = seat
                seatlist.remove(seat)  # 좌석 제거
                student.pop(std_key)  # 학생 제거
                curr_students.pop(std_key)  # 배정 대상에서 제거

            elif seatlist_tmp:
                seat = random.choice(seatlist_tmp)
                result[std_key] = seat
                seatlist.remove(seat)  # 좌석 제거
                student.pop(std_key)  # 학생 제거
                curr_students.pop(std_key)  # 배정 대상에서 제거

    # 1지망, 2지망, 3지망 순서대로 배치 처리
    for pref_idx in [1, 2, 3]:
        alloc_pref(pref_idx)

    return result


def std_alloc_unmatched(student, seatlist):
    """
    학생들을 좌석에 배치하는 함수
    student: {학생이름: [학년, 1지망, 2지망, 3지망, ...]}
    seatlist: [[배정 대상 학년, 열람실, 번호, 상태], ...]
    """

    result = {}  # 최종 배치 결과 저장
    curr_students = list(student.keys())  # 배정 대상 학생 명단
    random.shuffle(curr_students)  # 배정 순서 섞기

    ## [2025.8.] 남는 좌석 배치시 노트북 허용 열람실에 우선적으로 배치
    laptop_allowed_cnt = len([0 for seat in seatlist if seat[1] not in LAPTOP_NOT_ALLOWED_ZONES])

    ## [2024.8.] 남는 좌석 배치시 학년별 좌석에 우선적으로 배치. 2024-1 민원사항 반영.
    for std_key in curr_students:
        std_type = student[std_key][0]
        preferred_seat_type = get_preferred_seat_type(std_type)

        seatlist_tmp_std_type_matched = []      # 지망 열람실 내 현재 배정 가능 좌석 목록
        seatlist_tmp_std_type_unmatched = []    # 지망 열람실 내 현재 배정 가능 좌석 목록

        for seat in seatlist:
            ## [2025.8.] 남는 좌석 배치시 노트북 허용 열람실에 우선적으로 배치
            if laptop_allowed_cnt > 0 and seat[1] in LAPTOP_NOT_ALLOWED_ZONES:
                continue
            if seat[0] == preferred_seat_type:
                seatlist_tmp_std_type_matched.append(seat)
            else:
                seatlist_tmp_std_type_unmatched.append(seat)

        if laptop_allowed_cnt > 0:
            laptop_allowed_cnt -= 1

        if seatlist_tmp_std_type_matched:  # 좌석 타입 조건에 맞는 좌석이 있으면 배정
            seat = random.choice(seatlist_tmp_std_type_matched)
            result[std_key] = seat
            seatlist.remove(seat)  # 좌석 제거
            student.pop(std_key)  # 학생 제거

        elif seatlist_tmp_std_type_unmatched:  # 없는 경우 아무 자리나 배정
            seat = random.choice(seatlist_tmp_std_type_unmatched)
            result[std_key] = seat
            seatlist.remove(seat)  # 좌석 제거
            student.pop(std_key)  # 학생 제거

        elif seatlist:   # 혹시 몰라 넣어 두었으나, 걸릴 일 없음
            seat = random.choice(seatlist)
            result[std_key] = seat
            seatlist.remove(seat)  # 좌석 제거
            student.pop(std_key)  # 학생 제거

    return result


def std_3rd_alloc(student, seatlist):
    return std_alloc(student, seatlist, ['3학년', '수료생'], ['3학년'])


def std_grad_alloc(student, seatlist):
    ## [2025.8.] 좌석 배정 시 이전 단계 잔여 좌석도 활용하되, 학년별 좌석에 우선적으로 배치하도록 로직 수정
    return std_alloc(student, seatlist, ['3학년', '수료생', '졸업생'], ['3학년', '졸업생'])


def std_2nd_alloc(student, seatlist):
    ## [2025.8.] 좌석 배정 시 이전 단계 잔여 좌석도 활용하되, 학년별 좌석에 우선적으로 배치하도록 로직 수정
    return std_alloc(student, seatlist, [], ['3학년', '졸업생', '2학년'])


def main():
    # if __name__=="__main__":
    # def and input
    infile_std = './input/input_data.csv'
    infile_seat = './input/seatlist.csv'

    student_all = csv_to_dict_std(infile_std)
    seatlist_all = csv_to_list_seat(infile_seat)

    # 배정 가능 좌석 필터링
    seatlist_open, seatlist_closed = [], []
    for seat in seatlist_all:
        if seat[3] == 'open':
            seatlist_open.append(seat)
        else:
            seatlist_closed.append(seat)

    print("[*]전체 학생 수: " + str(len(student_all)))
    result_3rd = std_3rd_alloc(student_all, seatlist_open)
    result_grad = std_grad_alloc(student_all, seatlist_open)
    result_2nd = std_2nd_alloc(student_all, seatlist_open)
    result_unmatched = std_alloc_unmatched(student_all, seatlist_open)

    result_total = {}  # 최종 결과
    result_total.update(result_3rd)
    result_total.update(result_grad)
    result_total.update(result_2nd)
    result_total.update(result_unmatched)

    print("[*]배정된 학생 수: " + str(len(result_total)))
    print("[+]미배정된 학생 수: " + str(len(student_all)))

    # print(student_all)
    # print(seatlist_open)
    # print(seatlist_closed)

    # 결과 출력
    with open('./output/seat_result.csv', mode='wt', encoding='UTF-8') as file:
        file.write("이름,학번뒤2자리,열람실,좌석번호\n")
        for key, value in result_total.items():
            name = key.split("_")[0]
            id = key.split("_")[1][-2:]  # 가명처리 목적으로 뒷 2자리만
            room = value[1]
            roomid = value[2]
            file.write(name + "," + id + "," + room + "," + roomid + "\n")
    print("[+]배치결과 저장 경로: ./output/seat_result.csv")

    # 남은 학생 출력
    with open('./output/seat_unmatched_student.csv', mode='wt', encoding='UTF-8') as file:
        file.write("이름_학번,학년,1지망,2지망,3지망\n")
        for key, value in student_all.items():
            file.write(key + "," + value[0] + "," + value[1] + "," + value[2] + "," + value[3] + "\n")
    print("[+]남은 학생 리스트 저장 경로: ./output/seat_unmatched_student.csv")

    # 남은 좌석 출력
    with open('./output/seat_unmatched_seat.csv', mode='wt', encoding='UTF-8') as file:
        unmatched_seats = {}
        for i in seatlist_open:
            file.write(i[0] + "," + i[1] + "," + i[2] + "," + i[3] + "\n")
        #     key = i[0] + "_" + i[1]
        #     if key not in unmatched_seats:
        #         unmatched_seats[key] = 0
        #     unmatched_seats[key] += 1
        # print(unmatched_seats)
        for i in seatlist_closed:
            file.write(i[0] + "," + i[1] + "," + i[2] + "," + i[3] + "\n")
    print("[+]남은 좌석 리스트 저장 경로: ./output/seat_unmatched_seat.csv")

    # 추후 잔여 좌석 배치용 파일 출력
    with open('./free/free_seat.csv', mode='wt', encoding='UTF-8') as file:
        for i in seatlist_open:
            file.write(i[1] + "," + i[2] + "\n")
    print("[+]배정 가능 잔여 좌석 리스트 저장 경로: ./free/free_seat.csv")

if __name__ == "__main__":
    main()
