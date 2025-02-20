import json

def read_log_file(filename) :
    log_list = []
    
    with open(filename, "r", encoding='utf-8') as file:
        lines = file.readlines()

        # 1st line skip
        for line in lines[1:]:
            parts = line.strip().split(',', 2)
            if len(parts) == 3 :
                log_list.append(parts)
    return log_list

def lst_to_dict(log_entry) :
    log_dict = {}
    for entry in log_entry :
        log_dict[entry[0]] = {"event": entry[1], "message": entry[2]}
    return log_dict

def save_to_json(log_dict, filename) :

    """
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(log_dict, json_file, indent=4)
    """

    with open(filename, "w", encoding="utf-8") as json_file:
        json_file.write("{\n")
        items = list(log_dict.items())
        for i, (key, value) in enumerate(items):
            json_file.write(f'    "{key}": {{\n')
            json_file.write(f'        "event": "{value["event"]}",\n')
            json_file.write(f'        "message": "{value["message"]}"\n')
            json_file.write("    }" + ("," if i < len(items) - 1 else "") + "\n")
        json_file.write("}\n")

log_filename = "mission_computer_main.log"
json_filename = "mission_computer_main.json"

log_entry = read_log_file(log_filename)

log_entry.sort(reverse=True)

# list를 dictionary로 변경
log_dict = lst_to_dict(log_entry)

# JSON 파일로 저장
save_to_json(log_dict, json_filename)

for entry in log_entry:
    print(entry)