# Python Twitter Fetch

Fetch accounts from Twitter using variety of API endpoints.

## Install

The project has 1 dependency

```bash
pip install tweepy
```

Or use the requirements.txt file.

## Usage

Open `app/config.py` and place in your Twitter app credentials.

Here you have 4 scripts to use as a CLI tool. The arguments can be either passed to the command or manually entered for required ones.

`python3 xx.py --{arg-name}={value}`

**Arguments**

`max-page` maximum number of pages to go through to collect data. Defaults to `1`.

`save-to` optional, set the path to the file where to save the data.

`screen-name` some tools that collect profile-based data require a Twitter user, can be identified by a screen name (handle) or ID.

`user-id` some tools that collect profile-based data require a Twitter user, can be identified by a screen name (handle) or ID.

`sleep` the amount of seconds to sleep between requests. See the Twitter references to find out more about the rate limit in the rate limit interval.

`count` optional, max items to list per request. Defaults to maximal value per endpoint.

`hashtag` for the hashtags, you can use this to enter 1 or more hashtags. Multiple hashtags are separated by spaces.

`max-id-start` for hashtags and retweets, if you want to start on a specific tweet ID instead of starting from the most recent tweet.

## Getting followers

```bash
python3 followers.py --screen_name=realDonaldTrump
```

## Getting friends (followed accounts)

```bash
python3 friends.py --screen_name=realDonaldTrump
```

## Getting hashtags accounts

```bash
python3 hashtag.py --hashtag=NRA
python3 hashtag.py --hashtag="NRA Test"
```

## Getting retweeted accounts

```bash
python3 timelineRT.py --screen_name=realDonaldTrump
```
