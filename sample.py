# -*-coding:utf-8-*-
from renren import *
import pprint

api_key = "xxx"
secret_key = "xxx"

renren = RenRenOauth(
    api_key=api_key,
    redirect_uri="http://renrenhole.sinaapp.com",
    scope='photo_upload admin_page',
)
print "Go to"

#Redirect user to this url
print renren.get_authorize_url()

code = raw_input("The code?")

#get access_token
renren =\
RenRenOauth(api_key=api_key,secret_key=secret_key,redirect_uri="http://renrenhole.sinaapp.com")
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
