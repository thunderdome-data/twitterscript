twitterscript
=============

What is this?
-------------

Python script for grabbing an archive of a user's tweets and dumping it into a simple CSV.

`pip install requirements.txt`

Edit local_settings_example.py, adding your secret Twitter keys that you can get from [dev.twitter.com](dev.twitter.com). Rename that file to local_settings.py.

Change the name of the SOURCE_ACCOUNT in local_settings.py.

`python tweetgrab.py`

Credits
---------

Tom Meagher

Assumptions
-----------

* You're using Python and have a set of API keys for Twitter.

License
----------

This code is available under the MIT license. For more information, please see the LICENSE file in this repo.