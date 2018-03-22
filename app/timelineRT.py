# -*- coding: utf-8 -*-
"""
Gets accounts being retweeted by a specific user
args:
    screen_name or user_id: target user handle or id
    max-page: maxiumun pages to fetch, each page could contain up to 200 (or --count=X) tweets. default: 1
    save-to: file path to which we'll save the IDs
    count: defaults to 200, max is 200, the total tweets to get per request
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

    if not opt['user_id'] and not opt['screen_name']:
        try:
            stdin = input('Please enter a screen name or a user Id:\n')
        except NameError:
            stdin = raw_input('Please enter a screen name or a user Id:\n')
        except:
            pass

        if stdin and stdin.isdigit():
            opt['user_id'] = stdin
        elif stdin:
            opt['screen_name'] = stdin

    if not opt['user_id'] and not opt['screen_name']:
        print ( 'No user_id or screen_name argument supplied. Exitting..' )
        exit(1)

    uid_key = 'user_id' if opt['user_id'] else 'screen_name'
    print ( 'Processing data for %s' % opt[uid_key] )

    if not opt['save-to']:
        from datetime import datetime
        from helpers import checkWritable
        opt['save-to'] = './timeline-RT-%s-%s.txt' % ( opt[uid_key], str(datetime.now()) )
        checkWritable( opt['save-to'] )

    api = api()
    ids = []
    total=0

    try:
        try: steps = xrange(0,opt['max-page'])
        except NameError: steps = range(0,opt['max-page'])

        max_id=opt['max_id']
        for i in steps:
            args = {uid_key: opt[uid_key], 'count': opt['count'] if opt['count'] and opt['count'] <= 200 else 200}
            if max_id: args['max_id'] = max_id
            tweets = api.user_timeline(**args)
            if tweets:
                for status in tweets:
                    try:
                        if 'retweeted_status' in dir(status):
                            rt = getattr( status, 'retweeted_status' )
                            uid = getattr( getattr(rt, 'author'), 'screen_name' if fetch_handles else 'id' )
                            if uid and uid not in ids: ids.append( uid )
                        max_id = getattr(status, 'id')
                    except:
                        pass
                    total+=1
            else:
                break;

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