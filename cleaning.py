import os, pylab as pl, pandas as pd
from datetime import datetime
from lib import helper, graphs as g
from progress.bar import ChargingBar

KEYWORD1 = input()
KEYWORD2 = input()
SINCE   = input()
UNTIL   = input()
DBName  = input()
COUNTRY = input()
CACHE   = bool(input())
PORT    = int(input())
# BASE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
BASE_DATE_FORMAT = '%a %b %d %H:%M:%S %z %Y'

print('Loading variables ...')
variables  = helper.get_variables('config/variables.yml')
# -----------------------------------------------------------------------------
figpath = 'app/output/'+DBName
if not os.path.exists(figpath) and not os.path.isdir(figpath):
    print('Creating Plots Folder ...')
    os.mkdir(figpath)
# -----------------------------------------------------------------------------
print('Loading xlsx output file ...')
xlsx = pd.ExcelFile('app/output/'+DBName+'/'+DBName+'.xlsx')
df = pd.read_excel(xlsx, 'DATA')
# -------- Drop Unwanted Columns -----------------
df.drop(variables['dropable'], axis=1, inplace=True)
# ------------ Generate the graphs --------------
print('Generating graphs...')
tweet = df['text'].value_counts()
same_tweets = tweet.apply(lambda x: 1 if x>1 else 0).sum()
indv_tweets = len(tweet.index)-same_tweets
legend_labels = ['Same tweets       - '+str(same_tweets),
                 'Independent tweet - '+str(indv_tweets)]
indexes = [i for i in df.index if df.loc[i,'text']==tweet.idxmax() ]
isRT = ['Retweet' if text[:3]=='RT ' else 'Individual' for text in df['text']]
isRT = pd.Series(isRT).value_counts()
xlabs = ['Individual', 'Retweet']
xvals = [isRT['Individual'], isRT['Retweet']]
legend_labels = [ 'Retweet - '+str(xvals[1]),
                  'Individual - '+str(xvals[0]) ]
bar = ChargingBar('Processing', max=12)
bar.start()
# -----------------------------------------------------------------------------
# Analysis of Number of Retweets in the Data...
# Fig. 1.1
# ------------- Histogram ------------------
g.Hist(df,colname='text',
        xlabel='Text', ylabel='Frequency of each tweet',
        title='Histogram for frequency of tweets',
        figpath=figpath+'/Fig-1.1.png',
        legend=legend_labels)
bar.next()
# --------------------------------------------
# Fig. 1.2
# ------------- Bar Plot  ------------------
pl.figure()
pl.bar(range(len(xlabs)), xvals, align='center', width=0.1, color=['steelblue', 'crimson'])
pl.xticks(range(len(xlabs)), xlabs)
pl.xlabel('Retweets and Individual Tweets')
pl.ylabel('Frequency')
pl.title('Text Comparision - Individual and Re-Tweets')
pl.legend(handles=g.patches(legend_labels),prop={'size':10})
pl.savefig(figpath+'/Fig-1.2.png')
# pl.show()
pl.close()
bar.next()
# ----------------------------------------
# Analysis of Location w.r.t to tweets
# ----- Fig. 1.3 Box Plot  ---------------
g.Boxp(df,colname='subdivision',
        xlabel='Frequency', ylabel='Places',
        title='Boxplot of tweets frequency \nfrom various places in '+COUNTRY,
        figpath=figpath+'/Fig-1.3.png')
bar.next()
# ----- Fig. 1.4 Horizontal Bar Plot  ----
g.HBar(df,colname='subdivision',
        xlabel='Frequency', ylabel='Places',
        title='Frequency distribution tweets in '+COUNTRY,
        figpath=figpath+'/Fig-1.4.png')
bar.next()
# ----- Fig. 1.5 Histogram ---------------
g.Hist(df,colname='subdivision',
        xlabel='Places', ylabel='No. of tweets',
        title='Histogram for tweets Frequency w.r.t places',
        figpath=figpath+'/Fig-1.5.png')
bar.next()
# ----------------------------------------
# Analysis of Sources w.r.t tweets
# ----- Fig. 1.6 Box plot ----------------
g.Boxp(df,colname='source',
        xlabel='Frequency', ylabel='Sources',
        title='Boxplot of tweets frequency \nfrom various sources',
        figpath=figpath+'/Fig-1.6.png')
bar.next()
# ----- Fig. 1.7 Horizontal Bar plot -----
g.HBar(df,colname='source',
        xlabel='Frequency', ylabel='Sources',
        title='Frequency distribution sources of tweets',
        figpath=figpath+'/Fig-1.7.png')
bar.next()
# ----- Fig. 1.8 Histogram ---------------
g.Hist(df,colname='source',
        xlabel='Sources', ylabel='No. of tweets',
        title='Histogram for tweets Frequency w.r.t sources',
        figpath=figpath+'/Fig-1.8.png')
bar.next()
# ----------------------------------------
# Analysis of Users w.r.t to tweets
# ----- Fig. 1.9 Box plot ----------------
g.Boxp(df,colname='screen_name',
        xlabel='Frequency', ylabel='Users',
        title='Boxplot of users frequencies \n of tweets',
        figpath=figpath+'/Fig-1.9.png')
bar.next()
# ----- Fig. 1.10 Horizontal Bar plot -----
g.HBar(df,colname='screen_name',
        xlabel='Frequency', ylabel='Users',
        title='Frequency distribution user\'s tweets',
        figpath=figpath+'/Fig-1.10.png')
bar.next()
# ----- Fig. 1.11 Histogram ---------------
g.Hist(df,colname='screen_name',
        xlabel='users', ylabel='No. of tweets',
        title='Histogram for users tweeting Frequency',
        figpath=figpath+'/Fig-1.11.png')
bar.next()
# ------------------------------------------------------------------------------
# -------- Recode the response variable -----------
df[variables['response']] = df[variables['response']].apply(lambda x: 0 if helper.containsAny(KEYWORD1, x) else 1)
# --------- Fig.1.12 Time Series Graph  ----------
df['created_at'] = df['created_at'].apply(lambda x: datetime.strptime(x, BASE_DATE_FORMAT))
df.set_index(df['created_at'], inplace=True)
df['created_at'] = df['created_at'].apply(lambda x: datetime.strftime(x, BASE_DATE_FORMAT))
pl.figure()
pl.ylim([-1,2])
locs, labels = pl.yticks([0,1], [KEYWORD1, KEYWORD2])
pl.setp(labels, size=8)
df['text'].plot()
pl.title('Conversation on '+KEYWORD1+' and '+KEYWORD2+' over the period of time')
pl.xlabel('Tweet Creation Date')
pl.ylabel('Tweet Talks About ...')
# pl.show()
pl.savefig(figpath+'/Fig-1.12.png')
pl.close()
bar.next()
df.reset_index(drop=True, inplace=True)
bar.finish()
print('Reducing factor levels for multi_factor columns...')
# -------- Reducing factor levels for multi_factor columns -------
for col in variables['multi_factors']:
    freq = df[col].value_counts()
    newlabel = COUNTRY if col=='subdivision' else 'others'
    df[col] = df[col].apply(lambda x: newlabel if x not in freq[:6] else x)
print('Breaking the time series data into multiple columns...')
# -------- Break the Time data into multiple columns -------------
for col in variables['time_series']:
    df[col] = df[col].apply(lambda x: datetime.strptime(x, BASE_DATE_FORMAT).strftime(format='%d-%m-%Y %H:%M:%S'))
    day, mon, yr = df[col].str[:2], df[col].str[3:5], df[col].str[6:10]
    hr, mi, se = df[col].str[11:13],df[col].str[14:16],df[col].str[17:19]
    timeDF = pd.DataFrame({ 'day' : day, 'mon' : mon, 'year': yr,
                            'hrs' : hr , 'mins': mi , 'secs': se }, columns=['day','mon','year','hrs','mins','secs'])
    timeDF.rename(columns=lambda x : col+'_'+x, inplace=True)
    timeDF = timeDF.astype(int)
    df = pd.concat([df, timeDF], axis=1)
df.drop(variables['time_series'], axis=1, inplace=True)
variables['time_series'] = [ col+suffix for col in variables['time_series'] for suffix in ['_day','_mon','_year','_hrs','_mins','_secs'] ]
# ----------------------------------------
df['contributors_enabled'] = df['contributors_enabled'].astype(str)
print('Saving the cleaned dataset ...')
df = df.loc[:, (df != 0).any(axis=0)]
df.dropna(axis=1, how='all', inplace=True)
df.drop_duplicates(inplace=True)
df.to_excel(figpath+'/'+DBName+'_clean.xlsx', sheet_name='DATA', index=False)
# -----------------------------------------------------------------------------
print('Initiallising the report markdown file ...')
reportpath = 'output/'+DBName
report = open(figpath+'/'+DBName+'_report1.md','w')
print('Generating Report ...')
sub_freq = df['subdivision'].value_counts()
sub_labs = sub_freq.index.values[:4]
sub_labs = [l for l in sub_labs if l.lower()!=COUNTRY.lower()]
sub_vals = pd.Series(sub_freq.values)

src_freq = df['source'].value_counts()
src_labs = src_freq.index.values[:3]
src_labs = [l.lower().replace('twitter','').replace('for','').lstrip().rstrip() for l in src_labs]
src_vals = pd.Series(src_freq.values)

scr_name_freq = df['screen_name'].value_counts()
scr_name_labs = scr_name_freq.index.values[:3]
scr_name_vals = pd.Series(scr_name_freq.values)

report.write('''
<center>![Histogram for frequency of tweets](http://localhost:8080/'''+reportpath+'''/Fig-1.1.png "Histogram for frequency of tweets")</center>
<center><sub>Fig 1.1 Histogram for frequency of tweets</sub></center>

From the figure 1.1 it can be seen that the number of unique tweets from the
downloaded set of tweets is '''+str(indv_tweets)+''' where as the number of
tweets that appear to be same are '''+str(same_tweets)+'''. It can also be noted
that the few of the tweets are retweeted more than the others with the tweet
__"'''+tweet.idxmax()+'''"__
being tweeted the most and appears in the dataset at indexes
'''+str(indexes)[1:-1]+''' from the users
__'''+str(set(df.ix[indexes,'screen_name']))[1:-1]+'''__

<center>![Text Comparision - Individual and Re-Tweets](http://localhost:8080/'''+reportpath+'''/Fig-1.2.png "Text Comparision - Individual and Re-Tweets")</center>
<center><sub>Fig 1.2 Text Comparision - Individual and Re-Tweets</sub></center>

The figure 1.2 shows the number of tweets that contains 'RT ' in front of the
given text and those that do not contain it. From the frequency plot it can be seen
that the number of individual tweets is '''+str(xvals[0])+''' and number of
re-tweets is '''+str(xvals[1])+''' in count.

The following graphs show the analysis of tweets according to the locations. It
might be considered as a good metric to identify people from which places tend to
vote more than others.

<center>![Boxplot of tweets frequency from various places in '''+COUNTRY+'''](http://localhost:8080/'''+reportpath+'''/Fig-1.3.png "Boxplot of tweets frequency from various places in '''+COUNTRY+'''")</center>
<center><sub>Fig 1.3 Boxplot of tweets frequency from various places in '''+COUNTRY+'''</sub></center>

<center>![Frequency distribution tweets in '''+COUNTRY+'''](http://localhost:8080/'''+reportpath+'''/Fig-1.4.png "Frequency distribution tweets in '''+COUNTRY+'''")</center>
<center><sub>Fig 1.4 Frequency distribution tweets in '''+COUNTRY+'''</sub></center>

<center>![Histogram for tweets Frequency w.r.t places](http://localhost:8080/'''+reportpath+'''/Fig-1.5.png "Histogram for tweets Frequency w.r.t places")</center>
<center><sub>Fig 1.5 Histogram for tweets Frequency w.r.t places</sub></center>

The figure 1.3, 1.4 and 1.5 it is clear that people from __'''+', '.join(sub_labs)+'''__ tend to
tweet more than any other places. From the boxplot it is clear that the data is
''')
report.write('skewed.' if sub_vals.max() > sub_vals.quantile(.75)*1.5 else 'not skewed.')

report.write('''
The following graphs show the analysis of tweets according to the sources or the devices used
for tweeting. It is interesting to see which voters tend to use a which kind of device.

<center>![Boxplot of tweets frequency from various sources](http://localhost:8080/'''+reportpath+'''/Fig-1.6.png "Boxplot of tweets frequency from various sources")</center>
<center><sub>Fig 1.6 Boxplot of tweets frequency from various sources</sub></center>

<center>![Frequency distribution sources of tweets](http://localhost:8080/'''+reportpath+'''/Fig-1.7.png "Frequency distribution sources of tweets")</center>
<center><sub>Fig 1.7 Frequency distribution sources of tweets</sub></center>

<center>![Histogram for tweets Frequency w.r.t sources](http://localhost:8080/'''+reportpath+'''/Fig-1.8.png "Histogram for tweets Frequency w.r.t sources")</center>
<center><sub>Fig 1.8 Histogram for tweets Frequency w.r.t sources</sub></center>

The figure 1.6, 1.7 and 1.8 shows that the twitter users tweet mainly using
__'''+', '.join(src_labs)[:', '.join(src_labs).rfind(', ')]+' and, '+', '.join(src_labs)[', '.join(src_labs).rfind(', ')+1:]+'''__
devices more than any other. From the boxplot it is clear that the data is
''')
report.write('skewed.' if src_vals.max() > src_vals.quantile(.75)*1.5 else 'not skewed.')

report.write('''
The following graphs show the analysis of tweets w.r.t. the screen names of the users.
These graphs help in understanding the tweeting frequency of each user.

<center>![Boxplot of users frequencies of tweets](http://localhost:8080/'''+reportpath+'''/Fig-1.9.png "Boxplot of users frequencies of tweets")</center>
<center><sub>Fig 1.9 Boxplot of users frequencies of tweets</sub></center>

<center>![Frequency distribution user\'s tweets](http://localhost:8080/'''+reportpath+'''/Fig-1.10.png "Frequency distribution user\'s tweets")</center>
<center><sub>Fig 1.10 Frequency distribution user\'s tweets</sub></center>

<center>![Histogram for users tweeting Frequency](http://localhost:8080/'''+reportpath+'''/Fig-1.11.png "Histogram for users tweeting Frequency")</center>
<center><sub>Fig 1.11 Histogram for users tweeting Frequency</sub></center>

The figure 1.9, 1.10 and 1.11 shows that the twitter users
__'''+', '.join(scr_name_labs)[:', '.join(scr_name_labs).rfind(', ')]+' and, '+', '.join(scr_name_labs)[', '.join(scr_name_labs).rfind(', ')+1:]+'''__
tend to tweet more about the keywords __'''+KEYWORD1+'__ and, __'+KEYWORD2+'''__
than any other person on twitter from the sample. From the boxplot it is clear that the data is
''')
report.write('skewed.' if scr_name_vals.max() > scr_name_vals.quantile(.75)*1.5 else 'not skewed.')

report.write('''
The following graphs show the time series analysis of tweets w.r.t. keywords been
talked about, over the given period of time.

<center>![Conversation on '''+KEYWORD1+''' and '''+KEYWORD2+''' over the period of time](http://localhost:8080/'''+reportpath+'''/Fig-1.12.png "Conversation on '''+KEYWORD1+''' and '''+KEYWORD2+''' over the period of time")</center>
<center><sub>Fig 1.12 Conversation on '''+KEYWORD1+''' and '''+KEYWORD2+''' over the period of time</sub></center>

''')
report.close()
print('Done.')
