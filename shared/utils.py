def convert_int_stringbyte(value, max_length=16):
    if max_length < 1:
        max_length = 32
    value = str(value)

    if len(value) > max_length:
        return '9' * max_length
    fill_number = max_length - len(value)

    return ' ' * fill_number + value