import requests,db,os
from datetime import datetime,timedelta

db =db.dbCon()

users = db.getAllUsers()

def saveStoryOfUser(_id,_name, _lastSavedStroyCount):
    result=db.getAllStoryUrlOf(_id)
    directory="storyler/"+str(_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    count=int(_lastSavedStroyCount)+1
    print(_name+" storyleri..")
    for it in result:
        r = requests.get(it[3])
        fileType=(r.headers['content-type']).split("/")[1]
        if (fileType=="jpeg"):
            fileType="bmp"
        storyName=f'{count:05}'+"." + fileType

        with open(directory+'/'+storyName, 'wb') as f:
            f.write(r.content)
        db.updateLastSavedCount(_id,count)
        db.updateStoryIsDownload(it[0],1)
        count+=1
        print(_name+" storysi kayıt edildi..")

sayac =1
for it in users:
    print(sayac)
    sayac+=1
    saveStoryOfUser(it[0],it[2],it[6])
    directory="storyler/"+str(it[2])
    for i in os.listdir(directory):
        
        if i.split(".")[1]=="jpeg":
            print(i)
            os.rename(directory+"/"+i,directory+"/"+f'{int(i.split(".")[0]):05}'+".bmp")



liste={"a"}
liste.clear


for i in users:
    liste.add(i[2])


for dos in os.walk("storyler"):
    reiz=dos[0].replace("storyler","")[1:]
    if liste.__contains__(reiz):
        pass
    else:
        print(reiz)

