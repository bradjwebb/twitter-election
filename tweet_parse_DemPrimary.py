"""twitter api, json dict objects"""
import json
import logging
import os
import time
from stream_files import stream_list


# instantiate error logging handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = logging.FileHandler('ParseLog')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
handler.setFormatter(formatter)
logger.addHandler(handler)

current_time = time.strftime('%Y-%m-%d %H:%M:%S')

stream_files = stream_list

parsed_files = []

start = time.clock()
# instantiate file paths
for i in stream_files:
    if i not in parsed_files:
        original_tweets_file = i
        filepath = os.path.basename(original_tweets_file)
        original_tweets_file = open(original_tweets_file, 'r')
        currated_tweets_file = os.path.join(filepath + '__parsed__' + '.txt')

        print('Current file: {}, Start: {}'.format(filepath, current_time))

        pytweet_key = 0

        # parse each tweet from file into a new file
        for line in original_tweets_file:
            data = line.strip()
            if data:
                pytweet_key += 1
                try:
                    tweet = json.loads(line)
                    tweet_field_headers = [
                        'id_str',
                        'created_at',
                        'text',
                        'coordinates',
                        'place',
                        'lang',
                    ]

                    user_field_headers = [
                        'location',
                        # 'lang',
                    ]

                    entities_field_headers = [
                        'hashtags',
                        # 'user_mentions',
                    ]

                    new_tweet = {}
                    new_tweet['primary_key'] = pytweet_key
                    new_tweet.update(
                        {
                            field: tweet.get(field, None)
                            for field in tweet_field_headers
                        }
                    )
                    new_tweet.update(
                        {
                            field: tweet['user'].get(field, None)
                            for field in user_field_headers
                        }
                    )
                    new_tweet.update(
                        {
                            field: tweet['entities'].get(field, None)
                            for field in entities_field_headers
                        }
                    )
                    with open(currated_tweets_file, 'a') as twtfl:
                        try:
                            json.dump(new_tweet, twtfl)
                            twtfl.write('\n')
                        except (SystemExit, KeyboardInterrupt):
                            raise
                        except Exception:
                            logger.error('Write Failure: ', exc_info=True)

                except (SystemExit, KeyboardInterrupt):
                    raise
                except Exception:
                    logger.error('Write Failure: ', exc_info=True)

#     twtfl.close()

end = time.clock()
runtime = end - start
# sub_runtime = sub_end - sub_start

# print 'The count process took: %f seconds' % (sub_runtime)
print('Total Tweets: ', pytweet_key)
print('Total Runtime (secs): ', runtime)
print('Estimated runtime per tweet, in seconds: {}'.format((runtime/pytweet_key)))
print('Estimated tweets processed per second: {}'.format((pytweet_key/runtime)))
