data = {}
quit = True
def Asdf(s):
    result = ""
    for i in range(0, len(s), 2):
        result+=s[i:i+2]+" "
    return result
while quit:
    text = input("文字列を入力してください > ").strip()
    if text == "quit":
        quit=False
    else:
        byte_data = text.encode("utf-8") 
        print(byte_data)
        hex_str = byte_data.hex() 
        hex_str=Asdf(hex_str)
        data[hex_str]=text
        print("→ 16 進列:", hex_str)
file_name = "ansKeys.txt"
with open(file_name, "w") as file:
    for key, value in data.items():
        if isinstance(value, list):
            file.write(f"{key.capitalize()}: {', '.join(value)}\n")
        else:
            file.write(f"{key.capitalize()}: {value}\n")

print(f"saved")