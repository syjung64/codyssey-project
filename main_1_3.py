def read_csv_file(filename) :
    try:
        csv_list = []

        with open(filename, "r", encoding='utf-8') as file:
            lines = file.readlines()

            # 1st line skip
            for line in lines[1:]:
                parts = line.strip().split(',', 4)
                if len(parts) == 5 :
                    # 5번쨰 원소 문자열을 실수로 변환환
                    parts[4] = float(parts[4])
                    csv_list.append(parts)
        return csv_list
    except FileNotFoundError:
        print(f'Ereror: The File "{filename}" was not found')
        return []
    except Exception as e:
        print(f'An error occured: {e}')
        return []

def write_csv_file(lstname, filename) :
    try :
        with open(filename, "w", encoding="utf-8") as file:
            file.write("Substance,Weight (g/cm³),Specific Gravity,Strength,Flammability\n")
            for line in lstname :
                # 5번째 원소를 포함하여 원소 자료형을 문자열로 변환하여 join
                file.write(",".join(map(str, line)) + "\n")
    except FileNotFoundError:
        print(f'Ereror: The File "{filename}" was not found')
    except Exception as e:
        print(f'An error occured: {e}')

filename = "Mars_Base_Inventory_List.csv"
csvfilename = "Mars_Base_Inventory_danger.csv"

csv_entry = read_csv_file(filename)

# 인화값(5번째 항목)으로 정렬렬
csv_entry.sort(key = lambda item: item[4])

# 인화값으로 정렬된 리스트 출력력
print("\n 인화성 값으로 정렬한 리스트 출력 : ")
for entry in csv_entry:
    print(entry)

# 인화성 값이 0.7이상인 항목 추출
filtered_list = []
for item in csv_entry:
    if item[4] >= 0.7 :
        filtered_list.append(item)

print("\n 인화성 값이 0.7이상인 항목 : ")
for item in filtered_list:
    print(item)

print("\n 인화성 값이 0.7이상인 항목을 저장: ")
write_csv_file(filtered_list, csvfilename)