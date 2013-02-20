# -*-coding:utf-8-*-
from renren import *
import pprint

#api_key = "febdee5ac3324567b390beaa1f0c1307"
api_key = "api_key"
secret_key = "secret_key"
redirect_uri = "http://widget.renren.com/callback.html"

renren = RenRenOauth(
    api_key=api_key,
    redirect_uri=redirect_uri,
    scope='photo_upload admin_page read_user_status publish_comment',
)
print "Go to"

#Redirect user to this url
print renren.get_authorize_url()

code = raw_input("The code?")

#get access_token
renren =\
RenRenOauth(api_key=api_key,secret_key=secret_key,redirect_uri="http://www.whuhole.tk")
access_token = renren.get_access_token(code)

print "access_token is"
print access_token
"""
to make a request
format your params like this
args = {
    "method" : "users.getInfo",
}
"""
args = {
    "method" : "users.getInfo"
}
renren = RenRenOauth(secret_key=secret_key,access_token=access_token["access_token"])
result = renren.request(args)
print "entry is "
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(result)
