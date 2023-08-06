char_to_num = {
    "<sos>" : 0,
    "a" : 1,
    "b" : 2,
    "c" : 3,
    "d" : 4,
    "e" : 5,
    "f" : 6,
    "g" : 7,
    "h" : 8,
    "i" : 9,
    "j" : 10,
    "k" : 11,
    "l" : 12,
    "m" : 13,
    "n" : 14,
    "o" : 15,
    "p" : 16,
    "q" : 17,
    "r" : 18,
    "s" : 19,
    "t" : 20,
    "u" : 21,
    "v" : 22,
    "w" : 23,
    "x" : 24,
    "y" : 25,
    "z" : 26,
    " " : 27,
    "," : 28,
    "." : 29,
    "'" : 30,
    "<unk>" : 31,
    "<eos>" : 32
}

def get_charmap():
    """
    Returns the charmap in the form of (char):(num)
    """
    return char_to_num

def get_reverse_charmap():
    """
    Returns the charmap in the form of (num):(char)
    """
    return dict([(char_to_num[k], k) for k in char_to_num.keys()])

def text_to_num(text):
    """
    Converts a string to a list of numbers
    """
    target = [char_to_num["<sos>"]]
    text = text.lower()

    for letter in text:
        if letter in char_to_num.keys():
            target.append(char_to_num[letter])
        else:
            target.append(char_to_num["<unk>"])
    target.append(char_to_num["<eos>"])
    return target
