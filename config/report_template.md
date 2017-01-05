##Election Campaign Monitor
************************************************************
## Table of Contents
1. [Training](#1. Training)

2. [Cleaning](#2. Cleaning)

3. [Modelling](#3. Modelling)

4. [Interpretation](#4. Interpretation)

5. [Diagnostics](#5. Diagnostics)

6. [Accuracy](#6. Accuracy)


This report is generated for the elections held or to be held in {{ COUNTRY }}. The dataset
is extracted from Twitter using the keywords __{{ KEYWORD1 }}__ and, __{{ KEYWORD2 }}__ and is
saved under the name __{{ DBName }}__. The collected dataset dates between __{{ SINCE }}__ and __{{ UNTIL }}__ and
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

{{ table1 }}

####2. Cleaning

In order to clean the data obtained using the Twitter APIs, first the discriptor variables are grouped
to see the relationship between various choosen predictor variables,
according to user, place, tweets, and source as mentioned below:
<br/><br/><br/><br/>
<center><sub>Table 2. Discriptor variables grouped according to user, place, tweets etc.</sub></center>

{{ variable_set1 }}

Then, they are clubbed according to the relevance in the model, as mentioned below:

<center><sub>Table 3. Discriptor variables grouped according to relevance in the model</sub></center>

{{ variable_set2 }}

It is seen from the table above that the multifactors predictor variables needs factor reduction.
Also, we have time series column to understand which keyword was spoken the most and at what time over the given duration.
We also see that the dropable variables give the same information as few other variables. For example,
user id gives the same information as the screen name of the user, so they have high correlation and
might affect the overall model and hence, it is dropped from the model. Further it is always a good idea
to analyse the data for frequency distribution, therefore all the multi factor variables are analysed.
The frequency distribution charts and the information obtained using them is also noted.

<center>![Histogram for frequency of tweets]( {{ FILEPATH }}/Fig-1.1.png "Histogram for frequency of tweets")</center>
<center><sub>Fig 1.1 Histogram for frequency of tweets</sub></center>

From the figure 1.1 it can be seen that the number of unique tweets from the
downloaded set of tweets is {{ indv_tweets }} where as the number of
tweets that appear to be same are {{ same_tweets }}. It can also be noted
that the few of the tweets are retweeted more than the others with the tweet __"{{ tweet.idxmax() }}"__
being tweeted the most and appears in the dataset at indexes {{ indexes }} from the users __{{ screen_names }}__

<center>![Text Comparision - Individual and Re-Tweets]( {{ FILEPATH }}/Fig-1.2.png "Text Comparision - Individual and Re-Tweets")</center>
<center><sub>Fig 1.2 Text Comparision - Individual and Re-Tweets</sub></center>

The figure 1.2 shows the number of tweets that contains 'RT ' in front of the
given text and those that do not contain it. From the frequency plot it can be seen
that the number of individual tweets is {{ xvals }} and number of
re-tweets is {{ xvals }} in count.

The following graphs show the analysis of tweets according to the locations. It
might be considered as a good metric to identify people from which places tend to
vote more than others.

<center>![Boxplot of tweets frequency from various places in {{ COUNTRY }}]( {{ FILEPATH }}/Fig-1.3.png "Boxplot of tweets frequency from various places in {{ COUNTRY }}")</center>
<center><sub>Fig 1.3 Boxplot of tweets frequency from various places in '''+COUNTRY+'''</sub></center>

<center>![Frequency distribution tweets in {{ COUNTRY }}]( {{ FILEPATH }}/Fig-1.4.png "Frequency distribution tweets in {{ COUNTRY }}")</center>
<center><sub>Fig 1.4 Frequency distribution tweets in {{ COUNTRY }}</sub></center>

<center>![Histogram for tweets Frequency w.r.t places]( {{ FILEPATH }}/Fig-1.5.png "Histogram for tweets Frequency w.r.t places")</center>
<center><sub>Fig 1.5 Histogram for tweets Frequency w.r.t places</sub></center>

The figure 1.3, 1.4 and 1.5 it is clear that people from __{{ sub_labs }}__ tend to
tweet more than any other places. From the boxplot it is clear that the data is

{{ skewed|not skewed }}

The following graphs show the analysis of tweets according to the sources or the devices used
for tweeting. It is interesting to see which voters tend to use a which kind of device.

<center>![Boxplot of tweets frequency from various sources]( {{ FILEPATH }}/Fig-1.6.png "Boxplot of tweets frequency from various sources")</center>
<center><sub>Fig 1.6 Boxplot of tweets frequency from various sources</sub></center>

<center>![Frequency distribution sources of tweets]( {{ FILEPATH }}/Fig-1.7.png "Frequency distribution sources of tweets")</center>
<center><sub>Fig 1.7 Frequency distribution sources of tweets</sub></center>

<center>![Histogram for tweets Frequency w.r.t sources]( {{ FILEPATH }}/Fig-1.8.png "Histogram for tweets Frequency w.r.t sources")</center>
<center><sub>Fig 1.8 Histogram for tweets Frequency w.r.t sources</sub></center>

The figure 1.6, 1.7 and 1.8 shows that the twitter users tweet mainly using
__{{ src_labs }}__
devices more than any other. From the boxplot it is clear that the data is

{{ skewed|not skewed }}

The following graphs show the analysis of tweets w.r.t. the screen names of the users.
These graphs help in understanding the tweeting frequency of each user.

<center>![Boxplot of users frequencies of tweets]( {{ FILEPATH }}/Fig-1.9.png "Boxplot of users frequencies of tweets")</center>
<center><sub>Fig 1.9 Boxplot of users frequencies of tweets</sub></center>

<center>![Frequency distribution user\'s tweets]( {{ FILEPATH }}/Fig-1.10.png "Frequency distribution user\'s tweets")</center>
<center><sub>Fig 1.10 Frequency distribution user\'s tweets</sub></center>

<center>![Histogram for users tweeting Frequency]( {{ FILEPATH }}/Fig-1.11.png "Histogram for users tweeting Frequency")</center>
<center><sub>Fig 1.11 Histogram for users tweeting Frequency</sub></center>

The figure 1.9, 1.10 and 1.11 shows that the twitter users
__{{ scr_name_labs }}__
tend to tweet more about the keywords __{{ KEYWORD1 }}__ and, __{{ KEYWORD2 }}__
than any other person on twitter from the sample. From the boxplot it is clear that the data is

{{ skewed|not skewed }}

The following graphs show the time series analysis of tweets w.r.t. keywords been
talked about, over the given period of time.

<center>![Conversation on {{ KEYWORD1 }} and {{ KEYWORD2 }} over the period of time]( {{ FILEPATH }}/Fig-1.12.png "Conversation on {{ KEYWORD1 }} and {{ KEYWORD2 }} over the period of time")</center>
<center><sub>Fig 1.12 Conversation on {{ KEYWORD1 }} and {{ KEYWORD2 }} over the period of time</sub></center>

####3. Modelling
For modelling we use backward selection process and interaction terms in order to
identify the statistically significant predictors in the model. The statsmodel
package in Python provides with patsy.dmatrices() function that allows us to
create dummy variables for the model with categorical data without manually
assigning them. So, after reducing the factor levels and creating dummy variables
we apply the logit function on our model and check for significance level of predictors
obtained in each model. Akaike Information Criteria for each one of the models is
mentioned below:

<center><sub>Table 4. AIC values obtained for each model</sub></center>

{{ table2 }}

So, the best model among the selected model is the following:

```
    {{ formula }}
```

After careful few iterations using backward selection method, we obtained the following model.
The result's summary obtained from the logit function are mentioned in the table below:
<br/><br/><br/><br/>

    {{ result_summary }}
    
Since the log likelyhood ratio p-value (LLR p-value) is euqal to {{ pvalue }} which is 

{{ more than 0.05 therefore, we accept the null hypothesis and conclude that the votes are independent of the discriptor variables. So, we donot proceed with further diagnostics. | less than 0.05 therefore, we reject the null hypothesis and conclude that the votes are dependent of the discriptor variables. }}

The confidence intervals and the odds ratios for the model is as follows:

<center><sub>Table 5. Confidence Interval and Odds Ratio for the selected model</sub></center>

So, it can be seen from the model above that the discriptor variables
{{ sig }} are statistically significant where as the variables {{ insig }} are not significant.

####4. Interpretation
According to the given model, following can be said about the given model:

{{ The odds of people voting for %s is %s more likely to occur, if there is no one voting/tweeting. }} |
{{ The odds of people voting for %s is %s less likely to occur, if there is no one voting/tweeting. }} |
{{ The odds of people voting for %s is equally likely to occur w.r.t %s, if there is no one voting/tweeting. }}

{{ For 1 unit increase in %s the odds of people voting for %s is likely to increase by %s }}
{{ For 1 unit increase in %s the odds of people voting for %s is likely to decrease by %s }}
{{ The odds of people voting for %s does not change w.r.t %s. }}
{{ The odds of people voting for %s more likely when the %s is %s as compared to %s by %s }}
{{ The odds of people voting for %s less likely when the %s is %s as compared to %s by %s }}
{{ The odds of people voting for %s equally likely when the %s is %s as compared to %s }}

####5. Diagnostics
Dependent variable (y), predicted values of y(ypred), error terms (e), hat values (h),
pearson's residual values (rpear), deviance residual values (rdev) and, cook's distance
values (D) are clubed together for closer investigation. Below is a small portion of
the data frame generated by clubbing these values:

<center><sub>Table 6. For Diagnostics summary for sample dataset</sub></center>

<center>
{{ sample }}
</center>

<center>![Index plot of pearson\'s residual]( {{ FILEPATH }}/Fig-1.13.png "Index plot of pearson\'s residual")</center>
<center><sub>Fig 1.13 Index plot of pearson\'s residual</sub></center>

<center>![Index plot of deviance residual]( {{ FILEPATH }}/Fig-1.10.png "Index plot of deviance residual")</center>
<center><sub>Fig 1.14 Index plot of deviance residual</sub></center>

Since, the pearson's residual and deviance residual is randomly scattered, having bands of rectangular cloud.
So, the systematic component of the model is correct.

The following graphs show the cases of high leverage and cases of high influence.

<center>![Plot for identifying cases of high leverage]( {{ FILEPATH }}/Fig-1.15.png "Plot for identifying cases of high leverage")</center>
<center><sub>Fig 1.15 Plot for identifying cases of high leverage</sub></center>

Fig 1.15 above shows the cases of high leverage. The values above the cut off {{ cut_off }} point marked in red are the cases of high leverage.
In this case, we have {{ high_leverage }} cases of high leverage.

They are indexed as {{ indexes_leverage }} in the dataset.

<center>![Plot for identifying cases of high influence]( {{ FILEPATH }}/Fig-1.16.png "Plot for identifying cases of high influence")</center>
<center><sub>Fig 1.16 Plot for identifying cases of high influence</sub></center>

The Fig 1.16 shows the cases of high influence. In this case, we have {{ high_influence }} cases of high influence 
and they are indexed as {{ indexes_influence }} in the dataset

####6. Accuracy

The accuracy of the model is obtained by considering the predicted values above 0.5 as {{ KEYWORD2 }} while,
values below or equal to 0.5 as {{ KEYWORD1 }}. A confusion matrix is plotted in order to obtain the overall accuracy of the model.
The following table shows the contigency/confusion matrix:
<br/><br/><br/>

<center><sub>Table 7. Confusion Matrix for the Model</sub></center>

<center>
<table>
<tr>
    <th rowspan='3' style='text-align:center'> Actual</th>
    <th colspan='3' style='text-align:center'>Predicted</th>
    <th>Total</th></tr>
<tr>
    <td> {{ KEYWORD1 }} </td>
    <td> {{ mat[0,0] }} </td>
    <td> {{ mat[0,1] }} </td>
    <td> {{ sum }} </td>
</tr>
<tr>
    <td> {{ KEYWORD2 }} </td>
    <td> {{ mat[1,0] }} </td>
    <td> {{ mat[1,1] }} </td>
    <td> {{ sum }} </td>
</tr>
<tr>
    <th colspan='2' style='text-align:right; margin-right:5px;'>Total</th>
    <td> {{ sum_mat[0,0] }} </td>
    <td> {{ sum_mat[0,1] }} </td>
    <td> {{ sum }} </td>
</tr>
</table>
</center>

So, the model is accurately able to identify {{ per1 }}%
of the results for {{ KEYWORD1 }} and {{ per2 }}%
for {{ KEYWORD2 }}. Also, the overall accuracy of the model is {{ per3 }}%.
So, we can say that the model performs
{{ pretty poorly | fairly | pretty good in predicting the accuracy of {{ KEYWORD1 }}

{{ and also does pretty badly | performs bad |also does fairly well | performs fairly well }}
{{ also does perform good | performs good }}
while predicting the accuracy of {{ KEYWORD2 }}

Consequently, it can be said that {{ mat }}%
of the people are sure to vote for {{ KEYWORD1 }} and, {{ mat }}%
of the people are sure to vote for {{ KEYWORD2 }}.

Consequently, it can be said that {{ mat }}%
of the people are sure to vote for {{ KEYWORD1 }}.

Consequently, it can be said that {{ mat }}%
of the people are sure to vote for {{ KEYWORD2 }}.

<center><sub>*** End ***</sub></center>

\begin{tabularx}{\textwidth}{|*{4}{Y|}}
\hline
\multirow{2}{*}{State of Health} 
  &\multicolumn{2}{c|}{Fasting Value}&After Eating\\
\cline{2-4}
             &Minimum       &Maximum &2 hours after eating\\
\hline
Healthy      &70            &100     &Less than 140\\
\hline
Pre-Diabetes &101           &126     &140 to 200\\
\hline
Diabetes     &More than 126 &N/A     &More than 200\\
\hline
\end{tabularx}


