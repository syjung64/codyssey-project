import random
import time

class MissionComputer:
    def __init__(self, env_values):
        self.env_values = env_values
        
    def get_sensor_data(self, sensor, interval=10) :

        while True:
            print("\n환경 변수 업데이트:")
            self.env_values = sensor
            for key in self.env_values.keys():
                print(f"{key}: {self.env_values[key][1]:.2f}, 허용용범위 ({self.env_values[key][0][0]}~{self.env_values[key][0][1]})")
            time.sleep(interval)

class DummySensor:
    def __init__(self, env_values):
        self.env_values = env_values
        self.header = False

        try:
            with open(log_file, 'r'):
                pass
        except FileNotFoundError:
            self.header = True

        if self.header:
            with open(log_file, 'a') as log:
               headers = self.env_values.keys()
               log.write('Date, | ' + ' | '.join(headers) + '\n')
    
    def get_env(self):
        return self.env_values

    def set_env(self):
        for key in self.env_values :
            self.env_values[key][1] = random.uniform(*self.env_values[key][0])

        with open(log_file, 'a') as log :
            values = list(map(lambda x: str(f'{x[1]:.2f}'), self.env_values.values()))
            log.write(f'{datetime.now()} | ' + ' | '.join(values) + '\n')


# 환경 변수 범위 설정
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18, '도'],
    "mars_base_external_temperature": [(0, 21), 0, '도'],
    "mars_base_internal_humidity": [(50, 60), 50, '%'],
    "mars_base_external_illuminance": [(500, 715), 500, 'W/m2'],
    "mars_base_internal_co2": [(0.02, 0.1), 0.02, '%'],
    "mars_base_internal_oxygen": [(4, 7), 4, '%']
}

# DummySensor 객체 생성
ds = DummySensor(env_values)

RunComputer = MissionComputer(env_values)

#ds.set_env()
RunComputer.get_sensor_data(ds)
