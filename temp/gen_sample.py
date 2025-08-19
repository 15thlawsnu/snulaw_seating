import random
import os

data = [
    '법오 골방(칸막이)',
    '법오 큰방(평상)',
    '법오 큰방(칸막이)',
    '법오 작은방(평상)',
    '15동 401호(평상)',
    '15동 401호(칸막이)',
    '15동 404호(칸막이)',
    '국산(칸막이)',
    '역사관(평상)',
]

# 현재 실행 파일(.py) 위치
script_dir = os.path.dirname(os.path.abspath(__file__))

# sample.csv 경로 생성
file_path = os.path.join(script_dir, 'sample.csv')

with open(file_path, mode='wt', encoding='UTF-8', newline='') as f:
    for i in range(500):
        values = random.sample(data, 3)
        f.write(",".join(values) + "\n")
