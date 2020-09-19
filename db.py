import sqlite3,time
from datetime import datetime,timedelta

class dbCon:

    conn = sqlite3.connect(r"instaStoryTube.db")

    def getAllUsers(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM instaAccount")
        return cur.fetchall() 

    def isUrlDownloaded(self):
        return True


    def getAllStoryOf(self,user):
        cur =self.conn.cursor()
        cur.execute("SELECT * FROM downloadedStory where userId="+str(user))
        return cur.fetchall() 

    def getAllStoryUrlOf(self,user):
        cur =self.conn.cursor()
        cur.execute("SELECT * FROM downloadedStory where userId="+str(user)+" and isDownload=0")
        return cur.fetchall() 

    def createDownloadStoryEntry(self,userId,storyDownTime,storyUrl,isDownload,storySize):
        sql = 'INSERT INTO downloadedStory(userId,storyDownTime,storyUrl,isDownload,storySize) VALUES(?,?,?,?,?)' 
        cur = self.conn.cursor()
        records = (userId,storyDownTime,storyUrl,isDownload,storySize)
        
        cur.execute(sql,records)
        self.conn.commit()
        return cur.lastrowid


    def checkStoryUrlIfExsist(self,storySize,userId):
        cur = self.conn.cursor()
        yesterday = (datetime.now()-timedelta(days = 1))
        cur.execute("SELECT * FROM downloadedStory WHERE storyDownTime>? and userId=? and storySize=?",(yesterday,userId,storySize))
        result=cur.fetchall()

        if (len(result)>0):
            return 1
        else:
            return 0

    def updateStoryCountAndLastChecked(self,id,time,count):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE instaAccount SET storyCount =?,lastCheckedAt =? WHERE id=?", (count,time,id))
            self.conn.commit()
            return 1
        except :
            return 0

    def updateLastChecked(self,id,time):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE instaAccount SET lastCheckedAt =? WHERE id=?", (time,id))
            self.conn.commit()
            return 1
        except :
            return 0


    def updateLastSavedCount(self,id,count):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE instaAccount SET lastSavedStoryCount =? WHERE id=?", (count,id))
            self.conn.commit()
            return 1
        except :
            return 0

    def updateStoryIsDownload(self,id,isDownload):
        try:
            cur = self.conn.cursor()
            cur.execute("UPDATE downloadedStory SET isDownload =? WHERE id=?", (isDownload,id))
            self.conn.commit()
            return 1
        except :
            return 0

    def saveUserIfNotExist(self,_userName):
        sql = 'INSERT or ignore INTO instaAccount(userName) VALUES(?)' 
        cur = self.conn.cursor()
        records = (_userName,)
        
        cur.execute(sql,records)
        self.conn.commit()
        return cur.lastrowid

    def saveNameIfNotExist(self,_name,_userName):
        conn = sqlite3.connect(r"instaStoryTube.db")
        cur = conn.cursor()
        cur.execute("UPDATE instaAccount SET name =? WHERE name=0 and userName=?", (_name,_userName))
        conn.commit()
        conn.close()
        time.sleep(1)
        print(_name)
        return cur.lastrowid

    def getAllUsersNullName(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM instaAccount where name=0")
        return cur.fetchall() 