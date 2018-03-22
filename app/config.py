"""
Enter your Twitter APP (https://apps.twitter.com) credentials below
"""
credentials = { 'consumer_key': '<xxx>',
'consumer_secret': '<xxx>',
'access_token': '<xxx>',
'access_token_secret': '<xxx>' }

"""
If you only want to fetch Twitter IDs, set to false.
For followers/friends, if this is set to true then
we'll make extra API requests to parse the IDs into
handles as Twitter API endpoints for this return only
an ID list.
"""
fetch_handles = True