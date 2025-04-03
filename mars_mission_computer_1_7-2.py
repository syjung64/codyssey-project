import random
import time
import msvcrt
import threading

log_file = 'env.log'

# 환경 변수 범위 설정 (class 변수)
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18, 0, '도'],
    "mars_base_external_temperature": [(0, 21), 0, 0, '도'],
    "mars_base_internal_humidity": [(50, 60), 50, 0, '%'],
    "mars_base_external_illuminance": [(500, 715), 500, 0, 'W/m2'],
    "mars_base_internal_co2": [(0.02, 0.1), 0.02, 0, '%'],
    "mars_base_internal_oxygen": [(4, 7), 4, 0, '%']
}

class MissionComputer:

    def __init__(self, env_values):
        self.env_values = env_values
        self.stop_flag = False

    def key_listener(self):
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b'q':
                    print('졸료 키 q 눌림')
                    self.stop_flag = True
                    break
        
    def get_sensor_data(self, ds, interval=10, ave_interva_min = 1) :
        global stop_flag
        listener_thread = threading.Thread(target=self.key_listener, daemon=True)
        listener_thread.start()

        ave_values_sec = ave_interva_min * 60
        loop = ave_values_sec // interval

        while not self.stop_flag:
            print("\n환경 변수 업데이트:")
            ds.set_env()
            self.env_values = ds.get_env()
            for key in self.env_values.keys():
                print(f"{key}: {self.env_values[key][1]:.2f}, 허용용범위 ({self.env_values[key][0][0]}~{self.env_values[key][0][1]})")

            if ave_values_sec > 0 :
                ave_values_sec = ave_values_sec - interval
                for key in self.env_values.keys():
                    self.env_values[key][2] += self.env_values[key][1]
                    print(f"--- {key}: {self.env_values[key][2]:.2f})")

            else :
                for key in self.env_values.keys():
                    print(f"{ave_interva_min} 분 평균 - {key}: {(self.env_values[key][2]/loop):.2f})")
                    self.env_values[key][2] = 0
                ave_values_sec = ave_interva_min * 60

            time.sleep(interval)

class DummySensor:
    def __init__(self, env_values):
        self.env_values = env_values

        if not self.__file_exist(log_file):
            with open(log_file, 'a') as log:
               headers = self.env_values.keys()
               log.write('Date | ' + ' | '.join(headers) + '\n')

    def __file_exist(self, log_file):
        try:
            with open(log_file, 'r'):
                return True
        except FileNotFoundError:
            return False   
        
    def get_env(self):
        return self.env_values

    def set_env(self):
        now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print('---', now_str)
        for key in self.env_values :
            self.env_values[key][1] = random.uniform(*self.env_values[key][0])

        with open(log_file, 'a') as log :
            values = list(map(lambda x: str(f'{x[1]:.2f}'), self.env_values.values()))
            log.write(f'{now_str} | ' + ' | '.join(values) + '\n')

# DummySensor 객체 생성
ds = DummySensor(env_values)

# MissionComputer 객체 생성
RunComputer = MissionComputer(env_values)

#ds.set_env()
RunComputer.get_sensor_data(ds, interval=20)
