data = {}
quit = True
while quit:
    hex_str = input("16 進文字列を入力してください > ").strip()
    if hex_str == "quit":
        quit=False
    else:
        byte_data = bytes.fromhex(hex_str)
        text = byte_data.decode("utf-8")
        data[hex_str]=text
        print("→ 文字列：", text)
file_name = "ansKeys.txt"
with open(file_name, "w") as file:
    for key, value in data.items():
        if isinstance(value, list):
            file.write(f"{key.capitalize()}: {', '.join(value)}\n")
        else:
            file.write(f"{key.capitalize()}: {value}\n")

print(f"saved")