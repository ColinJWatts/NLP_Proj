from os import listdir
from datetime import timezone 
import datetime 
import hashlib
import io

class Librarian():
    def __init__(self, maxDocuments=1000, path="D:\\SurfaceDocs\\MSAI\\NLP\\project\\dataCollection\\data"):
        self.path = path
        self.refresh()
        self.maxDocuments = maxDocuments
        self.documents = []

    def refresh(self):
        self.files = listdir(self.path)

    def parseDoc(self, docStr):
        doc = {}
        dat = docStr.split("***")
        if len(dat) < 3:
            return None
        doc["id"] = dat[0][len("id: "):len(dat[0])]
        doc["channel"] = dat[1][len("channel: "):len(dat[1])]
        doc["text"] = dat[2][len("text: "):len(dat[2])]
        return doc

    def parseFile(self, fileName):
        if fileName not in self.files:
            return []

        raw = None
        with open(f"{self.path}\\{fileName}", 'r', encoding='utf8') as f:
            raw = f.read()
        
        data = raw.split(']')
        docs = []
        for d in data:
            newDoc = self.parseDoc(d.replace('\n','')[1:len(d)])
            if not newDoc is None:
                docs.append(newDoc)
        return docs

    def saveDocs(self):
        toSave = ""

        dt = datetime.datetime.now() 
  
        utc_time = dt.replace(tzinfo = timezone.utc) 
        utc_timestamp = utc_time.timestamp() 
        fileName = f"data{utc_timestamp}.txt"
        for doc in self.documents:
            toSave = toSave + f"[id: {doc['id']}***channel: {doc['channel']}***text: {doc['text']}]\n"

        with open(f"{self.path}\\{fileName}", 'w', encoding="utf-8") as f:
            f.write(toSave)
            f.flush()
        self.documents = []
        self.refresh()

    def createDoc(self, id, channel, text):
        doc = {}
        doc["id"] = hashlib.sha256(bytes(id, 'utf-8')).hexdigest()
        doc["channel"] = channel
        doc["text"] = text.replace('*', '').replace('[', '').replace(']', '')
        return doc

    def addDocument(self, id, channel, text):
        self.documents.append(self.createDoc(id, channel, text))
        if len(self.documents) >= self.maxDocuments:
            self.saveDocs()

    def getCorpus(self):
        corpus = []
        for f in self.files:
            corpus = corpus + self.parseFile(f)
        return corpus

    def getAllDataForUser(self, id):
        data = []
        hashed = hashlib.sha256(bytes(id, 'utf-8')).hexdigest()
        for f in self.files:
            data = data + self.parseFile(f)

        result = []
        for d in data:
            if d["id"] == hashed:
                result.append(d)

        return result

