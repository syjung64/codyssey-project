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

    def set_env(self):
        for key in self.__env_values :
            self.__env_values[key][1] = random.uniform(*self.__env_values[key][0])

        with open(log_file, 'a') as log :
            values = list(map(lambda x: str(f'{x[1]:.2f}'), self.__env_values.values()))
            log.write(f'{datetime.now()} | ' + ' | '.join(values) + '\n')

# DummySensor 객체 생성
ds = DummySensor(env_values)

# 환경 변수 값 설정(random)
print(f'변수갑 설정(random)')
ds.set_env()

# 환경 변수 값 읽어오기기
print(f'변수갑 읽어오기')
env = ds.get_env()
for key in env.keys():
    print(f'{key}: {env[key][1]:.2f} {env[key][2]}, 허용범위 ({env[key][0][0]}~{env[key][0][1]})')

#ds.__env_values["mars_base_internal_temperature"][1] = 0.0 
#print('***', ds.__env_values)
