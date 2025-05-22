def caesar_cipher_decode(target_text):
    dictionary = ['mars', 'earth', 'love']  # 간단한 단어 사전

    def shift_char(c, shift):
        if c.isupper():
            return chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        elif c.islower():
            return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        else:
            return c

    decoded_texts = []
    print("가능한 해독 결과:")
    for shift in range(26):
        decoded = ''.join(shift_char(c, shift) for c in target_text)
        decoded_texts.append(decoded)
        print(f"[{shift}] {decoded}")

        # 자동 중단 조건: 사전 단어가 포함되면 저장 후 종료
        if any(word in decoded.lower() for word in dictionary):
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(decoded)
            print(f"\n자동으로 해독됨! 시프트: {shift}")
            print("result.txt에 저장 완료했어.")
            return

    # fallback: 사람이 직접 선택
    try:
        choice = int(input("\n자동으로 찾지 못했어. 사람이 직접 번호 선택해 줘 (0~25): "))
        if 0 <= choice < 26:
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(decoded_texts[choice])
            print("result.txt에 저장 완료했어.")
        else:
            print("잘못된 번호야. 저장하지 않았어.")
    except ValueError:
        print("숫자를 입력해야 해. 저장하지 않았어.")


if __name__ == "__main__":
    try:
        with open("password.txt", "r", encoding="utf-8") as file:
            encrypted_text = file.read().strip()
            caesar_cipher_decode(encrypted_text)
    except FileNotFoundError:
        print("password.txt 파일을 찾을 수 없어.")
