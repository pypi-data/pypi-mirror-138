#-*- coding: utf-8 -*-
"""
@author:Bengali.ai
"""
#------------------------------------------------------------
from __future__ import print_function
#------------------------------------------------------------
from indicparser import graphemeParser
from indicparser import languages

for language in languages.keys():
    vocab_text=f"vocab/{language}.txt"
    gp=graphemeParser(language)

    with open(vocab_text,"r") as f:
        lines=f.readlines()
    words=[]
    for line in lines:
        if line.strip():
            words.append(line.strip())
    print(f"# Found {len(words)} words for {language} in {vocab_text}")
    #grapheme wrong reconstuction check
    wrong=0
    for word in words:
        try:
            graphemes=gp.process(str(word))
            res="".join(graphemes)
            if word!=res:
                wrong+=1
                print(word,res)
        except Exception as e:
            print(word)
    if wrong>0:
        print(f"wrong reconstruction of {wrong} words for graphemes")
    else:
        print("#------------------------grapheme parsing accuracy:100%-----------------")
    # component wrong reconstuction check
    wrong=0
    for word in words:
        try:
            components=gp.process(str(word),return_graphemes=False)
            res="".join(components)
            if word!=res:
                wrong+=1
                print(word,res,gp.process(str(word)),components)
        except Exception as e:
            print(word)
    if wrong>0:
        print(f"#---------------------wrong reconstruction of {wrong} words for components")
    else:
        print("#------------------------components parsing accuracy:100%-----------------")