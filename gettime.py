import os
rootdir = '/home/cheng/Downloads/mstar40'

list = os.listdir(rootdir)

starttxt = '['
endtxt = ']'

num = 0
ecpohList = []

for i in range(0,len(list)):
    targetReachedNum = 1
    summ = 0
    if list[i][:20] == '256agents_80size_0.3':
        path = os.path.join(rootdir,list[i])
        f=open(path,"r", encoding = 'utf-8',errors='ignore')
        line = f.readline()
        
        num += 1

        if(len(line.split(' ')[1]) == 4):
            targetReachedNum = int(line.split(' ')[1][:3])
        elif(len(line.split(' ')[1]) == 5):
            targetReachedNum = int(line.split(' ')[1][:4])
        elif(len(line.split(' ')[1]) == 6):
            targetReachedNum = int(line.split(' ')[1][:5])
        elif(len(line.split(' ')[1]) == 2):
            targetReachedNum = int(line.split(' ')[1][:1])
        else:
            targetReachedNum = int(line.split(' ')[1][:2])
        print(targetReachedNum)

        if(targetReachedNum == 0):
            targetReachedNum = 1

        pos1 = line.find(starttxt)
        pos2 = line.find(endtxt)
        pathlist = line[pos1+1:pos2]
        pathlist = pathlist.split(', ')
        for i in range(0,len(pathlist)):
            # print(float(pathlist[i]))
            summ += float(pathlist[i])
            
        ecpoh = summ / targetReachedNum
        ecpohList.append(ecpoh)
        # print(len(ecpohList))
        # print(ecpohList)

avarageSum = 0
print(len(ecpohList))
for i in range(0,len(ecpohList)):
    avarageSum += ecpohList[i]
# print(ecpohList)
print(avarageSum / len(ecpohList))

