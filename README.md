# A Look Into r/WallStreetBets


## Data set details:
I decided I wanted to take a look at Reddit data; specifically, I wanted to take a look at the subreddit [r/WallStreetBets](https://www.reddit.com/r/wallstreetbets/). Having some difficulty with using a web parser, I decided to go with a dataset I ended up finding on [Kaggle](https://www.kaggle.com/gpreda/reddit-wallstreetsbets-posts) with a person who was able to collect the data using Reddit's API. The data came in a CSV format and included values such as the post title, number of upvotes (or the score), the url, the number of comments, the content in the body, and when the content was posted. As you can see from the first 20 rows from the original data set, there is a lot of data to parse through and a lot of unnecessary information. The first task was getting rid of all the emojis in the title and body because Excel could not parse/understand the data and instead returned unconventional characters. To accomplish that, I used a regex expression:

'''python
def strip_emoji(text):
    RE_EMOJI = re.compile(
        u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    return RE_EMOJI.sub(r'', text)
'''

Here, my goal was to use pattern matching to find any emojis that could exist in the text and "substitute" it out with an empty string.I also imported the emoji module to count how many emojis were in each post's title, dividing by 4 because of my nested for loop quadrupling the results. Once I got the emojis out, I moved on to "deleting" the columns; in reality, that was just me excluding the columns from when I wrote the data into the file. Specifically, I nixed the ID, URL, and CREATED columns because the information was pretty irrelevant. Note, the two columns added to this CSV were number of emojis in title and the number of words in each title (set this up with a counter variable for each line). This allowed me to create my first CSV, [clean_data.csv](./clean_data.csv). 

The next CSV I created was [clean_data_wordcounts.csv](./clean_data_wordcounts.csv) which included the count of every word that appeared in the text EXCLUDING stopwords such as "it," "the," and "they." However, I also ran into an issue there; specifically, words were not being counted as the same due to extra punctuation being added at the end. For example, "money" and "money!" would not be counted as the same. Instead their values would be stored seperately. So, I used regex again, but this time to strip my data of punctuation, URLS, and any extra whitespaces. See the following code:

'''python
#strip punctuation
twl[i] = re.sub(r'[^\w\s]', '', twl[i])
#strip websites
twl[i] = re.sub("https*\S+", " ", twl[i])
#strip white space
twl[i] = re.sub('\s{2,}', " ", twl[i])
'''

To get the counts of each word, I stored each word and it's value in a dictionary. I had one for the title words and one for the body words. After, I combined the two dictionaries with their keys and values using the following code:

'''python
#combine dictionaries to form all words
WORDS = {}
WORDS.update(titlewordsdict)
for key, value in bodywords.items():
    if key in WORDS:
        WORDS[key] += value
    else:
        WORDS.update({key: value})
'''

This allowed me to prevent repeats.

The next CSV I created was [clean_data_timestamps.csv](./clean_data_timestamps). This goal of this data is to show what words in the title are popular when. To do this, I just parsed through each word in the title and added the timestamp as I parsed through each line of the original CSV. I ended up only parsing the date because the time data wasn't particularly relevant to me. To make sure I separated the time and date data, I used the following code:

'''python
#note:line[7] here means the 7th "column" of the line that the program is parsing through in the original csv
timestamp = line[7].split(" ")        
#write in timestamp data
##parse through title words to assign each one a timestamp
for i in titlewords:
    timestamp_data.write('"' + i.lower() + '"' + ',' + timestamp[0] + "\n")
'''

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

- Describe each of the aggregate statistic you have calculated - include a description of each and describe any insights the statistic shows that may not be obvious to someone just viewing the raw data.
- If using a pivot table for analysis, include a Markdown table showing a sample of the results of the pivot table (no more than 20 rows, please), along with a short description of what the results show and any insights they offer.
- If using a chart for visualization, include the chart image in the report, with a short description of what the image shows and any insights it offers.  See the Markdown guide linked above for details of showing an image.

## Extra-credit
This assignment deserves extra credit because iste numquam eos et repudiandae sint enim. Rerum enim voluptas voluptatem consequuntur. Sed atque deserunt nihil eius neque et provident aspernatur. Incidunt iusto beatae illo minus vel. Quis sint sunt et facilis doloribus eligendi error est. Ipsum similique.
