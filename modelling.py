import pickle, pandas as pd, patsy, statsmodels.api as sm
import numpy as np
from lib import helper
from tabulate import tabulate
import collections

KEYWORD1 = input()
KEYWORD2 = input()
SINCE   = input()
UNTIL   = input()
DBName  = input()
COUNTRY = input()
CACHE   = bool(input())
PORT    = int(input())

filepath = 'app/output/'+DBName
# -----------------------------------------------------------------------------
print('Loading cleaned xlsx output file ...')
xlsx = pd.ExcelFile('app/output/'+DBName+'/'+DBName+'_clean.xlsx')
df = pd.read_excel(xlsx, 'DATA')

formulas = [ 'text ~ source + subdivision + statuses_count + followers_count + retweet_count + contributors_enabled + category + confidence + created_at_day + created_at_mon + created_at_year',
             'text ~ source + subdivision + statuses_count + followers_count + retweet_count + contributors_enabled + category + confidence + category:confidence + created_at_day + created_at_mon + created_at_year + created_at_day:created_at_mon:created_at_year',
             'text ~ source + subdivision + statuses_count + followers_count + retweet_count + contributors_enabled + category + category:confidence + created_at_day:created_at_mon:created_at_year',
             'text ~ source + subdivision + statuses_count + followers_count + retweet_count + contributors_enabled + category:confidence + created_at_day:created_at_mon:created_at_year'
           ]
results = []
print('Model Selection...')
for formula in formulas:
    formula = helper.removeUnwanted(formula, df.columns)
    y,X = patsy.dmatrices(formula, df, return_type='dataframe')
    logit = sm.Logit(y, X)
    result = logit.fit()
    results.append( (formula, y, X, result) )

table = {'Model':[],'AIC':[]}
i = 1
for result in results:
    table['Model'].append('Model '+str(i))
    table['AIC'].append(result[3].aic)
    i += 1

results = [result for result in results if result[3].mle_retvals['converged']==True]
formula, y, X, result = min(results, key=lambda x: x[3].aic)

print('Best Model : ', formula)
print('saving the model...')
model = { 'formula': formula, 'y': y, 'X': X, 'result': result }
f = open('data/pickle/'+DBName+'/model.pkl', 'wb')
pickle.dump(model, f)
f.close()
# -----------------------------------------------------------------------------
print('Re-opening the report markdown file ...')
report = open(filepath+'/'+DBName+'_report2.md','w')
print('Appending into Report file...')
report.write('''
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

''')
report.write(tabulate(table, headers='keys', tablefmt='html'))
report.write('''
So, the best model among the selected model is the following:```'''+formula.replace('retweet_count + contributors_enabled','retweet_count +\n\t contributors_enabled')+'''```
''')
report.write('''

After careful few iterations using backward selection method, we obtained the following model.
The result's summary obtained from the logit function are mentioned in the table below:
<br/><br/><br/><br/>
''')
report.write( '\t'+ helper.addtabs(str(result.summary())) )
report.write('''
Since the log likelyhood ratio p-value (LLR p-value) is euqal to '''+str(result.llr_pvalue)+''' which is''')
if result.llr_pvalue>0.05:
    report.write('''
more than 0.05 therefore, we accept the null hypothesis and conclude that the
votes are independent of the discriptor variables. So, we donot proceed with
further diagnostics.
''')
else:
    report.write('''
less than 0.05 therefore, we reject the null hypothesis and conclude that the
votes are dependent of the discriptor variables.
''')
    report.write('''
The confidence intervals and the odds ratios for the model is as follows:

<center><sub>Table 5. Confidence Interval and Odds Ratio for the selected model</sub></center>

''')
    conf = result.conf_int()
    conf['OR'] = result.params
    conf.columns = ['Lower CI', 'Upper CI', '_Odds Ratio']
    conf = np.exp(conf)
    indexes = conf.index
    conf.reset_index(drop=True, inplace=True)
    conf = conf.to_dict(orient='list')
    conf['Discriptors'] = indexes
    conf = collections.OrderedDict(sorted(conf.items()))
    report.write(tabulate(conf, headers='keys', tablefmt='html'))
    sig = [k for k, v in result.pvalues.iteritems() if v<=0.05 ]
    insig = [k for k, v in result.pvalues.iteritems() if v>0.05 ]
    report.write('''

So, it can be seen from the model above that the discriptor variables
'''+helper.prettyjoin(sig, df.columns)+''' are statistically significant where as the variables
'''+helper.prettyjoin(insig, df.columns)+''' are not significant.

####4. Interpretation
According to the given model, following can be said about the given model:

''')
    refdict = helper.getRefDict(X.columns, df)
    print('Loading variables ...')
    variables  = helper.get_variables('config/variables.yml')
    for k, v in result.params.iteritems():
        if k in sig:
            key = k[:k.find('[')] if k.find('[')!=-1 else k
            val = round(np.exp(v)*100,2)
            if key.lower()=='intercept':
                if val>100:
                    text = '''+ The odds of people voting for %s is %s more likely to
occur, if there is no one voting/tweeting.''' % (KEYWORD2, str(val-100)+'%')
                elif val<100:
                    text = '''+ The odds of people voting for %s is %s less likely to
occur, if there is no one voting/tweeting.''' % (KEYWORD2, str(val-100)+'%')
                else:
                    text = '''+ The odds of people voting for %s is equally likely to
occur w.r.t %s, if there is no one voting/tweeting.''' % (KEYWORD2, KEYWORD1)
            elif key in variables['numeric'] and k.find(':')==-1 and k.find('*')==-1:
                if val>100:
                    text = '''+ For 1 unit increase in %s the odds of people
voting for %s is likely to increase by %s''' % (key, KEYWORD2, str(val-100)+'%')
                elif val<100:
                    text = '''+ For 1 unit increase in %s the odds of people
voting for %s is likely to decrease by %s''' % (key, KEYWORD2, str(100-val)+'%')
                else:
                    text = '''+ The odds of people voting for %s does not change
w.r.t %s.''' % (KEYWORD2, key)
            elif key in refdict.keys() and k.find(':')==-1 and k.find('*')==-1:
                lookfor = '[T.' if k.find('[T.')!=-1 else '['
                myvar = k[k.find(lookfor)+len(lookfor):-1]
                if val>100:
                    text = '''+ The odds of people voting for %s more likely
when the %s is %s as compared to %s by %s''' % (KEYWORD2, key, myvar, refdict[key], str(val-100)+'%')
                elif val<100:
                    text = '''+ The odds of people voting for %s less likely
when the %s is %s as compared to %s by %s''' % (KEYWORD2, key, myvar, refdict[key], str(100-val)+'%')
                else:
                    text = '''+ The odds of people voting for %s equally likely
when the %s is %s as compared to %s''' % (KEYWORD2, key, myvar, refdict[key])
            else: #Interaction terms
                if val>100:
                    text = ''''''
                elif val<100:
                    text = ''''''
                else:
                    text = ''''''
            report.write(text+'\n\n')
    report.close()
    print('Done.')
