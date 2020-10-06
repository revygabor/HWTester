import json
from test_generator import generate_task

with open("tests.json", 'r') as json_file:
    param_list = json.load(json_file)

for i, params in enumerate(param_list):
    input_file = open("examples/input{0}.txt".format(str(i)), 'w')
    output_file = open("examples/output{0}.txt".format(str(i)), 'w')
    input_str, output_str = generate_task(params)
    input_file.write(input_str)
    output_file.write(output_str)
    input_file.close()
    output_file.close()
