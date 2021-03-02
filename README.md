# A Look Into r/WallStreetBets


## Data set details:
I decided I wanted to take a look at Reddit data; specifically, I wanted to take a look at the subreddit [r/WallStreetBets](https://www.reddit.com/r/wallstreetbets/). Having some difficulty with using a web parser, I decided to go with a dataset I ended up finding on [Kaggle](https://www.kaggle.com/gpreda/reddit-wallstreetsbets-posts) with a person who was able to collect the data using Reddit's API. The data came in a CSV format and included values such as the post title, number of upvotes (or the score), the url, the number of comments, the content in the body, and when the content was posted, starting from January 28, 2021. As you can see from the first 20 rows from the original data set, there is a lot of data to parse through and a lot of unnecessary information. The first task was getting rid of all the emojis in the title and body because Excel could not parse/understand the data and instead returned unconventional characters. To accomplish that, I used a regex expression:


    def strip_emoji(text):
        RE_EMOJI = re.compile(
            u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
        return RE_EMOJI.sub(r'', text)


Here, my goal was to use pattern matching to find any emojis that could exist in the text and "substitute" it out with an empty string.I also imported the emoji module to count how many emojis were in each post's title, dividing by 4 because of my nested for loop quadrupling the results. Once I got the emojis out, I moved on to "deleting" the columns; in reality, that was just me excluding the columns from when I wrote the data into the file. Specifically, I nixed the ID, URL, and CREATED columns because the information was pretty irrelevant. Note, the two columns added to this CSV were number of emojis in title and the number of words in each title (set this up with a counter variable for each line). This allowed me to create my first CSV, [clean_data.csv](./clean_data.csv). 

The next CSV I created was [clean_data_wordcounts.csv](./clean_data_wordcounts.csv) which included the count of every word that appeared in the text EXCLUDING stopwords such as "it," "the," and "they." However, I also ran into an issue there; specifically, words were not being counted as the same due to extra punctuation being added at the end. For example, "money" and "money!" would not be counted as the same. Instead their values would be stored seperately. So, I used regex again, but this time to strip my data of punctuation, URLS, and any extra whitespaces. See the following code:


    #strip punctuation
    twl[i] = re.sub(r'[^\w\s]', '', twl[i])
    #strip websites
    twl[i] = re.sub("https*\S+", " ", twl[i])
    #strip white space
    twl[i] = re.sub('\s{2,}', " ", twl[i])


To get the counts of each word, I stored each word and it's value in a dictionary. I had one for the title words and one for the body words. After, I combined the two dictionaries with their keys and values using the following code:


    #combine dictionaries to form all words
    WORDS = {}
    WORDS.update(titlewordsdict)
    for key, value in bodywords.items():
        if key in WORDS:
            WORDS[key] += value
        else:
            WORDS.update({key: value})


This allowed me to prevent repeats.

The next CSV I created was [clean_data_timestamps.csv](./clean_data_timestamps). This goal of this data is to show what words in the title are popular when. To do this, I just parsed through each word in the title and added the timestamp as I parsed through each line of the original CSV. I ended up only parsing the date because the time data wasn't particularly relevant to me. To make sure I separated the time and date data, I used the following code:


    #note:line[7] here means the 7th "column" of the line that the program is parsing through in the original csv
    timestamp = line[7].split(" ")        
    #write in timestamp data
    ##parse through title words to assign each one a timestamp
    for i in titlewords:
        timestamp_data.write('"' + i.lower() + '"' + ',' + timestamp[0] + "\n")


### The Raw Data (First 20 Rows)
NOTE: there's analysis under the table!

title | score | id | url | comms_num | created | body | timestamp
------| ------|----|-----|-----------|---------|------|----------
"It's not about the money, it's about sending a message. 🚀💎🙌"|55|l6ulcx|https://v.redd.it/6j75regs72e61|6|1611862661.0||2021-01-28 21:37:41
Math Professor Scott Steiner says the numbers spell DISASTER for Gamestop shorts|110|l6uibd|https://v.redd.it/ah50lyny62e61|23|1611862330.0||2021-01-28 21:32:10
Exit the system|0|l6uhhn|https://www.reddit.com/r/wallstreetbets/comments/l6uhhn/exit_the_system/|47|1611862235.0|"The CEO of NASDAQ pushed to halt trading “to give investors a chance to recalibrate their positions [https://mobile.twitter.com/Mediaite/status/1354504710695362563](https://mobile.twitter.com/Mediaite/status/1354504710695362563) Now SEC is investigating, brokers are disallowing buying more calls. This is the institutions flat out admitting they will change the rules to bail out the rich but if it happens to us, we get a “well shucks you should have known investing is risky! have you tried cutting out avocados and coffee, maybe doing Uber on the side?” We may have collectively driven up enough sentiment in wall street to make other big players go long on GME with us (we do not have the money to move the stock as much as it did alone). we didn’t hurt wall street as a whole, just a few funds went down while others went up and profited off the shorts the same as us. The media wants to pin the blame on us.It should be crystal clear that this is a rigged game by now. Its time to build new exchanges that can’t arbitrarily change the rules on us. Cr\*\*o has some version of these, maybe they can be repurposed to be trade stock without government intervention. I don’t know exactly what it will look like yet, but the broad next steps i see are - 1. exit the current financial system 2. build a new one."|2021-01-28 21:30:35
NEW SEC FILING FOR GME! CAN SOMEONE LESS RETARDED THAN ME PLEASE INTERPRET?|29|l6ugk6|https://sec.report/Document/0001193125-21-019848/|74|1611862137.0||2021-01-28 21:28:57
"Not to distract from GME, just thought our AMC brothers should be aware of this"|71|l6ufgy|https://i.redd.it/4h2sukb662e61.jpg|156|1611862016.0||2021-01-28 21:26:56
WE BREAKING THROUGH|405|l6uf7d|https://i.redd.it/2wef8tc062e61.png|84|1611861990.0||2021-01-28 21:26:30
SHORT STOCK DOESN'T HAVE AN EXPIRATION DATE|317|l6uf6d|https://www.reddit.com/r/wallstreetbets/comments/l6uf6d/short_stock_doesnt_have_an_expiration_date/|53|1611861987.0|"Hedgefund whales are spreading disinfo saying Friday is make-or-break for $GME. Call options expiring ITM on Friday will drive the price up if levels are maintained, but may not trigger the short squeeze.It may be Friday, but it could be next week the we see the real squeeze.DON'T PANIC IF THE SQUEEZE DOESN'T HAPPEN FRIDAY.It's not guaranteed to. The only thing that is guaranteed mathematically is that the shorts will have to cover at some point in the future. They are trying to get enough people hooked on the false expectation of Friday so that if/when it doesn't happen, enough will sell out of panic/despair. DON'T BE THAT PERSON.WE LIKE THE STOCK"|2021-01-28 21:26:27
THIS IS THE MOMENT|405|l6ub9l|https://www.reddit.com/r/wallstreetbets/comments/l6ub9l/this_is_the_moment/|178|1611861571.0|"Life isn't fair. My mother always told me that when I would complain about arbitrary treatment. I would play by the rules and someone else would ignore them. When they would win I would appeal to the first authority for an explanation. ""Are you going to let them get away with this""? ""Life isn't fair"". No, it is not. The game is the game. Always.In this moment, the fascade cracks further. When the first breach was made I do not know, perhaps it was Socrates, but today I see thousands. Millions. Once they were laughing, luxuries falling out of their disgusting diseased mouths as they cackled. The unmistakable stench of derision carried on their breath. They told anyone outside of their elite class that we were fools for even trying. They told us that we were naive. We needed networks to be successful. We needed polish. We needed expertise. We needed THEM. The game is the game. Always. They are no longer laughing. Their odious oeuvre still wafts through the air. While the rot, and hate, and condescention, remains, the noxious air betrays a new addition. Something all together disconcerting. What it betrays, is fear. They are afraid. And they should be. We do not need their inherited resources masked as acumen. A new day dawns. The day where we make an ever so slight step towards what they fear the most. An even field. Life becoming ever so slighty more fair.   AND. THEY. ARE. SCARED. They look at us and see roughness. We look at them and see softness. We are both correct in our estimation.The game is the game. Always.Fuck them in the street. Fuck them all in the street. We are the righteous. We are blessed by Phoebe. What started here will echo through time in the eons to come. Mount up and ride with the fury of a thousand rockets into the universal filament. May the wind always be at your back and the sun upon your face. And may the wings of destiny carry you aloft, to dance with the stars.GME@everything BB@everything🚀🚀🚀🚀🚀🚀🚀"|2021-01-28 21:19:31
Currently Holding AMC and NOK - Is it retarded that I think I should move it all to GME today?|200|l6ub4i|https://i.redd.it/6k2z7ouo42e61.png|161|1611861556.0||2021-01-28 21:19:16
I have nothing to say but BRUH I am speechless TO THE MOON 🚀🚀🚀💎💎👋👋|291|l6uas9|https://i.redd.it/bfzzw2yo42e61.jpg|27|1611861517.0||2021-01-28 21:18:37
"We need to keep this movement going, we all can make history!"|222|l6uao1|https://www.reddit.com/r/wallstreetbets/comments/l6uao1/we_need_to_keep_this_movement_going_we_all_can/|70|1611861505.0|" I believe right now is one of those rare opportunities that we all can help and do good. Some of these companies like GME, AMC are good companies that's been hit hard by this pandemic. Hedgefunds and Wallstreet just want to short these companies to zero and make millions. I really think right now we have enough support and enough of us to change that direction in history. Wallstreet says  well weak companies need to just go. 10 yrs down the road though I want to be able to watch a movie in a movie theater with my family. If we all buy and hold in what we believe in it gives these companies a second chance and we as a group can stop these companies from being shorted to death and just disappear. Just my 2 cents!"|2021-01-28 21:18:25
GME Premarket 🍁 Musk approved 🎮🛑💎✋|562|l6ua2q|https://i.redd.it/48rmgz5c42e61.png|97|1611861448.0||2021-01-28 21:17:28
Technical Analysis of GameStop ($GME) - TO THE MOON 🚀🚀🚀🚀🌚🌚🌚|324|l6ttk8|https://youtu.be/idbOOXFZnO4/|117|1611859696.0||2021-01-28 20:48:16
Really? I can’t even buy GME or AMC for now? 😤|606|l6tt3i|https://i.redd.it/mvfo6m14z1e61.jpg|376|1611859640.0||2021-01-28 20:47:20
I’ve got a friend who is all in on GME 🚀💎🙌🏼|261|l6tsx4|https://i.redd.it/hgrgffo1z1e61.jpg|43|1611859618.0||2021-01-28 20:46:58
Y'all broke it. How do we fix it? Any advice?|73|l6tqpv|https://i.redd.it/3if77nnay1e61.png|140|1611859366.0||2021-01-28 20:42:46
JUST PUT IN ANOTHER 30K IN NOK CALLS LET'S GO! $GME $NOK BUY AND HOLD 🚀🚀 🚀🚀|223|l6tpdl|https://i.redd.it/01jehyrnx1e61.png|146|1611859207.0||2021-01-28 20:40:07
"It ain’t much, but I’m in! From Germany to the moon ! 🚀🚀"|743|l6tocg|https://i.redd.it/oiqj3jbgx1e61.jpg|169|1611859083.0||2021-01-28 20:38:03
Are we ready to attack the Citadel !!!!|152|l6to43|https://www.reddit.com/r/wallstreetbets/comments/l6to43/are_we_ready_to_attack_the_citadel/|32|1611859056.0|https://youtu.be/BtjhgcAMYU0|2021-01-28 20:37:36
"Another devastating hit, Europoors using Trading212 can have their positions closed anytime. No new positions as well😤😤 We will HOLD as long as we can!🚀🚀"|788|l6tlew|https://i.redd.it/boaoxc3gw1e61.jpg|467|1611858745.0||2021-01-28 20:32:25
$GME back up to ~350USD after hours|304|l6tkvw|https://i.redd.it/tlb66b19w1e61.jpg|131|1611858679.0||2021-01-28 20:31:19


## Analysis:
Let's break down the data starting with an overview from [clean_data.csv](./clean_data.csv).

Beginning with the average number of comments per post, the calculated mean was 164.866046. This means in a normal distribution, on average, a post can be expected to have approximately 164 comments. However, we should note, that there is a significant possibility of the data being skewed indicated by the fact that the highest number of upvotes a post has had is 348241 while the lowest is 0 and the most common is 1. With such a wide range of results, I decided to dig deeper into what was the most likely cause for the data being skewed; specifically the number of upvotes, or the SCORE.

The overall average upvote per post, without picking apart the data is 1224.9977. This means that for any Reddit post on r/WallStreetBets you can expect 1224 unqiue IDs (people) to have upvoted the post. Or can you? 75% of the posts (or 27411 out of 36520 posts) have either 138 upvotes or below. Compared to the mean, this is a SIGNIFICANT drop by approximately 1100 upvotes. Therefore, I decided to calculate the averages of the bottom 75% and the top 25%. For the bottom 75%, we recieve an average of 21.56874977, meaning per post, the bottom 75% can expect to get an average of 21 upvotes per post. For the top 25% however, we calculate an average of 4846.38215, meaning per post, the top 25% can expect to recieve 4846 upvotes per post. The difference between these two numbers is approximately 4820 upvotes.

I then decided to take a look at the max number of upvotes per post based on the day they were posted as indicated by the image below.

![clean_data](./images/upvotes_128_21.png)

As you can see, the days after Robinhood closed trading for GME stock on January 28, 2021, the maximum of upvotes per day seemed to grow higher. This may be due to the influx of people who flooded the subreddit after hearing about the chaos on the news. However, come February 1, 2021, there seemed to be a sudden drop in upvotes - this could be due to an anomoly in the on January 31, 2021 where a post caught attention from several other subreddits, news, or social media. Or this could just be an example of where trends quickly come and go. The graph also shows that there is no data included for January 22, 2021. It only begins from January 28, 2021.

There were also some other interesting statistics such as the average number of emojis in a title, 0.713964951 (approximately 1 per post due to the popular use of the rocket emoji to symbolize the phrase "to the moon"), and the average title length, 10.84008762 (meaning approximately 10 words per title).

See below a condensed version of the data mentioned above.

As for the pivot table included with this data, I am unable to provide a condensed version of said table due to the fact that it has thousands of rows and columns. Please view [clean_data.csv](./clean_data.csv) to see the pivot table. The rows in the pivot table are sorted by score, while the columns are calculated by number of comments. The pivot table provides the average number of emojis per post, the length of the title per post, and number of posts (indicated by count of timestamps) based on number of upvotes and number of comments. This helps indicate what are the most popularly recvieved posts.

### Statistics Calculated

type of statistic | calculated 
------------------|-----------
AVERAGE OF COMMENTS	| 164.866046
AVERAGE OF SCORE | 1224.9977
MODE OF SCORES | 1
MAX OF SCORES | 348241
MIN OF SCORES | 0
QUARTILE 75 | 138
COUNTIF SCORE <= 138 | 27411
AVERAGEIF SCORE > 138 | 4846.38215
DAVERAGE OF SCORE IF SCORE <= 138 | 21.56874977
MAXIF SCORE DATE 1/22/21 (DATA NOT INCLUDED) | 0
MAXIF SCORE DATE 1/28/21 (ROBINHOOD LIMITED USERS) | 160999
MAXIF SCORE DATE 1/29/21 | 225870
MAXIF SCORE DATE 1/30/21 | 219779
MAXIF SCORE DATE 1/31/21 | 348241
MAXIF SCORE DATE 2/1/21 | 171545
AVERAGE OF EMOJI COUNT | 0.713964951
AVERAGE OF TITLE LENGTH | 10.84008762


Now, let's look at [clean_data_timestamps.csv](./clean_data_timestamps). Due to the nature of using Excel, I was unable to conduct the NLP tests I desired, but I was able to observe some interesting trends regardless. Note: I did not choose to exclude the stopwords here due to use of data for future analysis at a later date. Now moving forward, the most commonly referenced word was "the." 

Looking at the graph, the number of words based on each date seemed to peak on January 29, 2021 (as indicated in the graph below); however there was a jump on February 3, 2021. The peak on January 29 can be due to the fact that RobinHood closed trading the day before on January 28. The sudden peak on February 3 may be due to an influx of bots spamming the subreddit. 

![timestamp_chart](./images/timestamp_titlewords.png)

See below a condensed version of the data mentioned above.

The pivot chart shows the words and how many times it appears in each month. Because of the sheer amount of data, not all the words are able to be seen on one chart alone; however, we do see some spikes such as "GME" peaking in January, "a" peaking in February, and "the" peaking in January. Note: the pivot chart reinforces earlier claims about "the" being the most popular word.

![timestamp_pivot](./images/timestamp_titleword_pivotcahrt.png)

The pivot table the chart was derived from is indicated below, showing the most popular words based on their appearence in each month. 

### Pivot Table 

words| jan | feb | grand total	
-----|-----|-----|------------			
0 | 28 | 39 | 67
1 | 186 | 155 | 341
2 | 105 | 201 | 306
3 | 60 | 107 | 167
4 | 48 | 72 | 120
5 | 66 | 85 | 151
6 | 24 | 43 | 67
7 | 26 | 35 | 61
8 | 20 | 40 | 60
9 | 15 | 37 | 52
10 | 54 | 91 | 145

### Statistics Calculated

type of statistic | calculated 
------------------|-----------
MODE | the
COUNTIF JAN28 | 12387
COUNTIF JAN29 | 159938
COUNTIF JAN30 | 17363
COUNTIF JAN31 | 11903
COUNTIF FEB1 | 11630
COUNTIF FEB2 | 18777
COUNTIF FEB3 | 31834
COUNTIF FEB4 | 17863

And the last CSV to observe is [clean_data_wordcounts.csv](./clean_data_wordcounts.csv). This is the CSV where the number of counts have been calculated based on how often a word appears on the subreddit. As we can see, we have 1626135 words from the span of January 28, 2021, to when the data was exported on February 26, 2021. On average , there are approximately 15 (calculated average is 15.86968615) instances of each word (not including stop words); however, the median is 1, meaning that the middle value of the number of instances per word is 1. Given that there is a pretty large difference between the average and the median, this means the data is most likely skewed. This is reinforced by the standard deviation which is 167.298439. This means the values of the count tend to be farther away from the calculated average. Given that the data is pretty skewed, I wanted to see what was the most popular and the least popular term. GME was the most popular term with 17691 counts while steiner was the least popular with 1 count. However, note that there are several terms with a count of 1; the spreadsheet returned the most recent value in the table. I also decided to calculate how many words had one instance and how many words had 15 instances. I got 67582 and 4516 words respectively. I then wanted to see how many words existed that had some variation of game within it (game*) and I found out there were 182 counts. This may occur because of spelling errors or compound words, but I thought it was interesting to see how many variations for the word game occured.

See below a condensed version of the data mentioned above.

The pivot chart shows the words and the number of times it appears. As we can see, GME is the most popular term, reinforcing the statistical analysis conducted earlier.

![wordcount_total](./images/wordcount_total_pivotchart.png)

The pivot table the chart was derived from is indicated below, showing the most popular words to the least popular words. 

### Pivot Table 


word | count
-----|------
gme | 17691
buy | 10558
stock | 10181
shares | 9238
like | 9132
im | 8785
short | 8176
dont | 8171
market | 8151
hold | 7511
get | 7142
people | 7068
price | 6896
robinhood | 6857
money | 6641

### Statistics Calculated

type of statistic | calculated 
------------------|-----------
SUM | 1626135	
AVERAGE | 15.86968615	
MEDIAN | 1	
MAX | 17691(gme)
MIN	| 1(steiner)
STD | 167.298439	
SUMIF (all counts = 1) | 67582
SUMIF (all counts approx. avg 15) | 4516
COUNTIF (game*) | 182
