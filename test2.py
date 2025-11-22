import os

n = 0
l = 0
print_count = 0
for i in os.listdir():
    if ".py" in i:
        with open(i, "r", encoding="utf-8") as f:
            data = f.readlines()
            for index, j in enumerate(data):
                n+=len(j)
                if "print" in j:
                    print_count +=1
                    print(i, index+1)
            l+=len(data)
            print(f"{i} {len(data)}줄")
for i in os.listdir("widgets"):
    if ".py" in i:
        with open(os.path.join("widgets", i), "r",encoding="utf-8") as f:
            data = f.readlines()
            for index, j in enumerate(data):
                n+=len(j)
            if "print" in j:
                print_count += 1
                print(i, index+1)
            l+=len(data)
            print(f"{i} {len(data)}줄")
for i in os.listdir("utils"):
    if ".py" in i or ".sql" in i:
        with open(os.path.join("utils", i), "r",encoding="utf-8") as f:
            data = f.readlines()
            for index, j in enumerate(data):
                n+=len(j)
            if "print" in j:
                print_count += 1
                print(i, index+1)
            l+=len(data)
            print(f"{i} {len(data)}줄")
print(f"{n} 글자")
print(f"{l} 줄")
print(print_count)
input()
# from typing import Generator
#
#
# def echo_round() -> Generator[int, float, str]:
#     while True:
#         sent = yield
#         yield round(sent)
#         if sent<0:
#             break
#     return 'Done'
#
# e = echo_round()
# values = [1.6, 3.7, 7.9, -1.0]
# for n in values:
#     a= next(e)
#     e.send(n)
# print(e)
