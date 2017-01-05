import os, json
import pickle, zipfile
import tweepy
from lib import helper

KEYWORD1 = input()
KEYWORD2 = input()
SINCE   = input()
UNTIL   = input()
DBName  = input()
COUNTRY = input()
CACHE   = bool(input())
PORT    = int(input())

if __name__ == '__main__':
    KEYWORD = KEYWORD1 + ' ' + KEYWORD2
    # -----------------------------------------------------------
    dirpath = 'data/pickle/'+DBName
    if not (os.path.exists(dirpath) and os.path.isdir(dirpath)):
        print('\nCreating pickling folders ...')
        os.mkdir(dirpath)
    # -----------------------------------------------------------
    print('Loading Configuration ...')
    f = open('config/config.json')
    config = json.load(f)
    f.close()
    # -----------------------------------------------------------
    print('Fetching Country\'s information ...')
    countries = helper.get_all_countries()
    country = countries[COUNTRY]
    # -----------------------------------------------------------
    print('Initiallising Twitter API ...')
    config = config['twitter']
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.secure = True
    auth.set_access_token(config['access_key'], config['access_secret'])
    api = tweepy.API(auth)
    # -----------------------------------------------------------
    print('Downloading place ids from twitter ...')
    filename = dirpath+'/places.pkl'
    if os.path.exists(filename) and os.path.isfile(filename) and CACHE:
        print('Loading from the cache...')
        f = open(filename, 'rb')
        country = pickle.load(f)
        f.close()
    else:
        country['places'] = helper.download_place_ids(api, country)
        f = open(filename, 'wb')
        pickle.dump(country, f)
        f.close()
    # -----------------------------------------------------------
    print('\nDownloading user ids from twitter ...')
    filename = dirpath+'/users.pkl'
    users = None
    if os.path.exists(filename) and os.path.isfile(filename) and CACHE:
        print('Loading from the cache...')
        f = open(filename, 'rb')
        users = pickle.load(f)
        f.close()
    else:
        users = helper.download_user_ids(api, KEYWORD, country)
        f = open(filename, 'wb')
        pickle.dump(users, f)
        f.close()
    # -----------------------------------------------------------
    print('\nRevese map place ids and user ids to subdivisions ... ')
    places = helper.reverse_map(country['places'])
    users  = helper.reverse_map(users)
    user_ids = list(sorted(users.keys()))
    # -----------------------------------------------------------
    print('Downloading users timeline ...')
    bar = helper.IncrementalBar('Downloading ', max=len(users))
    for user_id in user_ids:
        data = {'id' : user_id,
                'place_id' : users[user_id][0],
                'subdivision' : places[users[user_id][0]][0],
                'keyword' : KEYWORD,
                'since' : SINCE,
                'until' : UNTIL,
                'path' : dirpath
               }
        bar.next()
        helper.download_users_timeline(api, data)
    # -----------------------------------------------------------
    print('\nSaving all data into MongoDB ... ')
    helper.save_data_to_mongoDB(PORT, DBName, dirpath, user_ids)
    # -----------------------------------------------------------
    print('\nZipping all user timelines up ... ')
    fzip = zipfile.ZipFile(dirpath+'/users_timeline.zip', 'w')
    for root, dirs, files in os.walk(dirpath):
        for afile in files:
            username = afile[1:len(afile)-4]   # remove '@'~~~'.pkl'
            if username in users:
                fzip.write(os.path.join(root,afile))
                os.unlink(os.path.join(root,afile))
    # -----------------------------------------------------------
    print('Done.')
