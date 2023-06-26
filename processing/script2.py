import time

with open("processing/file.txt", "a") as f:
    for i in range(100):
        f.write(str(i) + "\n")
        f.flush()
        time.sleep(0.1)
