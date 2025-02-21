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
    
    def get_env(self):
        return self.env_values

    def set_env(self, interval=5):
        while True:
            for key in self.env_values :
                self.env_values[key][1] = random.uniform(*self.env_values[key][0])
            time.sleep(interval)



# 환경 변수 범위 설정
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18],
    "mars_base_external_temperature": [(-110, -35), -110],
    "mars_base_internal_humidity": [(20, 60), 20],
    "mars_base_external_illuminance": [(50, 600), 50],
    "mars_base_internal_co2": [(300, 1000), 300],
    "mars_base_internal_oxygen": [(0.02, 0.13), 0.02]
}

# DummySensor 객체 생성
ds = DummySensor(env_values)
RunComputer = MissionComputer(env_values)

#ds.set_env()
RunComputer.get_sensor_data(ds.get_env())
