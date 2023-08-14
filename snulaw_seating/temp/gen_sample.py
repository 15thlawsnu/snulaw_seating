import random

data = ['법오 골방(칸막이)','법오 큰방(평상)','법오 큰방(칸막이)','법오 작은방(평상)','15동 401호(칸막이)','15동 404호(칸막이)','서암(평상)','국산(칸막이)']
f = open('sample.csv',mode='wt',encoding='UTF-8', newline='')
for i in range(500):
    f.write(str(random.choice(data))+","+random.choice(data)+","+random.choice(data)+"\n")
f.close()