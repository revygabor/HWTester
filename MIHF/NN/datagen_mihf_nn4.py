import json
import random
import JavaSolution
import math

trainparams = ["1,0.01,0.8","5,0.01,0","10,0.01,0.8","100,0.01,0.8","10,0.1,0.5","100,0.01,0.8"]
inps = ["2,3,2,1","1,1","1,2,1","1,4,6,2","3,3","2,6,6,4,2"] #make sure output count is 1

to_json = []
for z in range(len(inps)):

    sample = {}
    to_json.append(sample)

    input = []
    input.append(trainparams[z])
    input.append(inps[z])
    j = -1
    inpc = -1
    for i in inps[z].split(","):
        k = int(i)
        if j > 0:
            for m in range(k):
                line = []
                for n in range(j):
                    line.append(str(random.uniform(-0.1, 0.1)))
                line.append(str(random.uniform(-0.1, 0.1)))
                line = ",".join(line)
                input.append(line)
        else:
            inpc = k
        j = k
    outpc = k

    sc = random.randint(10, 50)
    input.append(str(sc))  # sample count
    for i in range(sc):
        line = []
        sum = 0
        for n in range(inpc):
            xx = random.uniform(-1, 1)
            sum += xx
            line.append(str(xx))
        for n in range(outpc):
            line.append(str(3*math.sin(sum * (n+10) / 5.0)))
        line = ",".join(line)
        input.append(line)

    input.append("\n")
    input = "\n".join(input)
    sample["input"] = input

    sol = JavaSolution.JavaSolution("/home/steve/workspace/MI-HF-NN/src/","/home/steve/workspace/MI-HF-NN/bin/")
    sol.prepare()
    runnable, _ = sol.find_runnable("NNSolutionFour")
    (stdout, stderr, extraerr) = sol.run_java(runnable,input)
    sample["target"] = stdout

with open("iodata_mihf_nn4.json", "w") as file:
    json.dump(to_json, file, sort_keys=True, indent=4)
