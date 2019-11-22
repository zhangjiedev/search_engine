import shelve
import os

from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

from utils import PriorityQueue

import bs4
import json

class Index:
    ''' Inverted index datastructure '''

    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
        self.stemmer = SnowballStemmer("english")
        self.index = shelve.open("save/index")
        self.urls = shelve.open("save/urls")
        self.id = 0


    def get_document(self):
        '''
        Iterate through all directories in DEV/, yield the name of a document.
        '''
        root = "/Users/jack/Desktop/Fall 2019/CS 121/projects/project_3/DEV/"
        count = 0

        with os.scandir(root) as directories:
            for directory in directories:
                print("working on " + directory.name)
                with os.scandir(directory) as folder:
                    for document in folder:
                        yield root + directory.name + '/' + document.name
                    print(directory.name + " is completed!!!")
                count += 1
                print(str(count) + " / 88")


    def _extract_content(self, doc_name: str):
        '''
        Extract the html from json file.
        '''
        with open(doc_name) as json_file:
            data = json.load(json_file)
            url = data["url"]
            content = data["content"]
            return url, content
    

    def _save_url(self, url : str):
        '''
        Save the document id and url into the urls database.
        '''

        self.id += 1
        self.urls[str(self.id)] = url
        self.urls.sync()
    
    def _clean_text(self, content):
        '''
        Return the text of the html.
        '''

        soup = bs4.BeautifulSoup(content, features="lxml")
        for s in soup(['script', 'style']):
            s.decompose()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        blanks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(blank for blank in blanks if blank)

        return text

    def add(self, name):
        '''
        Tokenize and add a text to index.
        '''
        url, content = self._extract_content(name)
        self._save_url(url)
        text = self._clean_text(content)

        for t in self.tokenizer.tokenize(text):
            token = t.lower()
            token = self.stemmer.stem(token)
        
            if not token in self.index:
                self.index[token] = PriorityQueue()
            self.index[token].add(self.id)
            self.index.sync()

    def close(self):
        '''
        close the database.
        '''

        self.index.close()
        self.urls.close()

if __name__ == "__main__":
    i = Index()
    for document in i.get_document():
        i.add(document)
    i.close()