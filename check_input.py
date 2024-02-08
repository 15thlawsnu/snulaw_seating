import csv
import random

def main():
    f_std = open(".\\input\\input_data.csv",'rt', encoding='UTF8')
    stdnum = -1
    for line in f_std.readlines():
        if len(line)>1 :
            stdnum += 1
    f_seat = open(".\\input\\seatlist.csv",'rt', encoding='UTF8')
    seatnum = 0
    for line in f_seat.readlines():
        if "open" in line:
            seatnum += 1
    print("[*]학생 수 및 좌석 수 체크")
    print("[*]학생 수:" + str(stdnum) + ", 좌석 수:" +str(seatnum))
    if stdnum > seatnum : 
        print("[-]좌석 수 부족. 입력값 조정할 것!")    
    


if __name__=="__main__":
    main()