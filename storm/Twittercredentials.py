import tweepy



consumer_key = "uyNLRh4tKXyBal2JhLtx0Lvzm"
consumer_secret = "ftA6fNV0vpteQGg35P1V4mpncExmsQZf4va5tC9lZv3vhwNe4V"
access_token = "2192654012-MWlVRmFote5mbCSCNIqKz57ScCHTjMWRKmSK8Oh"
access_token_secret = "a66ohifg6Mbr359Vo4y4DWLjyG21X53zv9WsJW4CTny7q"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



