import re


def main():
    stdnum, seatnum = 0, 0
    emails = set()
    ids = set()
    email_pattern = re.compile(r".+@snu\.ac\.kr$")  # @snu.ac.kr로 끝나야 함

    with open("./input/input_data.csv", encoding="utf-8-sig") as f_std:
        lines = f_std.readlines()

        # 첫 줄(header) 건너뛰기
        for line in lines[1:]:
            if len(line.strip()) == 0:
                break
            stdnum += 1
            vals = line.strip().split(",")
            email = vals[1]  # 이메일 값
            id = vals[3]  # 학번 값

            # 이메일 형식 검증
            # if not email_pattern.match(email):
            #     print(f"[!] 잘못된 이메일 형식: {email}")

            # 중복 체크
            if email in emails:
                print(f"[-] 중복 이메일 발생: {email}")
            else:
                emails.add(email)

            # 중복 체크
            if id in ids:
                print(f"[-] 중복 학번 발생: {id}")
            else:
                ids.add(id)

    with open("./input/seatlist.csv", 'rt', encoding='UTF8') as f_seat:
        for line in f_seat.readlines():
            if "open" in line:
                seatnum += 1

    print("[*]학생 수 및 좌석 수 체크")
    print("[*]학생 수:" + str(stdnum) + ", 좌석 수:" + str(seatnum))
    if stdnum > seatnum:
        print("[-]좌석 수 부족. 입력값 조정할 것!")


if __name__ == "__main__":
    main()
