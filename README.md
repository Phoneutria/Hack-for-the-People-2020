# Hack-for-the-People-2020

In this three day hackathon, we created Seedlink, a website for connecting communities through gardening. 

SeedLink is a platform for community gardeners to post what seeds, tools, or information they have, and what seeds, tools, or information they are looking for. Users can search other users' listings and contact them through email. Users can set up a rate of exchange on their own, but SeedLink does not encourage this. If users wish to trade seeds rather than buying or selling, they are welcome to do so. 

In addition, SeedLink features a "Get Recommendations" tab, which supplies users with a list of plants that they could start growing right now, based on the time of year and their zipcode. This will help beginners figure out how to start. 

Future features would include an improved user interface the ability to click on recommendations in order to search the catalog for nearby users offering those seeds, without having to run the search manually. 

We would also add a package manager in order to make it easier for collaborators to get started working with SeedLink. 

## Running ##

We did not use a package manager for SeedLink. In order to run it, first clone the repo. SeedLink is built on top of Python 3, so all of the libraries that you install should be compatible with Python 3. 

Install Flask with pip, then run `flask run` in the command line in the repository's root directory. You will get an error message saying that libraries or modules are missing; install those modules with pip and then enter `flask run` again. Repeat this until no more error messages appear. Enter `flask run` one more time, and the Flask server should start. Go to the provided localhost URL, and you should see our website. 
