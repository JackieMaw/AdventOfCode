def translate_to_ascii(int_code):
    ascii_output = ''.join([chr(i) for i in int_code])
    ascii_output_no_empty_lines = [line for line in ascii_output.split("\n") if line]
    return ascii_output_no_empty_lines