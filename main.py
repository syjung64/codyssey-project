LOG_NAME = 'mission_computer_main.log'
ISSUE_NAME = 'issue.log'

log = []
def read_file(filename) :
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            while True :
                line = file.readline()    # 라인을 요소로 한 리스트트
                if not line :
                    break
                log.append(line.strip().split(','))

        print('----log file 출력----')
        for item in log:
            print(item)

        print('\n----log file 역순 출력----')
        sorted_log = sorted(log, key=lambda x : x[0], reverse=True)
        for item in sorted_log:
            print(item)

        print('\n----문제가 된 log만 출력(2023-08-27 11:35:00 이후 로그)----')
        issue_log = [item for item in log if item[0] >= '2023-08-27 11:35:00']
        for item in issue_log:
            print(item)

        print('\n----문제가 된 log(2023-08-27 11:35:00 이후 로그)만 issue_log파일로 저장----')
        with open(ISSUE_NAME, 'w', encoding='utf-8') as file :
            for item in issue_log:
                file.write(','.join(map(str, item)) + '\n')

    except FileNotFoundError:
        print(f'Ereror: The File "{filename}" was not found')
    except Exception as e:
        print(f'An error occured: {e}')

if __name__ == '__main__' :
    read_file(LOG_NAME)