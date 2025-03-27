import random
from datetime import datetime

log_file = 'env.log'

# 환경 변수 범위 설정
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18, '도'],
    "mars_base_external_temperature": [(0, 21), 0, '도'],
    "mars_base_internal_humidity": [(50, 60), 50, '%'],
    "mars_base_external_illuminance": [(500, 715), 500, 'W/m2'],
    "mars_base_internal_co2": [(0.02, 0.1), 0.02, '%'],
    "mars_base_internal_oxygen": [(4, 7), 4, '%']
}

class Clock:
    year, month, day = 2025, 3, 27
    hour, minute, second = 0, 0, 0

    base_seconds = hour * 3600 + minute * 60 + second

    def __init__(self, loop_per_second=10000) :
        self.loop_count = 0
        self.loop_per_second = loop_per_second

    # 월별 일 수 정의 (윤년이 아닐 경우)
    @staticmethod
    def get_days_in_month(year, month):
        if month == 2:
            # 윤년 조건
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            else:
                return 28
        # 4, 6, 9, 11월은 30일
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31
    
    def tick(self):
        self.loop_count += 1

    def get_time(self) :
        seconds = int(self.loop_count / self.loop_per_second)
        current_time = Clock.base_seconds + seconds

        # 시, 분, 초로 환산
        new_hour = current_time // 3600
        remain = current_time % 3600
        new_minute = remain // 60
        new_second = remain % 60

        # 날짜 증가 처리
        new_day = Clock.day
        new_day += new_hour // 24
        new_hour = new_hour % 24

        # 월, 년 증가 처리
        new_month = Clock.month
        new_year = Clock.year
        while True:
            days_in_month = Clock.get_days_in_month(Clock.year, Clock.month)
            if new_day <= days_in_month:
                break
            new_day -= days_in_month
            new_month += 1
            if new_month > 12:
                new_month = 1
                new_year += 1

        now = f'{new_year}-{new_month:02d}-{new_day:02d} {new_hour:02d}:{new_minute:02d}:{new_second:02d}'
        return now

class DummySensor:
    def __init__(self, env_values):
        self.__env_values = env_values
        self.__header = False

        try:
            with open(log_file, 'r'):
                pass
        except FileNotFoundError:
            self.__header = True

        if self.__header:
            with open(log_file, 'a') as log:
               headers = self.__env_values.keys()
               log.write('Date, | ' + ' | '.join(headers) + '\n')
    
    def get_env(self):
        return self.__env_values

    def set_env(self, current_time):
        print('---', current_time)
        for key in self.__env_values :
            self.__env_values[key][1] = random.uniform(*self.__env_values[key][0])

        with open(log_file, 'a') as log :
            values = list(map(lambda x: str(f'{x[1]:.2f}'), self.__env_values.values()))
            log.write(f'{current_time} | ' + ' | '.join(values) + '\n')

c = Clock()
ds = DummySensor(env_values)     # DummySensor 객체 생성

def task1() :
    for _ in range(3):
        # 환경 변수 값 설정(random)
        print(f'변수갑 설정(random)')
        ds.set_env(c.get_time())

        # 환경 변수 값 읽어오기기
        print(f'변수갑 읽어오기')
        env = ds.get_env()
        for key in env.keys():
            print(f'{key}: {env[key][1]:.2f} {env[key][2]}, 허용범위 ({env[key][0][0]}~{env[key][0][1]})')
        yield


def task2() :
    for _ in range(3):
        for i in range(10000) : # 1초 - 10000 loop
            c.tick()
        print('10000(1초) loop 지남')
        yield

tasks = [task1(), task2()]
while tasks:
    task = tasks.pop(0)
    try:
        next(task)
        tasks.append(task)
    except StopIteration:
        pass

