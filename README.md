#text_cleaner
I have written tools like this several times now and finally decided to do it one more time. This time, however, the tool is reusable and robust.

The command line tool could just be downloaded and used on the command line to clean text documents. The options displayed with `text_cleaner.py -h` will give you the information you need to know how to use this utility.

The stopword list included by default is minimal.

The python porter stemmer implementation used is from [this site](http://tartarus.org/~martin/PorterStemmer/index.html).
From that site:

	All these encodings of the algorithm can be used free of charge for any purpose.

Warning: I ran this on a 90MB text document and it took a while to run (about 6 minutes), took up one whole processor for that time and about 230MB. 
A future enhancement might be to consider and improve the memory usage and processing time for cleaning even relatively large text documents.
