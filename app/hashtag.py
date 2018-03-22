# -*- coding: utf-8 -*-
"""
Gets accounts tweeting a specific hashtag
args:
    hashtag: hashtag or hashtags (separated by space) to lookup
    max-page: maxiumun pages to fetch, each page could contain up to 100 (or --count=X) tweets. default: 1
    save-to: file path to which we'll save the IDs
    count: defaults to 100, max is 100, the total tweets to get per request
    max-id-start: if you want to start on a specific tweet ID instead of starting from the most recent tweet.
Twitter ref: https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets
"""

def serve():
    import tweepy
    from tweepy.error import RateLimitError
    from helpers import parseCliArgs, api, writeToFile
    from config import fetch_handles
    from time import sleep
    from sys import argv, exit
    opt = parseCliArgs()

    hashtags = opt['hashtag']
    if not hashtags:
        try:
            stdin = input('Please enter a hashtag or a set of hashtags separated by spaces:\n')
        except NameError:
            stdin = raw_input('Please enter a hashtag or a set of hashtags separated by spaces:\n')
        except:
            pass

        if stdin:
            hashtags = stdin

    if str(hashtags):
        def remhash(s): return s.replace(r'#', '').strip()
        hashtags = [remhash(i) for i in str(hashtags).split(' ')]
        hashtags = [x for x in hashtags if x]

    if not hashtags:
        print ( 'No hashtag supplied. Exitting..' )
        exit(1)

    if not opt['save-to']:
        from datetime import datetime
        from helpers import checkWritable
        opt['save-to'] = './hashtag-%s-%s.txt' % ( ','.join([str(i) for i in hashtags]), str(datetime.now()) )
        checkWritable( opt['save-to'] )

    print ( 'Processing data for #%s' % ', #'.join(hashtags) )
    exit()

    qs = '#' + '+OR+#'.join(hashtags)
    api = api()
    ids = []
    total=0

    try:
        try: steps = xrange(0,opt['max-page'])
        except NameError: steps = range(0,opt['max-page'])

        max_id=opt['max_id']
        for i in steps:
            args = {'q':qs, 'count': opt['count'] if opt['count'] and opt['count'] <= 100 else 100}
            if max_id > 0: args['max_id'] = max_id
            tweets = api.search(**args)
            if tweets:
                for status in tweets:
                    try:
                        uid = getattr( getattr(status, 'author'), 'screen_name' if fetch_handles else 'id' )
                        if uid and uid not in ids: ids.append( uid )
                        max_id = getattr(status, 'id')
                    except:
                        pass
                    total+=1
            else:
                break

            if not 'max-page' in opt or opt['max-page'] <= i+1:
                break

            if int(opt['sleep']) > 0:
                print( 'ZzZ.. (page %d)' % int(i+1) )
                sleep(int(opt['sleep']))
    except RateLimitError:
        print( 'Rate limit exceeded! Halt..' )
    except Exception as e:
        print ( 'Exception raised, err: %s' % e )

    if ids:
        if writeToFile( opt['save-to'], '\n'.join([str(i) for i in ids])):
            print ( 'Successfully saved %d/%d items to %s.' % ( len(ids), total, opt['save-to'] ) )
            exit(0)
        else:
            print ( 'Writing to %s ended with an error.' % opt['save-to'] )
            exit(1)
    else:
        print ( 'No IDs retrieved. Exitting..' )
        exit(1)

if __name__ == '__main__':
    serve()