# place your code to clean up the data file below.
# make sure modules are all installed
try:
    import csv
    import re
    import emoji
except:
    print("Please make sure you have the following modules installed: csv, re, emoji")
    exit()

# function to strip emoji
def strip_emoji(text):
    RE_EMOJI = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    return RE_EMOJI.sub(r'', text)

# open csv
data = open("data/reddit_wsb.csv", 'r')
# create two new files
## clean_data.csv
new_data = open("clean_data.csv",'w')
## titlewords for time stamp csv
timestamp_data = open("clean_timestamp_titlewords.csv", 'w')
## word count
wordcount_data = open("clean_data_wordcount.csv", 'w')

# create dictionary with titlewords and counts
bodywords = {}
titlewordsdict = {}
emoji_count = 0

# read each line in the csv
for line in csv.reader(data):
    # first line must write header
    if line[0] == 'title':
        new_data.write("title,score,comms_num,timestamp,emoji_exists\n")
        timestamp_data.write("words,timestamp\n")
        wordcount_data.write("word,count\n")
    # every other line
    else: 
        # title 0,score 1,id 2,url 3,comms_num 4,created 5,body 6,timestamp7

        # clean up the title and get the words in the title
        twl = line[0].split(" ")
        titlewords = []

        # clean up the title and remove emojis
        for i in range(len(twl)):
            for emo in emoji.UNICODE_EMOJI.values():
                for j in twl[i]:
                    if j in emo:
                        emoji_count += 1
            if (emoji_count / 4 % 2) != 0:
                emoji_count = (emoji_count // 4) + 1
            else:
                emoji_count = (emoji_count / 4)
            twl[i] = strip_emoji(twl[i])
            twl[i] = re.sub(r'[^\w\s]', '', twl[i])
            twl[i] = re.sub("https*\S+", " ", twl[i])
            twl[i] = re.sub('\s{2,}', " ", twl[i])
            titlewords.append(twl[i])
            if twl[i].lower() in titlewordsdict:
                try:
                    titlewordsdict[twl[i].lower()] += 1
                except:
                    continue
            else:
                try:
                    
                    titlewordsdict.update({twl[i].lower(): 1})
                except:
                    continue

        
        # look at the words in the body
        bwl = line[6].split(" ")
        
        for i in range(len(bwl)):
            bwl[i] = re.sub(r'[^\w\s]', '', bwl[i])
            bwl[i] = re.sub("https*\S+", " ", bwl[i])
            bwl[i] = re.sub('\s{2,}', " ", bwl[i])
            bwl[i] = strip_emoji(bwl[i])
            if bwl[i].lower() in bodywords:
                try:
                    bodywords[bwl[i].lower()] += 1
                except:
                    continue
            else:
                try:
                    bodywords.update({bwl[i].lower(): 1})
                except:
                    continue

        title = ' '.join(titlewords)
        # data with title, time stamps, comments, score, and emoji count
        new_data.write('"'+title +'"'+ ','+ line [1] + ','+ line[4]+','+ line[7] + ',' +str(emoji_count) + "\n")
        for i in titlewords:
            timestamp_data.write('"' + i.lower() + '"' + ','+ line[7] +"\n")
        emoji_count = 0

#combine dictionaries to form all words
WORDS = {}
WORDS.update(titlewordsdict)
for key, value in bodywords.items():
    if key in WORDS:
        WORDS[key] += value
    else: 
        WORDS.update({key : value})

copy = WORDS.copy()

s = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
other = ['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once']
for i in other:
    if i not in s:
        s.append(i)
    #s.add(i)
    
for key in copy.keys():
    for value in s:
        try:
            if key == value:
                del WORDS[key]
        except:
            print("skipping", key)

for key, value in WORDS.items():
    wordcount_data.write('"'+ key+ '"' + "," + str(value) + "\n")

#print(titlewordsdict)
# get rid of ID column 

# parse through date and titles + body columns
## take out 100 most commonly used titlewords

# close files
new_data.close()
wordcount_data.close()
timestamp_data.close()
