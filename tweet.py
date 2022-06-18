# this script will allow you to create a tweet from terminal
# in order to use this script you need to add your credentials in creds.py

from helium import *
from . import creds

username = creds.username
password = creds.password

tweet = " " + input("Tweet? ")


try:
    start_chrome("https://twitter.com/login", headless=True)
    wait_until(Text("Sign").exists)
    write(username, into="Phone, email, or username")
    click("Next")
    wait_until(Text("Enter your password").exists)
    write(password, into="Password")
    click("Log in")
    wait_until(Text("Home").exists)
    write(tweet, into="What’s happening?")
    click("Tweet")

except:
    print("Something went wrong")

else:
    print("Tweeted Successfully")
