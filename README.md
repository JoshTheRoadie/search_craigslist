# search_craigslist
Written in 2016.
This is a small project that allows you to build URL query strings that can be used to search craigslist.com.  The program will run and check for changes based on what you searched and store any new items that meet your criteria in a text file.  The idea is to eventually add SMS alerts if a new item appears that you are looking for. 

To use:

Set up a config.py file that matches the structure of the one here in this repository.

Run the run.py file with one argument that corresponds to a key in config.query_data.
