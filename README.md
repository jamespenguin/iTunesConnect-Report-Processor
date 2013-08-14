iTunesConnect-Report-Processor
==============================

This is a simple Python script that automates processing monthly finanical reports generated by Apple for the App Store.

Requirements
------------

* Python >= 2.6 - [http://python.org](http://python.org)
* Requests - [https://github.com/kennethreitz/requests](https://github.com/kennethreitz/requests)


Configuration
-------------

1. Go to [http://openexchangerates.org/](http://openexchangerates.org/)
2. Click "Get Your App ID" in the top right hand corner of the website
3. Register your account (there's a forever free plan at the bottom of the plan options page.)
4. Open up merge.py and paste your account's App ID in the app_id variable at the top of the script.

Usage
-----

1. Extract all report archives to a single directory, along with the merge.py script.
2. Double click 'merge.py'.  It'll generate a consolidated CSV file for your app sales.
3. ?????????
4. PROFIT!