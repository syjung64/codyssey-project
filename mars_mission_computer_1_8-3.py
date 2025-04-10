import random
import time
import threading
import platform
import psutil
import json

log_file = 'env.log'
setting_file = 'setting.txt'

# 환경 변수 범위 설정 (class 변수)
env_values = {
    "mars_base_internal_temperature": [(18, 30.5), 18, 0, '도'],
    "mars_base_external_temperature": [(0, 21), 0, 0, '도'],
    "mars_base_internal_humidity": [(50, 60), 50, 0, '%'],
    "mars_base_external_illuminance": [(500, 715), 500, 0, 'W/m2'],
    "mars_base_internal_co2": [(0.02, 0.1), 0.02, 0, '%'],
    "mars_base_internal_oxygen": [(4, 7), 4, 0, '%']
}

class SystemInfo:
    @classmethod
    def get_cpu_usage(cls):
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            return None    
    @classmethod
    def get_memory_usage(cls):
        try:
            return psutil.virtual_memory().percent
        except Exception as e:
            return None
    @classmethod
    def get_os(cls):
        try:
            return platform.system()
        except Exception as e:
            return None
    @classmethod
    def get_os_version(cls):
        try:
            return platform.version()
        except Exception as e:
            return None 
    @classmethod      
    def get_cpu_type(cls):
        try:
            return platform.processor()
        except Exception as e:
            return None
    @classmethod       
    def get_cpu_cores(cls):
        try:
            return psutil.cpu_count(logical=False)
        except Exception as e:
            return None 
    @classmethod        
    def get_memory_gb(cls):
        try:
            return round(psutil.virtual_memory().total / (1024 ** 3), 2)
        except Exception as e:
            return None 

class MissionComputer:
    def __init__(self, env_values, setting_file = 'setting.txt'):
        self.env_values = env_values
        self.stop_flag = False
        self.setting_file = setting_file
        
    def key_listener(self):
        while True:
            key = input()
            if key == 'q':
                print('System Stoped....')
                self.stop_flag = True
                break

    def get_mission_computer_info(self):
        # 운영체계, 운영체계 버전, CPU 타입, CPU 코어 수, 메모리 크기
        # JSON 출력
        try:
            with open(self.setting_file, 'r') as f:
                self.settings = json.load(f)
        except Exception as e:
            print(f'설정 파일 오류 {e}')
            return {}
        
        self.system_info = {}
        for category, option in self.settings.items():
            if category == 'system_info' :
                for key, enabled in option.items():
                    if enabled:
                        try:
                            method = getattr(SystemInfo, f'get_{key}')
                            self.system_info[key] = method()
                        except AttributeError:
                            print(f"[경고] '{key}' 항목은 지원되지 않음")
                        except Exception as e:
                            print(f"[오류] '{key}' 수집 중 예외 발생: {e}")
                            self.system_info[key] = None

        print('system info', '-' * 20)
        print(self.system_info)
        return self.system_info

    def get_mission_computer_load(self):
        # CPU 실시간 사용량, 메모리 실시간 사용량
        # JSON 출력
        try:
            with open(self.setting_file, 'r') as f:
                self.settings = json.load(f)
        except Exception as e:
            print(f'설정 파일 오류 {e}')
            return {}
        
        self.system_load = {}
        for category, option in self.settings.items():
            if category == 'system_load' :
                for key, enabled in option.items():
                    if enabled:
                        try:
                            method = getattr(SystemInfo, f'get_{key}')
                            self.system_load[key] = method()
                        except AttributeError:
                            print(f"[경고] '{key}' 항목은 지원되지 않음")
                        except Exception as e:
                            print(f"[오류] '{key}' 수집 중 예외 발생: {e}")
                            self.system_load[key] = None

        print('system load', '-'*20)
        print(self.system_load)
        return self.system_load
        
    def get_sensor_data(self, ds, interval=10, ave_interval_min = 1) :
        listener_thread = threading.Thread(target=self.key_listener, daemon=True)
        listener_thread.start()

        ave_values_sec = ave_interval_min * 60
        loop = ave_values_sec // interval
        while not self.stop_flag:
            time.sleep(interval)

            print(f'\n환경 변수 출력 (주기 - {interval} 초):')
            ds.set_env()
            self.env_values = ds.get_env()

            # 환경 변수 출력 (json)
            json_str = '{\n'
            for key in self.env_values.keys():
                json_str += f'\t"{key}": {self.env_values[key][1]:.2f},\n'
            json_str = json_str.rstrip(',\n') + '\n}'
            print(json_str)
            
            if ave_values_sec > 0 :
                for key in self.env_values.keys():
                    self.env_values[key][2] += self.env_values[key][1]
                ave_values_sec = ave_values_sec - interval

            if ave_values_sec <= 0:      
                print(f'\n{ave_interval_min} 분 평균 값 출력----')
                # 환경 변수 평균 값 출력 (json)
                json_str = '{\n'
                for key in self.env_values.keys():
                    json_str += f'\t"{key}": {self.env_values[key][2]/loop:.2f},\n'
                    self.env_values[key][2] = 0
                json_str = json_str.rstrip(',\n') + '\n}'
                print(json_str)
                
                ave_values_sec = ave_interval_min * 60

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
        for key in self.env_values :
            self.env_values[key][1] = random.uniform(*self.env_values[key][0])

        with open(log_file, 'a') as log :
            values = list(map(lambda x: str(f'{x[1]:.2f}'), self.env_values.values()))
            log.write(f'{now_str} | ' + ' | '.join(values) + '\n')

# DummySensor 객체 생성
ds = DummySensor(env_values)

# MissionComputer 객체 생성
RunComputer = MissionComputer(env_values, setting_file)
RunComputer.get_mission_computer_info()
RunComputer.get_mission_computer_load()

#ds.set_env()
#RunComputer.get_sensor_data(ds, interval=20, ave_interval_min = 1)

