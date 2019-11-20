import PartA,PartB
import os
import nltk
from pathlib import Path
import json
from lxml import html
import lxml
from io import StringIO, BytesIO
from nltk import PorterStemmer
from collections import defaultdict
# from nltk.tokenize import word_tokenize
string_1=",!:.?''/`{};[]@#$%^&*()-=+_"
string_2="                           "
test_line = " Hello world, this is +He."
table = test_line.maketrans(string_1,string_2)
new_test_line = test_line.translate(table)
new_list = [token.lower() for token in new_test_line.split()]
# print(new_list)
inverted_index = defaultdict(list)
list_dir=os.listdir("developer/DEV")
list_dir=sorted(list_dir)


id = 0
files = sorted(os.listdir("developer/DEV/"+list_dir[0]))
f=open("idToIndex.txt","w")
for each_sub in list_dir:
    for each_json in sorted(os.listdir("developer/DEV/"+each_sub)):
        with open("developer/DEV/"+each_sub+"/"+each_json, encoding ="utf-8") as read_file:
            stemProcesser = PorterStemmer()
            data = json.load(read_file)
            data_content = data["content"]
            data_content = data_content.encode("utf-8","ignore") 
            try:
                html = lxml.html.fromstring(data_content)
                parse_html_content = html.text_content()
                token_list = []

                parse_html_content = parse_html_content.translate(table)

                parse_html_split = parse_html_content.rsplit()

                new_list = [token for token in parse_html_split if token.isascii()]  #list of token

                after_stem = []

                for word in new_list: #stem processing
                    after_stem.append(stemProcesser.stem(word))
                    #print(after_stem)
                for token in after_stem:
                    if(inverted_index.get(token)==None):
                        inverted_index[token].append((id,1))
                #        print(token,id)
                    else:
                        if(inverted_index[token][-1][0]!=id):
                            inverted_index[token].append((id,1))
                            #print(token+": old token exit in new file")
                        else:
                            inverted_index[token][-1] = (inverted_index[token][-1][0],inverted_index[token][-1][1]+1)
                            #print(token,inverted_index[token])
                f.write(str(id)+" "+data["url"]+"\n")
                id+=1

            except(lxml.etree.ParserError):
                #print("developer/DEV/"+each_sub+"/"+each_json+" has empty content")
                #print(data_content)
                #print("-------------")
                pass
                
            #token_list = []
    
            #parse_html_content = parse_html_content.translate(table)

            #parse_html_split = parse_html_content.rsplit()

            #new_list = [token for token in parse_html_split if token.isascii()]  #list of token

            #after_stem = []

            #for word in new_list: #stem processing
            #    after_stem.append(stemProcesser.stem(word))
            #    #print(after_stem) 
            #for token in after_stem:
            #    if(inverted_index.get(token)==None):
            #        inverted_index[token].append((id,1))
            #        print(token,id)
            #    else:
            #        if(inverted_index[token][-1][0]!=id):
            #            inverted_index[token].append((id,1))
            #            #print(token+": old token exit in new file")
            #        else:
            #            inverted_index[token][-1] = (inverted_index[token][-1][0],inverted_index[token][-1][1]+1)
                        #print(token,inverted_index[token])
       # id+=1
f.close()
#num_key = 0
#for key,value in list(inverted_index.items()):
#    print(key,value)
#    num_key+=1
#print(num_key,id)
