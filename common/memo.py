

def bit_search(lists):
    for i1 in range(2 ** len(lists)):
        strs = bin(i1).replace("0b", "")[::-1]
        get_lists = []
        for i2 in range(len(strs)):
            index = strs[i2]