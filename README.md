# Lyrics Bot Playlister

_A serverless twitter bot, used to power [@nationalbot_the](https://twitter.com/nationalbot_the)._

Built out of a love of [The National](https://americanmary.com/).

## Overview

This repo holds the python, terraform and CI setup to create a set of three lambda functions:

1. `asgi` - which trigers a [FastAPI](https://fastapi.tiangolo.com/) web application which powers an API in API Gateway to respond to Twitter web hooks.
2. `twitter_query` - which is triggered by a cloudwatch event, which fires at a given cron schedule to query a specific account's latest tweet, match them against a list of song lyrics stored in S3, and then, if it finds the song, places it in an SQS queue.
3. `tweet` - which consumes the SQS queue and replies to the queried tweet with the given song title, and then retweets this tweet to make it visible in a profile.

## Future Plans

* Improve documentation
* Use web hooks API to interact with tweeters
* Improve matching of songs using Elasticsearch

## Get in touch

If you're interested in the project, or want to talk about potential cloud based serverless python project, or just also really love The National, email dom dot weldon at gmail dot com.
