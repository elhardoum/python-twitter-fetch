# -*- coding: utf-8 -*-
"""
Gets followers and of a user and writes them to a file
args:
    screen_name or user_id: target user handle or id
    max-page: maxiumun pages to fetch, each page could contain up to 5000 followers. default: 1
    save-to: file path to which we'll save the IDs
./friends.py depends on this
Twitter ref: https://dev.twitter.com/rest/reference/get/followers/ids
"""

def serve(friends=False):
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
        opt['save-to'] = './%s-%s-%s.txt' % ( opt[uid_key], 'friends' if friends else 'followers', str(datetime.now()) )
        checkWritable( opt['save-to'] )

    api = api()
    ids = []
    screen_names = {}

    try:
        i=0
        for uids in tweepy.Cursor(api.friends_ids if friends else api.followers_ids, **{uid_key: opt[uid_key], 'count': opt['count']}).pages():
            ids.extend(uids)
            
            if fetch_handles:
                last = float(len(uids))/float(100)
                last += 1 if last != int(last) else 0

                try: chunks = xrange(0, int(last))
                except NameError: chunks = range(0, int(last))

                for x in chunks:
                    chunk = uids[x*100:x*100 +100]

                    if not chunk or len(chunk) <= 0: break

                    handles = api._lookup_users(user_id=','.join([str(i) for i in chunk]))
                    if handles:
                        for user in handles:
                            try: screen_names[getattr(user, 'id')] = getattr(user, 'screen_name')
                            except: pass
                    else:
                        raise Exception('Unable to retrieve handles for set of IDs, stop right here.')
                        break

                    if 'id2handle_sleep' in opt and int(opt['id2handle_sleep']) > 0:
                        print( 'ZzZ..' )
                    sleep(int(opt['id2handle_sleep']))

            i+=1
            if not 'max-page' in opt or opt['max-page'] <= i:
                break
            if int(opt['sleep']) > 0:
                print( 'ZzZ.. (page %d)' % i )
                sleep(int(opt['sleep']))
    except RateLimitError:
        print( 'Rate limit exceeded! Halt..' )
    except Exception as e:
        print ( 'Exception raised, err: %s' % e )

    if ids:
        def stringifyId(i): return str(i) if not i in screen_names else screen_names[i]
        if writeToFile( opt['save-to'], '\n'.join([stringifyId(i) for i in ids])):
            print ( 'Successfully saved %d items to %s.' % ( len(ids), opt['save-to'] ) )
            exit(0)
        else:
            print ( 'Writing to %s ended with an error.' % opt['save-to'] )
            exit(1)
    else:
        print ( 'No IDs retrieved. Exitting..' )
        exit(1)

if __name__ == '__main__':
    serve()