#!/usr/bin/python2

from re import sub, compile
pattern = compile("[^a-zA-Z]")

stop_words = set(['', '', 'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', "just", "can", "day", "like", "now", "get", "one", "good", "happy"])

def get_word_count(opts, profile_data):
     text_dir_path = "%s/Text/" % opts.inputdir

     word_correlation = {}
     field = "gender"

     for profile,data in profile_data.items():
         path = "%s/%s.txt" % (text_dir_path, profile)
         with open(path) as f:
             text = f.read()
             words = sub(pattern, " ", text.lower())
             try:
                 bucket = word_correlation[data.get(field)]
             except KeyError:
                 bucket = {}
                 word_correlation[data.get(field)] = bucket
             words = set([word for word in words.split() if word and len(word) > 2]) - stop_words
             for word in words:
                 try:
                     bucket[word] += 1
                 except KeyError:
                     bucket[word] = 1
     super_set = None
     buckets = []
     for val,bucket in word_correlation.items():
         bucket = sorted(bucket.items(), key=lambda obj: obj[1], reverse=True)[:100]
         words  = [word for word,count in bucket]
         try:
             super_set &= set(words)
         except:
             super_set = set(words)
         print val,bucket
         buckets.append((val,words))
     print super_set

     print "\n"
     for val,bucket in buckets:
         print val, set(bucket) - super_set

if __name__ == "__main__":
    from sys import argv

    # Read command line arguments and populate environment variables
    from options import get_opts
    opts = get_opts(argv[1:])

    # Read profile.csv and load a dictionary
    from read_profile import read_profile

    # Assert at each point to check output and print if error
    from assert_return import assert_return

    status,data = read_profile(opts)
    assert_return(opts, status, data)

    get_word_count(opts, data)
