open-module
==============

This app the html for the guardian open community iframes.

## Running

This is a Python appengine application. Grab the source and then run
the dev appserver provided in the Google appengine SDK. From within
the open-modules  and assuming you have the linux tools
in your home directory:

    ~/linux-dev/google_appengine/dev_appserver.py . --port=8888

You can then add a new open snippet thing by going to localhost:

## Details

This is a simple CRUD application for creating and editing open snippets.

The following public endpoints are supported and available under at http://open-module.appspot.com


/create - this is default
/delete?id=id
/preview?id=id
/update?id=id
/list

These endpoint will require you to authenticate yourself with a guardian.co.uk email

/view?id=id

This is the json endpoint which returns a json representation of an open snippet. It is unsecured and served over https

## Deployment

Get appengine access sorted out with someone like Nathaniel or Grant and do

~/linux-dev/google_appengine/appcfg.py update .

This probably won't work in of itself though, as two factor authentication gets in the way. So do

~/linux-dev/google_appengine/appcfg.py update . --oauth2 --no_cookies

