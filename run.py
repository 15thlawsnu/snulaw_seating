import hashlib

import check_input
import drawer
import seat
import test

if __name__ == "__main__":
    # input_data.csv 해시값 출력
    print("[***]입력값 경로 : ./input/input_data.csv")
    with open("./input/input_data.csv", "rb") as f:
        data = f.read()
    print("[***]입력값 해시(SHA256) : " + hashlib.sha256(data).hexdigest())

    # 입력 데이터 검증
    check_input.main()

    # 좌석 및 사물함 배정
    seat.main()
    drawer.main()

    # 불변 검증용 input_data.csv 해시값 출력
    print("[***]입력값 경로 : ./input/input_data.csv")
    with open("./input/input_data.csv", "rb") as f:
        data = f.read()
    print("[***]입력값 해시(SHA256) : " + hashlib.sha256(data).hexdigest())

    # seat_drawer_result.csv 해시값 출력
    print("[***]출력값 경로 : ./output/seat_drawer_result.csv")
    with open("./output/seat_drawer_result.csv", "rb") as f:
        data = f.read()
    print("[***]출력값 해시(SHA256) : " + hashlib.sha256(data).hexdigest())

    # test.main()
