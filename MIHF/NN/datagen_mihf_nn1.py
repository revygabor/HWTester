import json

inps = ["2,3,1","2,3,2,1","1,4,6,1","3,3","2,6,2,3,1,4","100,100,100,100,10"]


to_json = []
for inp in inps:
    sample = {}
    to_json.append(sample)
    sample["input"] = inp + "\n\n"

    out = []
    out.append(inp)
    j = -1
    for i in inp.split(","):
        k = int(i)
        if j > 0:
            for m in range(k):
                line = []
                for n in range(j):
                    line.append("N")
                line.append("0")
                line = ",".join(line)
                out.append(line)
        j = k
    out.append("")
    out = "\n".join(out)
    sample["target"] = out

with open("iodata_mihf_nn1.json", "w") as file:
    json.dump(to_json, file, sort_keys=True, indent=4)
