#INLS 490-172 Project 1 Text Indexing& Boolean Queries Checkpoint #3
#Author：Yaxue Guo March 19, 2018
import re

# Store stopwords in a list
print("Loading stopwords...")
stopword = []
sw = open("stopwords.txt", "r")
for aline in sw:
    value = aline.split('\n')
    stopword.append(value[0])
print(stopword,'\n')

# Store all words in a list in lowercase without stopwords and special characters
# keep the linenum of titles in a list and keep the linenum & title in a dictionary
# start at line 125 and ends at line 9208, which includes the main story part.
print("Buidling index...")
grimms = open("grimms.txt", "r", encoding='utf8')
allwords = [[]]
linenum = 0
title = {}
startline = 124
finishline = 9209
allwords[linenum] = []

# Use a list to store the original lines for further output use
list_of_lines = []
list_of_lines.append([])

# create the clean words in list of list (according to line number)
for aline in grimms:
    linenum += 1
    list_of_lines.append(aline)
    allwords.append([])
    if linenum <= startline:
        continue
    if linenum >= finishline:
        break
    if aline.isupper():
        if aline[0] not in ('1', '2', '3'):
            title[linenum] = re.sub(r'\\|\n', r'', aline)
    items = aline.split()
    for aword in items:
        aword = aword.lower()
        cleanWord = re.sub(r'[^\w+]', r'', aword)
        if cleanWord not in stopword:
            allwords[linenum].append(cleanWord)

# index words in dict of dict. Notice: allwords[[]] index starts from 0.
d = {}
currentStory = ''
linenum = -1
for alist in allwords:
    linenum += 1
    if linenum <= startline:
        continue
    if linenum >= finishline:
        break
    if linenum in title.keys():
        currentStory = title.get(linenum, 'not found')
        continue
    for aword in alist:
        d.setdefault(aword, {}).setdefault(currentStory, []).append(linenum)

index_build = 1
for avalue in title.values():
    print(index_build,' ',avalue)
    index_build += 1

print("\n"+"Welcome to the Grimms' Fairy Tales search system!"+"\n")

#search engine interface
def call_input():
    query = input("Please input the search term：")
    print("query = ",query,'\n')
    query.lower()
    ls_query = query.split()
    
    if len(ls_query) == 1 and ls_query[0] == 'qquit':
        exit()
    elif len(ls_query) == 1:
        one_word(ls_query[0])
    elif len(ls_query) == 3 and ls_query[1] == 'and':
        multi_words(ls_query)
    elif len(ls_query) == 3 and ls_query[1] == 'or':
        a_or_b(ls_query)
    elif len(ls_query) == 3 and ls_query[1] == 'morethan':
        morethan(ls_query)
    elif len(ls_query) == 3 and ls_query[1] == 'near':
        near(ls_query)
    else:
        multi_words(ls_query)
    call_input()
        
def one_word(word):
    if word not in d.keys():
        print('  --')
        return
    dic = d.get(word)
    ls_storyname = list(dic.keys())
    for i in range(0,len(dic)):
        print('  ',ls_storyname[i],'\n')
        for line in dic.get(ls_storyname[i]):
            rep_old = ' ' + word
            rep_new = ' **' +word.upper() +'** '
            print('    ',line,list_of_lines[line].replace(rep_old,rep_new))
            
def a_or_b(lsquery):
    w1 = lsquery[0]
    w2 = lsquery[2]
    if w1 not in d.keys() and w2 not in d.keys():
        print('  --')
        return
    if w1 in d.keys() and w2 not in d.keys():
        print('  ',w2,' not found.\n')
        one_word(w1)
        return
    if w1 not in d.keys() and w2 in d.keys():
        print('  ',w1,' not found.\n')
        one_word(w2)
        return
    
    dic1 = d.get(w1)
    dic2 = d.get(w2)
    story_common = []
    ls_storyname = list(dic1.keys())
    for i in range(0,len(dic1)):
        if ls_storyname[i] in list(dic2.keys()):
            story_common.append(ls_storyname[i])
    if len(story_common) > 0:
        for key in story_common:
            print('  ',key,'\n')
            print('    ',w1,'\n')
            for line in dic1.get(key):
                rep_old = ' ' + w1
                rep_new = ' **' +w1.upper() +'** '
                print('      ',line,list_of_lines[line].replace(rep_old,rep_new))
            print('    ',w2,'\n')
            for line in dic1.get(key):
                rep_old = ' ' + w2
                rep_new = ' **' +w2.upper() +'** '
                print('      ',line,list_of_lines[line].replace(rep_old,rep_new))

    for key in dic1.keys():
        if key not in story_common:
            print('  ',key,'\n')
            print('    ',w1,'\n')
            for line in dic1.get(key):
                rep_old = ' ' + w1
                rep_new = ' **' +w1.upper() +'** '
                print('      ',line,list_of_lines[line].replace(rep_old,rep_new))
            print('    ',w2, '\n', '     --')

    for key in dic2.keys():
        if key not in story_common:
            print('  ',key,'\n')
            print('    ',w2,'\n')
            for line in dic2.get(key):
                rep_old = ' ' + w1
                rep_new = ' **' +w1.upper() +'** '
                print('      ',line,list_of_lines[line].replace(rep_old,rep_new))
            print('    ',w1, '\n', '     --')

def multi_words(lsquery):
    ls = lsquery
    
    if ls[1] == 'and':
        ls.remove(ls[1])
        
    for aword in ls:
        if aword not in d.keys():
            print('  --')
            return
    #find the interaction stories that contains all words
    lsofdic = []
    for aword in ls:
        lsofdic.append(set(d.get(aword).keys()))
    inter = set.intersection(*lsofdic)
    if len(inter) == 0:
        print('  --')
        return
    
    for key in inter:
        print('  ',key,'\n')
        for aword in ls:
            print('    ',aword)
            for line in d.get(aword).get(key):
                rep_old = ' ' + aword
                rep_new = ' **' + aword.upper() +'** '
                print('      ',line,list_of_lines[line].replace(rep_old,rep_new))
       
def morethan(lsquery):
    w1 = lsquery[0]
    w2 = lsquery[2]
    time1 = 0
    if(w1 not in d.keys()):
        print('  --')
        return
    
    if w2.isdigit():
        least_time = int(w2)       
        for akey in d.get(w1):
            for anumber in d[w1].get(akey):
                time1 += 1
            if time1 > least_time:
                print('  ',akey,'\n')
                for line in d.get(w1).get(akey):
                    rep_old = ' ' + w1
                    rep_new = ' **' + w1.upper() +'** '
                    print('    ',line,list_of_lines[line].replace(rep_old,rep_new))
            time1 = 0
    elif type(w2) == str:
        time2 = 0
        if(w2 not in d.keys()):
            print('  --')
            return
        for akey in d.get(w1):
            if akey not in d.get(w2):
                continue
            for anumber in d[w1].get(akey):
                time1 += 1
            for bnumber in d[w2].get(akey):
                time2 += 1
            if time1 > time2:
                print(akey,'\n')
                print('  ',w1,'\n')
                for line in d.get(w1).get(akey):
                    rep_old = ' ' + w1
                    rep_new = ' **' + w1.upper() +'** '
                    print('    ',line,list_of_lines[line].replace(rep_old,rep_new))
                print('  ',w2,'\n')
                for line in d.get(w2).get(akey):
                    rep_old = ' ' + w2
                    rep_new = ' **' + w2.upper() +'** '
                    print('    ',line,list_of_lines[line].replace(rep_old,rep_new))
            else:
                print('  --')
                
def near(lsquery):
    w1 = lsquery[0]
    w2 = lsquery[2]
    if w1 not in d.keys() or w2 not in d.keys():
        print('  --')
        return
    
    lsofdic = []
    for aword in [w1,w2]:
        lsofdic.append(set(d.get(aword).keys()))
    inter = set.intersection(*lsofdic)
    if len(inter) == 0:
        print('  --')
        return   
    for key in inter:
        for avalue in d.get(w1).get(key):
            linenumw2 = d.get(w2).get(key)
            if (avalue+1) in linenumw2:
                print(key,'\n')
                rep_old = ' ' + w1
                rep_new = ' **' + w1.upper() +'** '
                print('    ',avalue,list_of_lines[avalue].replace(rep_old,rep_new))
                rep_old = ' ' + w2
                rep_new = ' **' + w2.upper() +'** '
                print('    ',avalue+1,list_of_lines[avalue+1].replace(rep_old,rep_new))
            elif (avalue-1) in linenumw2:
                print(key,'\n')
                rep_old = ' ' + w1
                rep_new = ' **' + w1.upper() +'** '
                print('    ',avalue,list_of_lines[avalue].replace(rep_old,rep_new))
                rep_old = ' ' + w2
                rep_new = ' **' + w2.upper() +'** '
                print('    ',avalue-1,list_of_lines[avalue-1].replace(rep_old,rep_new))
            elif avalue in linenumw2:
                print(key,'\n')
                rep_old = ' ' + w1
                rep_new = ' **' + w1.upper() +'** '
                print('    ',avalue,list_of_lines[avalue].replace(rep_old,rep_new))
                rep_old = ' ' + w2
                rep_new = ' **' + w2.upper() +'** '
                print('    ',avalue,list_of_lines[avalue].replace(rep_old,rep_new))
            else:
                 print('  --')
                 return 

call_input()



    

    
    


        
    
    
    
    
