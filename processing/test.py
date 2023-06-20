import time

with open("processing/file.txt", "r") as f:
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.1)  # wait for 100ms before checking again
            f.seek(0, 1)  # move the file pointer to the current position
        else:
            print(line)
