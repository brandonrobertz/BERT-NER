import codecs
import os
import json
import sys

from sklearn.model_selection import train_test_split


def write_out(dataset, filename, overwrite=True):
    if not overwrite and os.path.exists(filename):
        print(f"Data exists: {filename}! Not overwriting")
    else:
        with open(filename, "w") as f:
            udata = bytes("".join(dataset), "utf-8")
            asciidata=udata.decode("ascii","ignore")
            f.write(asciidata)

if __name__ == "__main__":
    with codecs.open(sys.argv[1], "r", encoding="utf-8") as f:
        data = f.readlines()

    print("Data", len(data))

    labels = set()
    for line in data:
        if not line.strip():
            continue
        word, label = line.strip().split(" ")
        labels.add(label)

    train, test = train_test_split(data, test_size = 0.2)
    test, val = train_test_split(test, test_size = 0.5)

    print("Train", len(train))
    print("Test", len(test))
    print("Validation", len(val))

    write_out(train, "data/train.txt")
    write_out(test, "data/test.txt")
    write_out(val, "data/valid.txt")
    with open("data/labels.json", "w") as f:
        f.write(json.dumps(sorted(list(labels), key=lambda l: l.split("-")[1] if "-" in l else l)))