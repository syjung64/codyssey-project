
filename = 'Mars_Base_Inventory_List.csv'
danger_file = 'Mars_Base_Inventory_danger.csv'
bin_file = 'Mars_Base_Inventory_List.bin'

def read_csv_file(filename) :
    try:
        csv_list = []
        with open(filename, "r", encoding='utf-8') as file:
            lines = file.readlines()

            if not lines:
                raise ValueError('파일이 비었음')
            
             # 1st line skip
            for line in lines[1:]:
                parts = line.strip().split(',', 4)
                if len(parts) == 5 :
                    parts[4] = float(parts[4])
                    csv_list.append(parts)
    except FileNotFoundError:
        print(f'Ereror: The File "{filename}" was not found')
    except ValueError as e:
        print(f"입력 데이터 오류: {e}")
    except Exception as e:
        print(f'An error occured: {e}')
    finally:
        return csv_list

def write_csv_file(filename, csv_list) :
    try:
        with open(filename, "w", encoding='utf-8') as file:
            for line in csv_list :
                file.write(','.join(map(str, line)) + '\n')
        print(f"파일 {filename}로 저장하였습니다.")
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")
    except Exception as e:
        print(f'An error occured: {e}')

# list를 이진 파일로 저장 - 참고 - pickle 모듈 (int, float, str만 처리)
def write_binary_file(bin_file, csv_list) :
    try:
        with open(bin_file, "wb") as file:
            for line in csv_list :
                file.write(b'L' + len(line).to_bytes(4, 'big'))
                for item in line :
                    if isinstance(item, float) :
                        float_str = str(item).encode('utf-8')
                        file.write(b'F' + len(float_str).to_bytes(4, 'big') + float_str)
                    elif isinstance(item, str) :
                        encoded_str = item.encode('utf-8')
                        file.write(b'S' + len(encoded_str).to_bytes(4, 'big') + encoded_str)
                    elif isinstance(item, int) :
                        file.write(b'I' + item.to_bytes(4, 'big'))
        print(f"파일 {bin_file}로 저장하였습니다.")
    except IOError as e:
        print(f"파일 저장 중 오류 발생: {e}")
    except Exception as e:
        print(f'An error occured: {e}')

# 이진 파일을 다시 읽어오기 (list - 요소 int, float, str만 처리)
def read_binary_file(bin_file):
    try:
        with open(bin_file, mode='rb') as file:
            loaded_lst = []
            while True :
                data_type = file.read(1)
                if not data_type :
                    break

                if data_type == b'L' :
                    sublist_len = int.from_bytes(file.read(4), 'big')
                    sublist = []
                    for _ in range(sublist_len) :
                        item_type = file.read(1)
                        if item_type == b'F' : # 실수
                            length = int.from_bytes(file.read(4), 'big')
                            value = float(file.read(length).decode('utf-8'))
                            sublist.append(value)
                        elif item_type == b'S' : # 문자열
                            length = int.from_bytes(file.read(4), 'big')
                            value = file.read(length).decode('utf-8')
                            sublist.append(value)
                        elif item_type == b'I' : # 정수
                            value = int.form_bytes(file.read(4), 'big')
                            sublist.append(value)
                loaded_lst.append(sublist)
            return loaded_lst

    except FileNotFoundError:
        print("이진 파일을 찾을 수 없습니다.")
    except UnicodeDecodeError as e:
        print(f"디코딩 오류 발생: {e}")
    except IOError as e:
        print(f"파일 읽기 중 오류 발생: {e}")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")

def print_csv(csv_entry, seq=True) :
    print(f'csv 파일 출력----------')
    csv_entry.sort(key = lambda item: item[4], reverse=seq)

    for entry in csv_entry:
        print(entry)

def get_danger(csv_entry, level=0.9) :
    d_entry = list(filter(lambda x: x[4] >=  level, csv_entry))
    return d_entry


# 인화성 지수 파일 읽어오기
csv_lst = read_csv_file(filename)
print_csv(csv_lst)

# 인화성 지수 0.7이상 읽어오기
danger_lst = get_danger(csv_lst, level=0.7)
print_csv(danger_lst)

# 인화성 지수 0.7이상 csv 파일로 저장하기기
write_csv_file(danger_file, danger_lst)

# 추가 과제
print('\n\n추가 과제')

print('\n\n인화물질 리스트')
for line in danger_lst :
    print(line)

print('\n\n인화물질 리스트 bin 파일 저장')
# 인화성 지수 0.7 이상 binary 파일로 저장장
write_binary_file(bin_file, danger_lst)

# 이진 파일을 다시 읽어 화면에 출력
print('\n\n인화물질 리스트 bin 파일 출력')
lst = read_binary_file(bin_file)
for line in lst :
    print(line)


## 이진파일과 파이썬 텍스트(utf-8) 파일일 비교 설명
lst = [[1, 0.88, 'abc'], [2, 0.99, 'xxx']]
write_binary_file('a.bin', lst)
write_csv_file('a.txt', lst)