users=[
    {"name":"Kaung Set Lin","password":"abc"},
    {"name":"Bihimu","password":"abc"},
]

def LockIn(
    name =input("Please input your name. => "),
    password =input("Please input your password. => ")
):
    lock_in =False
    for i in users:
        if i["name"]==name and i["password"]==password:
            lock_in = True
    if lock_in:
        print("Access granted")
    else:
        print("Access denied")
    return lock_in

print(LockIn())