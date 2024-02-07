import random
import csv
"""
def shuffle_range(start, end):
    numbers = list(range(start, end + 1))
    random.shuffle(numbers)
    return numbers

start = int(input("시작 정수를 입력하세요: "))
end = int(input("끝 정수를 입력하세요: "))

shuffled_numbers = shuffle_range(start, end)
for num in shuffled_numbers:
    print(num)
"""
def main():
    # 좌석배치 완료된 파일에서 정보 입력
    student = []
    result = []
    file_path = ".\\output\\seat_result.csv"
    with open(file_path, mode='rt',encoding='UTF-8', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # 첫 번째 행을 건너뜁니다
        for row in csvreader:
            student.append(row)
    random.shuffle(student) #학생 순서 랜덤으로 섞기 -> 섞인 순서를 기준으로 앞에부터 사물함 배정



    bg = 53 #법오 골방 : 53~64
    bkp = 65 # 법오 큰방 평상 : 65~96
    bkk = 97 # 법오 큰방 칸막이 : 97~348
    bj = 1 # 법오 작은방 1~52
    fo = 1 # 401호 - 404(A) 1~66
    ff = 1 # 404호 - 404(B) 1~150
    sa = 1 # 서암 - 1~80
    gs = 81 # 국산 - 81~162

    for std in student : # 법오 큰방(골방) - 법오 큰방 53~64

        if std[2]=='법오 골방(칸막이)':
            drawer = ['법오 큰방',bg]
            bg +=1 
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='법오 큰방(평상)':
            drawer = ['법오 큰방',bkp]
            bkp+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='법오 큰방(칸막이)':
            drawer = ['법오 큰방',bkk]
            bkk+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='법오 작은방(평상)':
            drawer = ['법오 작은방',bj]
            bj+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='15동 401호(칸막이)':
            drawer = ['404(A)',fo]
            fo+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='15동 404호(칸막이)':
            drawer = ['404(B)',ff]
            ff+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)
        elif std[2]=='서암(평상)':
            drawer = ['서암',sa]
            sa+=1
            std_drawer=std+drawer
            #print(std_drawer)
            result.append(std_drawer)     
        elif std[2]=='국산(칸막이)':
            drawer = ['국산',gs]
            gs+=1
            std_drawer=std+drawer
            result.append(std_drawer)

    #초과 확인
    if bg > 65 : 
        print("[-]골방 사물함 넘버 초과")   
    if bkp > 97 : 
        print("[-]큰방 평상 사물함 넘버 초과")                 
    if bkk > 349 : 
        print("[-]큰방 칸막이 사물함 넘버 초과") 
    if bj > 53 : 
        print("[-]작은방 사물함 넘버 초과") 
    if fo > 67 : 
        print("[-]401 사물함 넘버 초과") 
    if ff > 151 : 
        print("[-]404 사물함 넘버 초과") 
    if sa > 81 : 
        print("[-]서암 사물함 넘버 초과") 
    if gs > 163 : 
        print("[-]국산 사물함 넘버 초과") 
    if len(result) != len(student):
        print("[-]전체 숫자 안 맞음. 데이터 오타 확인할 것")

    #결과 출력
    with open('.\\output\\seat_drawer_result.csv', mode='wt',encoding='utf-8') as file:
        #file.write("이름,열람실,좌석번호,사물함,사물함번호,학번뒤2자리\n")
        file.write("이름,학번뒤2자리,열람실,좌석번호,사물함,사물함번호\n")

        for r in result : 
            file.write(r[0]+","+r[1]+","+r[2]+","+r[3]+","+r[4]+","+str(r[5])+"\n")
    print('[+]Done. check .\\output\\seat_drawer_result.csv')

    
if __name__=="__main__":
    main()