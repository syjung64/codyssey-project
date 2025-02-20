def read_file(filename) :
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f'Ereror: The File "{filename}" was not found')
    except Exception as e:
        print(f'An error occured: {e}')

read_file('./mission_computer_main.log')