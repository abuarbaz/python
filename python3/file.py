f = open("demofile2.txt", "a")
f.write("Tell me something")
f.close()

f = open("demofile2.txt", "r")
print(f.read())
