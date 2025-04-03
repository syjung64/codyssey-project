# mars_mission_computer.py
# 더미 센서 시스템
# 2025-03-23

import random

#with open('current_time.txt') as f:
    #CURRENT_TIME = f.read().strip()

CURRENT_TIME = '2025-12-12-00-00-00'

class DummySensor:
    ENV_VALUE_CONFIG = {
        'mars_base_internal_temperature': (18, 30, 'int'),
        'mars_base_external_temperature': (0, 21, 'int'),
        'mars_base_internal_humidity': (50, 60, 'int'),
        'mars_base_internal_co2': (0.02, 0.1, 'float'),
        'mars_base_internal_oxygen': (4, 7, 'int'),
    }

    LOG_FILENAME = 'sensor.log'
    DELIMITER = ', '

    def __init__(self):
        self.env_values = {key: 0 for key in self.ENV_VALUE_CONFIG.keys()}

    def _file_exists(self, path):
        try:
            with open(path, "r"):
                return True
        except FileNotFoundError:
            return False

    def _log_env(self):
        file_needs_header = not self._file_exists(self.LOG_FILENAME)

        log_values = [CURRENT_TIME] + [
            str(self.env_values[key]) for key in self.env_values
        ]
        log_line = self.DELIMITER.join(log_values) + '\n'

        with open(self.LOG_FILENAME, 'a') as log_file:
            if file_needs_header:
                header_keys = ['datetime'] + list(self.env_values.keys())
                header_line = self.DELIMITER.join(header_keys) + "\n"
                log_file.write(header_line)

            log_file.write(log_line)

    def set_env(self):
        for key, (start, end, value_type) in self.ENV_VALUE_CONFIG.items():
            if value_type == 'int':
                self.env_values[key] = random.randint(start, end)
            elif value_type == 'float':
                self.env_values[key] = round(random.uniform(start, end), 2)

    def get_env(self):
        self._log_env()
        return self.env_values


if __name__ == '__main__':
    ds = DummySensor()
    ds.set_env()
    ds.get_env()