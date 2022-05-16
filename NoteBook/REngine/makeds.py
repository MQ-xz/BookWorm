file = open('dataset.txt', 'r')
for line in file.readlines():
    nline = line.split('"')
    print('{"prompt":"'+str(nline[3])+ '\\n' +" ".join(nline[-2].split(" ")[:15])+'", "completion":" ' + str(nline[-2][15:])+'"}')