import csv
import random

def csv_to_dict_std(filename): 
    #'박성하_2020-22992': ['1학년', '법오 큰방(칸막이)', '국산(칸막이)', '15동 404호(칸막이)']
    with open(filename, mode='rt',encoding='UTF-8') as file:
        reader = csv.reader(file)
        next(reader)
        result = {}
        for row in reader:
            row.pop(0)
            key = row.pop(0) +"_"+ row.pop(0)
            if len(key) > 1 :
                result[key] = row
    return result
def csv_to_list_seat(filename): # ['3학년', '15동 401호(칸막이)', '38'], ['3학년', '15동 401호(칸막이)', '39']
    with open(filename, mode='rt',encoding='UTF-8') as file:
        reader = csv.reader(file)
        next(reader)
        result = []
        for row in reader:
            if len(row)>1:
                result.append(row)
    return result

def std_3rd_alloc(student, seatlist):
    student_3rd = {}
    seatlist_tmp = []
    result = {}
    for key, value in student.items() : 
        if value[0]=='3학년' or value[0]=='수료생' :
            student_3rd[key]=value
    student_3rd_1= student_3rd.copy() #1지망
    student_3rd_2= student_3rd.copy() #2지망
    student_3rd_3= student_3rd.copy() #3지망

    ## 1지망배치
    while len(student_3rd_1) > 0 :
        std_key = random.choice(list(student_3rd_1.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='3학년' and seat[3]=='open' and seat[1]==student_3rd_1[std_key][1]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_3rd_1.pop(std_key) #학생리스트 삭제
            student_3rd_2.pop(std_key) 
            student_3rd_3.pop(std_key) 
            student.pop(std_key)
        else : #1지망 없는 경우
            student_3rd_1.pop(std_key) #학생리스트 삭제
        seatlist_tmp = []#임시변수 초기화

    ## 2지망배치
    while len(student_3rd_2) > 0 :
        std_key = random.choice(list(student_3rd_2.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='3학년' and seat[3]=='open' and seat[1]==student_3rd_2[std_key][2]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_3rd_2.pop(std_key) #학생리스트 삭제
            student_3rd_3.pop(std_key) 
            student.pop(std_key)
        else : #2지망 없는 경우
            student_3rd_2.pop(std_key) #2지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화       

    ## 3지망배치
    while len(student_3rd_3) > 0 :
        std_key = random.choice(list(student_3rd_3.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='3학년' and seat[3]=='open' and seat[1]==student_3rd_3[std_key][3]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : # 해당 학생 조건에 맞는 좌석 리스트가 있다면
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_3rd_3.pop(std_key) #학생리스트 삭제
            student.pop(std_key)
        else : #3지망 없는 경우
            student_3rd_3.pop(std_key) #3지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화        
    return result

def std_grad_alloc(student,seatlist):
    student_grad = {}
    seatlist_tmp = []
    result = {}
    for key, value in student.items() : 
        if value[0]=='3학년' or value[0]=='수료생' or value[0]=='졸업생':
            student_grad[key]=value
    student_grad_1= student_grad.copy() #1지망
    student_grad_2= student_grad.copy() #2지망
    student_grad_3= student_grad.copy() #3지망

    ## 1지망배치
    while len(student_grad_1) > 0 :
        std_key = random.choice(list(student_grad_1.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='졸업생' and seat[3]=='open' and seat[1]==student_grad_1[std_key][1]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_grad_1.pop(std_key) #학생리스트 삭제
            student_grad_2.pop(std_key) 
            student_grad_3.pop(std_key) 
            student.pop(std_key)
        else : #1지망 없는 경우
            student_grad_1.pop(std_key) #학생리스트 삭제
        seatlist_tmp = []#임시변수 초기화

    ## 2지망배치
    while len(student_grad_2) > 0 :
        std_key = random.choice(list(student_grad_2.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='졸업생' and seat[3]=='open' and seat[1]==student_grad_2[std_key][2]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_grad_2.pop(std_key) #학생리스트 삭제
            student_grad_3.pop(std_key) 
            student.pop(std_key)
        else : #2지망 없는 경우
            student_grad_2.pop(std_key) #2지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화       

    ## 3지망배치
    while len(student_grad_3) > 0 :
        std_key = random.choice(list(student_grad_3.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='졸업생' and seat[3]=='open' and seat[1]==student_grad_3[std_key][3]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_grad_3.pop(std_key) #학생리스트 삭제
            student.pop(std_key)
        else : #3지망 없는 경우
            student_grad_3.pop(std_key) #3지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화        
    return result

def std_under_alloc(student,seatlist):
    #student_under = {}
    seatlist_tmp = []
    result = {}
    #for key, value in student.items() : 
    #    if value[0]=='3학년' or value[0]=='수료생' or value[0]=='졸업생':
    #        student_under[key]=value
    student_under_1= student.copy() #1지망
    student_under_2= student.copy() #2지망
    student_under_3= student.copy() #3지망

    ## 1지망배치
    while len(student_under_1) > 0 :
        std_key = random.choice(list(student_under_1.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='2학년' and seat[3]=='open' and seat[1]==student_under_1[std_key][1]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_under_1.pop(std_key) #학생리스트 삭제
            student_under_2.pop(std_key) 
            student_under_3.pop(std_key) 
            student.pop(std_key)
        else : #1지망 없는 경우
            student_under_1.pop(std_key) #학생리스트 삭제
        seatlist_tmp = []#임시변수 초기화

    ## 2지망배치
    while len(student_under_2) > 0 :
        std_key = random.choice(list(student_under_2.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='2학년' and seat[3]=='open' and seat[1]==student_under_2[std_key][2]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_under_2.pop(std_key) #학생리스트 삭제
            student_under_3.pop(std_key) 
            student.pop(std_key)
        else : #2지망 없는 경우
            student_under_2.pop(std_key) #2지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화       

    ## 3지망배치
    while len(student_under_3) > 0 :
        std_key = random.choice(list(student_under_3.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[0]=='2학년' and seat[3]=='open' and seat[1]==student_under_3[std_key][3]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_under_3.pop(std_key) #학생리스트 삭제
            student.pop(std_key)
        else : #3지망 없는 경우
            student_under_3.pop(std_key) #3지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화        
    return result        

def std_unmatched_alloc(student,seatlist): 
    # 남는 분들 학년 상관 없이 배치 
    ## [2024] 여기서 남는 분들 전부 배치하는 것으로 변경.
    ## [2024/8] 남는좌석 배치시 학년별 좌석에 우선적으로 배치. 2024-1 민원사항 반영. 
    seatlist_tmp = []
    seatlist_tmp2 = []
    result = {}
    student_unmatched_1= student.copy() #1지망
    student_unmatched_2= student.copy() #2지망
    student_unmatched_3= student.copy() #3지망
    student_unmatched_4= student.copy() #잔여
    

    ## 1지망배치
    while len(student_unmatched_1) > 0 :
        std_key = random.choice(list(student_unmatched_1.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[3]=='open' and seat[1]==student_unmatched_1[std_key][1]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_unmatched_1.pop(std_key) #학생리스트 삭제
            student_unmatched_2.pop(std_key) 
            student_unmatched_3.pop(std_key) 
            student_unmatched_4.pop(std_key) 
            student.pop(std_key)
        else : #1지망 없는 경우
            student_unmatched_1.pop(std_key) #학생리스트 삭제
        seatlist_tmp = []#임시변수 초기화

    ## 2지망배치
    while len(student_unmatched_2) > 0 :
        std_key = random.choice(list(student_unmatched_2.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[3]=='open' and seat[1]==student_unmatched_2[std_key][2]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_unmatched_2.pop(std_key) #학생리스트 삭제
            student_unmatched_3.pop(std_key) 
            student_unmatched_4.pop(std_key) 
            student.pop(std_key)
        else : #2지망 없는 경우
            student_unmatched_2.pop(std_key) #2지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화       

    ## 3지망배치
    while len(student_unmatched_3) > 0 :
        std_key = random.choice(list(student_unmatched_3.keys())) #1명 랜덤 선택

        for seat in seatlist : #1지망 조건 맞는 좌석 리스트
            if seat[3]=='open' and seat[1]==student_unmatched_3[std_key][3]:
                seatlist_tmp.append(seat)
        if len(seatlist_tmp) > 0 : 
            seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
            result[std_key]=seat #결과 반영
            seatlist.remove(seat) #좌석 전체리스트에서 삭제
            student_unmatched_3.pop(std_key) #학생리스트 삭제
            student_unmatched_4.pop(std_key)
            student.pop(std_key)
        else : #3지망 없는 경우
            student_unmatched_3.pop(std_key) #3지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화 

    ## 마지막까지 안 된 분들 배치
    ## [2024/8] 남는좌석 배치시 학년별 좌석에 우선적으로 배치. 2024-1 민원사항 반영. 
    while len(student_unmatched_4) > 0 :
        std_key = random.choice(list(student_unmatched_4.keys())) #1명 랜덤 선택

        #학생이 3학년, 수료생인 경우, 3학년 및 수료생 빈좌석에 우선 자리 배정
        if student_unmatched_4[std_key][0] == '3학년' or student_unmatched_4[std_key][0] == '수료생' :
            for seat in seatlist : #3학년 잔여 좌석 리스트 
                if seat[3]=='open' and (seat[0] == '3학년' or seat[0] == '수료생'):
                    seatlist_tmp.append(seat)
                elif seat[3]=='open': #잔여 2학년 좌석 리스트
                    seatlist_tmp2.append(seat)

            if len(seatlist_tmp) > 0 : #3학년 잔여 좌석이 있는 경우
                seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
                result[std_key]=seat #결과 반영
                seatlist.remove(seat) #좌석 전체리스트에서 삭제
                student_unmatched_4.pop(std_key)
                student.pop(std_key)
            elif len(seatlist_tmp2) > 0 : #1,2학년 잔여 좌석이 있는 경우
                seat = random.choice(seatlist_tmp2) #랜덤 좌석 배치
                result[std_key]=seat #결과 반영
                seatlist.remove(seat) #좌석 전체리스트에서 삭제
                student_unmatched_4.pop(std_key)
                student.pop(std_key)
            else : #잔여 좌석이 없는 경우 
                student_unmatched_4.pop(std_key) #3지망 학생리스트에서만 삭제
              
        # 1,2학년인 경우 1,2학년 빈좌석에 우선 자리 배정
        else : #학생 1,2학년
            for seat in seatlist : #2학년 잔여 좌석 리스트 
                if seat[3]=='open' and (seat[0] == '2학년'):
                    seatlist_tmp.append(seat)
                elif seat[3]=='open': #잔여 3학년 좌석 리스트
                    seatlist_tmp2.append(seat)
            if len(seatlist_tmp) > 0 : #1,2학년 잔여 좌석이 있는 경우
                seat = random.choice(seatlist_tmp) #랜덤 좌석 배치
                result[std_key]=seat #결과 반영
                seatlist.remove(seat) #좌석 전체리스트에서 삭제
                student_unmatched_4.pop(std_key)
                student.pop(std_key)
            elif len(seatlist_tmp2) > 0 : #3학년 잔여 좌석이 있는 경우
                seat = random.choice(seatlist_tmp2) #랜덤 좌석 배치
                result[std_key]=seat #결과 반영
                seatlist.remove(seat) #좌석 전체리스트에서 삭제
                student_unmatched_4.pop(std_key)
                student.pop(std_key)
            else : 
                student_unmatched_4.pop(std_key) #3지망 학생리스트에서만 삭제
        seatlist_tmp = []#임시변수 초기화   
        seatlist_tmp2 = []                
     
    return result   
    
def main():
#if __name__=="__main__":
    #def and input
    infile_std = '.\\input\\input_data.csv'
    infile_seat = '.\\input\\seatlist.csv'
    
    student_all = csv_to_dict_std(infile_std)
    seatlist_all = csv_to_list_seat(infile_seat)

    print("[*]전체 학생 수: " + str(len(student_all)))
    result_3rd = std_3rd_alloc(student_all,seatlist_all)
    result_grad = std_grad_alloc(student_all,seatlist_all)
    result_under = std_under_alloc(student_all,seatlist_all)
    result_unmatched = std_unmatched_alloc(student_all,seatlist_all)
    result_total = result_3rd.copy()
    result_total.update(result_grad)
    result_total.update(result_under)
    result_total.update(result_unmatched)    
    print("[*]배정된 학생 수: "+str(len(result_total)))
    print("[+]미배정된 학생 수: "+str(len(student_all)))
    #print(student_all)
    #print(seatlist_all)

    #결과 출력
    with open('.\\output\\seat_result.csv', mode='wt',encoding='UTF-8') as file:
        """
        file.write("이름,열람실,좌석번호,학번뒤2자리\n")
        for key, value in result_total.items() : 
            name = key.split("_")[0]
            id = key.split("_")[1][-2:] #가명처리로, 뒷 2자리만
            room = value[1]
            roomid = value[2]
            file.write(name+","+room+","+roomid+","+id+"\n")
        """
        file.write("이름,학번뒤2자리,열람실,좌석번호\n")
        for key, value in result_total.items() : 
            name = key.split("_")[0]
            id = key.split("_")[1][-2:] #가명처리로, 뒷 2자리만
            room = value[1]
            roomid = value[2]
            file.write(name+","+id+","+room+","+roomid+"\n")

    print("[+]배치결과 저장 경로: .\\output\\seat_result.csv")
    #남은 학생 출력
    with open('.\\output\\seat_unmatched_student.csv', mode='wt',encoding='UTF-8') as file:
        file.write("이름_학번,학년,1지망,2지망,3지망\n")
        for key, value in student_all.items() : 
            file.write(key+","+value[0]+","+value[1]+","+value[2]+","+value[3]+"\n")
    print("[+]남은 학생 리스트 저장 경로: .\\output\\seat_unmatched_student.csv")
    #남은 좌석 출력
    with open('.\\output\\seat_unmatched_seat.csv', mode='wt',encoding='UTF-8') as file:
        for i in seatlist_all:
            file.write(i[0]+","+i[1]+","+i[2]+","+i[3]+"\n")
    print("[+]남은 좌석 리스트 저장 경로: .\\output\\seat_unmatched_seat.csv")
    

if __name__=="__main__":
    main()