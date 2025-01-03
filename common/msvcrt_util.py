import msvcrt

# キーボード入力対応

# key：qなど一文字
def break_key(key):
    check_key = "b'" + key + "'"
    if msvcrt.kbhit() and msvcrt.getch() == check_key:
        return True
    else:
        return False


# key：qなど一文字
def break_key_loop(key):
    check_key = "b'" + key + "'"
    while True:
        if msvcrt.kbhit() and msvcrt.getch() == check_key:
            break


if __name__ == '__main__':
    while True:
       # key = ord(msvcrt.getch())
       key = msvcrt.getch()
       print(key)
       test = "b'" + "q" + "'"
       print(key == b'q')