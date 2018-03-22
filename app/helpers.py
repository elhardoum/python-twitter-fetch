# -*- coding: utf-8 -*-

def api():
    from tweepy import OAuthHandler, API
    from config import credentials
    auth = OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
    auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
    return API(auth)

def parseCliArgs():
    from sys import argv
    args = {
        'max-page': int(parseCliArg(argv, 'max-page', 1)),
        'save-to': parseCliArg(argv, 'save-to'),
        'screen_name': parseCliArg(argv, 'screen-name'),
        'user_id': int(parseCliArg(argv, 'user-id', 0)),
        'sleep': int(parseCliArg(argv, 'sleep', 3)),
        'id2handle_sleep': int(parseCliArg(argv, 'id2handle-sleep', 0)),
        'count': int(parseCliArg(argv, 'count', 5000)),
        'hashtag': parseCliArg(argv, 'hashtag'),
        'max_id': int(parseCliArg(argv, 'max-id-start', 0)),
    }

    if args['save-to']:
        checkWritable(args['save-to'])

    if not args['hashtag'] and parseCliArg(argv, 'hashtags'):
        args['hashtag'] = parseCliArg(argv, 'hashtags')

    return args

def parseCliArg(argv, tag, default=None):
    import re
    if argv:
        for arg in argv:
            m = re.search(tag + r'\=(.+)', arg)
            if m and m.group(1):
                return m.group(1)
    return default

def checkWritable(path):
    try:
        from os import remove
        with open(path, 'w') as fopen:
            fopen.write('test\n')
            remove(path)
    except IOError as e:
        raise Exception('Output file specified %s is not writable!\nIOError message: %s' % (path, e))

def writeToFile(path, data):
    try:
        checkWritable(path);
    except e:
        print ( 'Could not save to file, err: %s\ndata: %s' % (e, data) );
        return;
    
    with open(path, 'w') as fopen:
        fopen.write(str(data)+'\n');

    return True;
