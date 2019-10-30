import json

data = []

with open("bata_2014.txt") as file:
        data = [json.loads(line.strip()) for line in file.readlines()]

f = open("bata_2014.json", "a+")

for line in data:
    f.write(json.dumps(line, indent=3))
    f.write("\n")
