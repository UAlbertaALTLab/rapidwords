import json
data = []
with open('rapidwords.txt') as f:
    for line in f:
        data.append(line.split(' ', 1))

# Process

rw = dict()
for entry in data:
    index = entry[0].split(".")
    domain = entry[1]
    hypernyms = []
    current = rw
    for k in range(0, len(index)):
        hypernyms.append(".".join(index[0:k]))
        current = current.setdefault("subindexes",dict())
        current = current.setdefault(index[k], dict())
    current["domain"] = domain.replace("\n","")
    current["index"] = entry[0]
    current["hypernyms"] = hypernyms
    current["hypernyms"].remove("")

# Process hyponyms

def add_hyponyms(entry, top):
    ans = [ top ]
    for key, value in entry.get("subindexes",dict()).items():
        ans.extend(add_hyponyms(value,top+"."+key))
    entry["hyponyms"] = ans.copy()
    entry["hyponyms"].remove(entry["index"])
    return ans

for key, value in rw["subindexes"].items():
    add_hyponyms(value,key)

flat = dict()

def flatten_data (entry) :
    flat[entry["index"]] = {
        "domain" : entry["domain"],
        "hypernyms" : entry["hypernyms"],
        "hyponyms": entry["hyponyms"]
    }
    for value in entry.get("subindexes",dict()).values():
        flatten_data(value)

for value in rw["subindexes"].values():
    flatten_data(value)

def compact_data(entry):
    for value in entry.get("subindexes",dict()).values():
        compact_data(value)
    entry.pop("hyponyms", None)
    entry.pop("hypernyms", None)

compact_data(rw)

with open ("rapidwords-compact.json","w") as f:
    json.dump(rw,f) #,indent="\t")

with open("rapidwords.json", "w") as f:
    json.dump(flat,f) #,indent="\t")