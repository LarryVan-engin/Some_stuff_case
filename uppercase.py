import os

def uppercase(text):
    return text.upper()

if __name__ == "__main__":
    try:
        input_text = input()
        print(uppercase(input_text))
    except Exception as e:
        print(e)