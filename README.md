#text_cleaner
I have written tools like this several times now and finally decided to do it one more time. This time, however, the tool is reusable and robust.

The command line tool could just be downloaded and used on the command line to clean text. The options displayed with `text_cleaner.py -h` will give you the information you need to know about how to use the utility.

The stopword list included by default is minimal and is contained within the code.

The python porter stemmer implementation used is from [this site](http://tartarus.org/~martin/PorterStemmer/index.html).
From that web site:

	All these encodings of the algorithm can be used free of charge for any purpose.

