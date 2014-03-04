email-renderer
==============

This app the html for the guardian open community iframes.

## Running the email renderer

This is a Python appengine application. Grab the source and then run
the dev appserver provided in the Google appengine SDK. From within
the email renderer's directory and assuming you have the linux tools
in your home directory:

    ~/linux-dev/google_appengine/dev_appserver.py . --port=8888

You can then add a new open snippet thing by going to localhost:

## Details

This is a simple CRUD application for creating and editing open snippets.

/create
/delete?id=id
/view?id=id
/update?id=id
/list


## Deployment

Get appengine access sorted out with someone like Nathaniel or Grant and do

~/linux-dev/google_appengine/appcfg.py update .

you can then go to
