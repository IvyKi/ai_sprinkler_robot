import numpy as np
import pandas as pd

fold_dir = "C:\\Users\\hihi5\\Downloads\\소방청_서울시 읍면동 단위 화재 발생 현황_20231012.csv"
data = pd.read_csv(fold_dir, encoding='cp949', skiprows=1, header=None)
# numpy 배열로 변환
data = data.to_numpy()

def sobang(data):
    # 파일 경로

    # numpy 배열 출력
    real_data = data[:, 20:22]  # 온습도 데이를 따로 저장
    temp_data = real_data[:, 0]  # 온도데이터를 받은 변수
    humi_data = real_data[:, 1]  # 습도데이터 받은 변수
    temp_size = len(humi_data)
    humi_size = len(humi_data)

    # print(temp_data[1])
    total_temp = 0;
    total_humi = 0;
    # 온도총합
    for i in range(0, temp_size, 1):
        if not np.isnan(temp_data[i]):
            total_temp += temp_data[i]
    # 습도총함
    for i in range(0, humi_size, 1):
        total_humi = total_humi + humi_data[i]
    average_temp = total_temp / temp_size
    average_humi = total_humi / humi_size
    average_temp = round(average_temp, 3)  # 온도평균을 소수점3자리까지표현
    average_humi = round(average_humi, 3)  # 습도평균을 소수점3자리까지표현

    return total_humi, total_temp, average_temp, average_humi#총합온도 및 습도 값 확인해보려고 return포함시킴


total_humi, total_temp, average_temp, average_humi = sobang(data)
