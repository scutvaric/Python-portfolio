morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.',
    'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.', ' ': '/'
}


def morse_translator(input, direction, translated_word):
    if direction == "alphabet":
        morse_chars = input.split(" ")
        for code in morse_chars:
            for key, value in morse_code.items():
                if value == code:
                    print(key)
                    translated_word.append(key)
        print("".join(translated_word))
    elif direction == "morse":
        for letter in input:
            new_letter = morse_code[letter.upper()]
            print(new_letter)
            translated_word.append(new_letter)
        print(" ".join(translated_word))
    else:
        print("Wrong input please try again")

is_on = True

while is_on:
    direction = input("Type 'alphabet' to translate from morse code to alphabet or type "
                      "'morse' to translate from alphabet to morse: ").lower()
    user_input = input("Insert the word you'd like transformed: ").lower()

    translated_word = []
    morse_translator(user_input, direction,translated_word)
    again= input("Translate another word? (yes/no): ").lower()
    if again != "yes":
        is_on=False

