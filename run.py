import seat
import drawer
import hashlib

if __name__=="__main__":
    #input_data.csv 해시값 출력
    print("[***]입력값 경로 : .\\input\\input_data.csv")
    f = open(".\\input\\input_data.csv",'rb')
    data = f.read()
    f.close()
    print("[***]입력값 해시(SHA256) : "+hashlib.sha256(data).hexdigest())
    #돌리기
    seat.main()
    drawer.main()
    #seat_drawer_result.csv 해시값 출력
    #input_data.csv 해시값 출력
    print("[***]출력값 경로 : .\\output\\seat_drawer_result.csv")
    f = open(".\\output\\seat_drawer_result.csv",'rb')
    data = f.read()
    f.close()
    print("[***]출력값 해시(SHA256) : "+hashlib.sha256(data).hexdigest())


    