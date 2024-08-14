data = [1, 2, 10, 11]

f = open("file.bin", mode="wb")
for i in data:

    f.write(bytes(i))

f.close()
