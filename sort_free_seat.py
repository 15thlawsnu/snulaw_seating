import csv
from collections import Counter
import pandas as pd

def sort_csv():
    filename = "free/free_seat.csv"  # 정렬할 CSV 파일 이름
    rows = []

    # CSV 읽기
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            rows.append((row[0], int(row[1])))

    # 정렬 (첫 번째 컬럼 → 두 번째 컬럼)
    rows.sort(key=lambda x: (x[0], x[1]))

    counter = Counter([row[0] for row in rows])
    print()
    print('남은 좌석 리스트')
    for key, cnt in counter.items():
        print(f"{key}: {cnt}")
    print()

    # CSV 덮어쓰기
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    # 동명의 XLSX 파일 생성
    df = pd.DataFrame(rows, columns=["열람실", "좌석번호"])
    xlsx_filename = filename.replace('.csv', '.xlsx')
    df.to_excel(xlsx_filename, index=False, engine='openpyxl')
    print(f"[+] {xlsx_filename} 생성 완료")

def main():
    sort_csv()

if __name__ == "__main__":
    main()
