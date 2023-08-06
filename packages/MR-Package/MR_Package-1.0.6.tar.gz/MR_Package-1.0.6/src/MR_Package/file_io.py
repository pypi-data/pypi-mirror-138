import MR_Package
debug_mode = MR_Package.debug_mode

if debug_mode: print(__name__ + " loading")

def read(filename):
    data = []
    with open(filename, "r+") as f:
        for line in f:
            if line:
                data.append(line.strip())
        if debug_mode:
            print("File: " + filename + ", read data: " + str(data))
        return data

def write(filename, data):
    with open(filename, "w+") as f:
        f.truncate()
        for line in data:
            f.write(line)
            f.write("\n")
            if debug_mode:
                print("File: " + filename + ", write line: " + str(line))

def append(filename, data):
    with open(filename, "a") as f:
        for line in data:
            f.write(line)
            f.write("\n")
            if debug_mode:
                print("File: " + filename + ", append line: " + str(line))


if debug_mode: print(__name__ + " loaded!")