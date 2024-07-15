
monthly_data = [45, 56, 34, 78, 67, 89, 90, 34, 23, 49, 67, 32]  # 샘플데이터 1차원 리스트 (월별 데이터)
daily_data = [
    [3, 4, 5, 2, 6, 3, 8, 4, 6, 7, 8, 2],  # 1일
    [2, 3, 4, 5, 1, 7, 3, 4, 2, 6, 5, 4],  # 2일
    [5, 6, 2, 4, 3, 8, 6, 5, 4, 3, 7, 1],  # 3일
    [7, 8, 9, 3, 2, 4, 5, 6, 7, 4, 2, 3],  # 4일
    [6, 5, 4, 2, 3, 7, 5, 6, 4, 5, 3, 2],  # 5일
    [4, 3, 2, 6, 5, 4, 2, 3, 5, 6, 4, 3],  # 6일
    [3, 2, 5, 4, 6, 3, 4, 5, 2, 3, 6, 4],  # 7일
    [4, 6, 3, 5, 7, 8, 6, 3, 2, 4, 5, 6],  # 8일
    [5, 4, 6, 7, 3, 2, 4, 6, 5, 3, 2, 7],  # 9일
    [7, 8, 3, 2, 4, 5, 6, 3, 7, 4, 3, 5],  # 10일
    [3, 4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8],  # 11일
    [6, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 1],  # 12일
    [2, 3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7],  # 13일
    [5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 1, 6],  # 14일
    [4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8, 3],  # 15일
    [7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2],  # 16일
    [3, 2, 1, 6, 5, 4, 3, 2, 1, 6, 5, 4],  # 17일
    [5, 6, 7, 8, 3, 2, 5, 6, 7, 8, 3, 2],  # 18일
    [8, 7, 6, 5, 4, 3, 8, 7, 6, 5, 4, 3],  # 19일
    [4, 3, 2, 1, 6, 5, 4, 3, 2, 1, 6, 5],  # 20일
    [6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 7],  # 21일
    [7, 8, 5, 4, 3, 6, 7, 8, 5, 4, 3, 6],  # 22일
    [3, 4, 5, 6, 7, 2, 3, 4, 5, 6, 7, 2],  # 23일
    [2, 3, 6, 5, 4, 3, 2, 3, 6, 5, 4, 3],  # 24일
    [5, 6, 7, 2, 3, 4, 5, 6, 7, 2, 3, 4],  # 25일
    [7, 8, 3, 4, 5, 6, 7, 8, 3, 4, 5, 6],  # 26일
    [3, 2, 1, 6, 5, 4, 3, 2, 1, 6, 5, 4],  # 27일
    [4, 5, 6, 7, 8, 3, 4, 5, 6, 7, 8, 3],  # 28일
    [6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 7],  # 29일
    [7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2],  # 30일
    [3, 2, 1, 6, 5, 4, 3, 2, 1, 6, 5, 4],  # 31일
]  # 2차원 리스트 (일별 데이터) 샘플데이터

# 월별 트리거: 화재가 가장 많이 발생한 월 3가지

def get_top_3_months(monthly_data):
    """ 화재가 가장 많이 발생한 상위 3개월을 반환하는 함수 """
    monthly_data_with_index = list(enumerate(monthly_data))
    monthly_data_with_index.sort(key=lambda x: x[1], reverse=True)
    top_3_months_indices = [index for index, value in monthly_data_with_index[:3]]
    top_3_months = [i + 1 for i in top_3_months_indices]  # 월은 1월부터 시작
    return top_3_months, top_3_months_indices

def get_top_5_days_per_month(daily_data, top_3_months_indices):
    """ 상위 3개월 각각에 대해 화재가 가장 많이 발생한 상위 5일을 반환하는 함수 """
    top_5_days_per_month = []
    for month_index in top_3_months_indices:
        daily_counts_for_month = [daily_data[day][month_index] for day in range(len(daily_data))]
        daily_counts_with_index = list(enumerate(daily_counts_for_month))
        daily_counts_with_index.sort(key=lambda x: x[1], reverse=True)
        top_5_days_indices = [index for index, value in daily_counts_with_index[:5]]
        top_5_days = [i + 1 for i in top_5_days_indices]  # 일은 1일부터 시작
        top_5_days_per_month.append(top_5_days)
    return top_5_days_per_month

def check_trigger(current_month, current_day, top_3_months, top_5_days_per_month):
    """ 현재 날짜가 상위 3개월 및 상위 5일에 해당하는지 확인하여 트리거를 반환하는 함수 """
    trigger_month = current_month in top_3_months
    trigger_day = False

    if trigger_month:
        month_index = top_3_months.index(current_month)
        trigger_day = current_day in top_5_days_per_month[month_index]

    if trigger_month and trigger_day:
        return True
    return False


    # 화재가 가장 많이 발생한 상위 3개월 및 해당 월의 상위 5일 계산
top_3_months, top_3_months_indices = get_top_3_months(monthly_data)
top_5_days_per_month = get_top_5_days_per_month(daily_data, top_3_months_indices)

    # 결과 출력
print("화재가 가장 많이 발생한 월 3가지:", top_3_months)
for i, month in enumerate(top_3_months):
        print(f"{month}월에서 화재가 가장 많이 발생한 일 5가지: {top_5_days_per_month[i]}")

    # 현재 날짜 설정 (예: 7월 15일)  7월15일은 포함되지 않으므로 트리거 조건 미충족이 출력됨.
current_month = 7
current_day = 15

# 트리거 작동 여부 확인
if check_trigger(current_month, current_day, top_3_months, top_5_days_per_month):
        print("트리거 작동!")
        # return 1  # 필요에 따라 반환값 설정
else:
        print("트리거 조건 미충족")

# 디버그를 위한 출력
print(f"현재 날짜: {current_month}월 {current_day}일")


""""""""""""""""""""""""""""""""" 여기부턴 온습도 데이터 트리거작동부분 """""""""""""""""
##임시로 데이터 설정해둠
monthly_temp_data = [10, 12, 15, 18, 20, 25, 30, 28, 22, 18, 15, 12]  # 평균 온도 데이터
monthly_hum_data = [70, 68, 65, 60, 58, 55, 50, 52, 60, 65, 70, 75]  # 평균 습도 데이터


def calculate_average(data):
    """ 주어진 데이터의 평균을 계산하는 함수 """
    return sum(data) / len(data)

def calculate_standard_deviation(data, mean):
    """ 주어진 데이터와 평균을 사용하여 표준편차를 계산하는 함수 """
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    return variance ** 0.5


def trigger_on_standard_deviation(temp_data, hum_data, current_month):
    """ 표준편차가 작으면 트리거를 작동시키는 함수 """
    current_temp = temp_data[current_month - 1]#파이썬의 리스트 인덱스는 0부터 시작하므로, current_month - 1을사용
    current_hum = hum_data[current_month - 1]#예를 들어, current_month가 7이면, temp_data[6]과 hum_data[6]을 가져옴

    avg_temp = calculate_average(temp_data)
    avg_hum = calculate_average(hum_data)

    std_dev_temp = calculate_standard_deviation(temp_data, avg_temp)
    std_dev_hum = calculate_standard_deviation(hum_data, avg_hum)

    # 표준편차가 작으면 트리거를 작동 (여기서는 임의로 작다고 판단하는 값을 2와 5로 설정)
    if std_dev_temp < 2 and std_dev_hum < 5:
        return True
    return False


# 현재 월 설정 (예: 7월) 임시로 설정
current_month = 7

# 트리거 작동 여부 확인
trigger = trigger_on_standard_deviation(monthly_temp_data, monthly_hum_data, current_month)

# 결과 출력
if trigger:
    print("트리거 작동!")
else:
    print("트리거 조건 미충족")

# 디버그를 위한 출력
print(f"현재 날짜: {current_month}월")
print(f"월별 평균 온도 데이터: {monthly_temp_data}")
print(f"월별 평균 습도 데이터: {monthly_hum_data}")









