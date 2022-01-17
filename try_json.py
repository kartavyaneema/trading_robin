import json


out = [] 
out.append({"a":54, "b":87})
out.append({"a":34532, "b":534})

jsonFile = open("./Data/data.json", "w")
jsonString = json.dumps(out)
jsonFile.write(jsonString)
jsonFile.close()

# import json

# f = open('./Data/data.json')

# data = json.load(f)
# print(data[0]['a'] + 2)