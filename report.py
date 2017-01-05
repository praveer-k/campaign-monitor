from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments import highlight
from markdown2 import markdown
from bs4 import BeautifulSoup
from tabulate import tabulate
from lib import helper
import pdfkit, os

KEYWORD1 = input()
KEYWORD2 = input()
SINCE   = input()
UNTIL   = input()
DBName  = input()
COUNTRY = input()
CACHE   = bool(input())
PORT    = int(input())

filepath = 'app/output/'+DBName
lexer = get_lexer_by_name('python3', stripall=True)
formatter = HtmlFormatter(style='default')
# ------- Apply the heading of markdown as following ----------
table = [['Classifier','Accuracy'],
         ['MultinomialNB', '93.10%'],
         ['BernoulliNB', '94.75%'],
         ['LogisticRegression', '95.10%'],
         ['SGDClassifier', '95.10%'],
         ['SVC', '94.95%'],
         ['NuSVC', '94.95%'],
         ['LinearSVC', '94.90%']]

text = '''##Election Campaign Monitor
************************************************************
## Table of Contents
1. [Training](###1. Training)

2. [Cleaning](#2. Cleaning)

3. [Modelling](#3. Modelling)

4. [Interpretation](#4. Interpretation)

5. [Diagnostics](#5. Diagnostics)

6. [Accuracy](#6. Accuracy)


This report is generated for the elections held or to be held in '''+COUNTRY+'''. The dataset
is extracted from Twitter using the keywords __'''+KEYWORD1+'__ and, __'+KEYWORD2+'''__ and is
saved under the name __'''+DBName+'''__. The collected dataset dates between __'''+SINCE+'__ and __'+UNTIL+'''__ and
only signifies the people's viewpoint as seen on the platform "Twitter", strictly between the given dates.

> __Please Note:__ The Report is generated automatically and is intented for an overview
> of the model only.

In order to analyse the effect of sentiments on the overall decision of the people,
we first analysed the sentiment of each text that was recieved using the Twitter APIs.
For classification of twitter text messages into negative/positive sentiment we used nltk corpus
in order to train the classifiers. Once this sentiment analysis or classification of each
text message into positive/negative sentiment is done, we further go on to investigate
the effects of these messages on the overall decision making of the people using logistic regression.

Each hastag for the first keyword recieved is counted as "+1 vote". The same was applicable to the second keyword.
Out of the few models considered the best model was picked using Akaike Information Criteria or AIC. Once the
best model is selected, the significane of each variable is calculated. The report is then interpreted
for each descriptor variable. To cross verify the quality of the model daignostic graphs are also obtained.

The steps followed during the process is mentioned below:

####1. Training

The accuracy of each classifier after training them with the NLTK corpus for Twitter Senitment Analysis
were the following:

<center><sub>Table 1. Accuracy of the trained classifiers</sub></center>

'''
text += tabulate(table, headers='firstrow', tablefmt='html')
text += '''
####2. Cleaning

In order to clean the data obtained using the Twitter APIs, first the discriptor variables are grouped
to see the relationship between various choosen predictor variables,
according to user, place, tweets, and source as mentioned below:
<br/><br/><br/><br/>
<center><sub>Table 2. Discriptor variables grouped according to user, place, tweets etc.</sub></center>

'''
variables  = helper.get_variables('config/variables.yml')
set1 = helper.dictfilt(variables, ['user','place','tweet','author','source'])
set2 = helper.dictfilt(variables, ['dropable','two_factors','multi_factors','numeric','time_series'])
text += tabulate(set1, headers='keys', tablefmt='html')
text += '''

Then, they are clubbed according to the relevance in the model, as mentioned below:

<center><sub>Table 3. Discriptor variables grouped according to relevance in the model</sub></center>

'''
text += tabulate(set2, headers='keys', tablefmt='html')
text += '''

It is seen from the table above that the multifactors predictor variables needs factor reduction.
Also, we have time series column to understand which keyword was spoken the most and at what time over the given duration.
We also see that the dropable variables give the same information as few other variables. For example,
user id gives the same information as the screen name of the user, so they have high correlation and
might affect the overall model and hence, it is dropped from the model. Further it is always a good idea
to analyse the data for frequency distribution, therefore all the multi factor variables are analysed.
The frequency distribution charts and the information obtained using them is also noted.

'''
# ----------- Read the generated MarkDown File ----------------
f = open(filepath+'/'+DBName+'_report1.md','r')
text += f.read()
f.close()
# ----------- Read the generated MarkDown File ----------------
f = open(filepath+'/'+DBName+'_report2.md','r')
text += f.read()
f.close()
# ----------- Read the generated MarkDown File ----------------
f = open(filepath+'/'+DBName+'_report3.md','r')
text += f.read()
f.close()

text +='''
*********************************************************************
<center><sub>*** End ***</sub></center>
'''
f = open(filepath+'/'+DBName+'_report.md','w')
f.write(text)
f.close()
# os.remove(filepath+'/'+DBName+'_report1.md')
# os.remove(filepath+'/'+DBName+'_report2.md')
# os.remove(filepath+'/'+DBName+'_report3.md')
# ----------- Export MarkDown file to HTML ----------------
html = markdown(text)
html = BeautifulSoup(html, 'html.parser')
for code in html.find_all('code'):
    fragment = BeautifulSoup(highlight(code.string, lexer, formatter), 'html.parser')
    code.string.replace_with( BeautifulSoup(fragment.prettify(), 'html.parser') )
html = html.prettify()
f = open(filepath+'/'+DBName+'_report.html','w')
f.write(html)
f.close()
# ----------- Export HTML string to PDF ----------------
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    'no-outline': None
}
pdfkit.from_string(html, filepath+'/'+DBName+'_report.pdf', options=options, css='./lib/codehilite.css')
