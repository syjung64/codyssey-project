import random

class DummySensor:
    def __init__(self, env_values):
        self.env_values = env_values
    
    def get_env(self):
        return self.env_values

    def set_env(self):
        for key in self.env_values :
            self.env_values[key][1] = random.uniform(*self.env_values[key][0])


# 환경 변수 범위 설정
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18],
    "mars_base_external_temperature": [(-110, -35), -110],
    "mars_base_internal_humidity": [(20, 60), 20],
    "mars_base_external_illuminance": [(50, 600), 50],
    "mars_base_internal_co2": [(300, 1000), 300],
    "mars_base_internal_oxygen": [(0.02, 0.13), 0.02]
}

def printenv(env) :
    for key in env.keys():
        print(f"{key}: {env[key][1]:.2f}, 허용용범위 ({env[key][0][0]}~{env[key][0][1]})")

# DummySensor 객체 생성
ds = DummySensor(env_values)

# 환경 변수 값 읽어오기기
print(f'변수갑 읽어오기')
env = ds.get_env()
printenv(env)

# 환경 변수 값 설정(random)
print(f'변수갑 설정(random)')
ds.set_env()

# 환경 변수 값 읽어오기기
print(f'변수갑 읽어오기')
env = ds.get_env()
printenv(env)