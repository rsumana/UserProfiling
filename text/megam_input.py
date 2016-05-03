#!/bin/env python2

from re import sub

stop_words = []
lists = ['en.list']
for list in lists:
    file = open("text/%s" % list, "r")
    words = file.read().split('\n')
    words = [sub('[^a-zA-Z0-9\']', '', word.lower()) for word in words]
    stop_words.extend(words)
stop_words = set(stop_words)

slangs = ['asap', 'gn', 'm/f', 'asl', 'idk', 'sd', 'brb', 'jk', 'tnx', 'btw', 'k', 'ty', 'rofl', 'lol', 'ttyl', 'fyi', 'lmao', 
              'wtf', 'fb', 'lmfao', 'wth', 'gm', 'lmk', 'zzz', 'bff', 'jk', 'b4', 'l8', 'gr8', 'plz', 'sry', 'bbz', 'kk', 'kl']

#tokenize = lambda str: " ".join([str for str in sub('[^a-z:)(;]', ' ', str.lower()).split() if str])
def tokenize(str):
    word_only_str       = sub('[^a-z]', ' ', str.lower())
    expression_only_str = sub('[^:;)(]', ' ', str.lower())
    all_punctuations    = [_char for _char in sub('[a-z:;)(\n]', ' ', str.lower()) if _char != ' ']

    from nltk.stem.porter import PorterStemmer
    porter_stemmer = PorterStemmer()

    return " ".join([porter_stemmer.stem(word) for word in word_only_str.split()])
    return " ".join(word_only_str.split() + 
                        ["emoticon" if ':' in word or ';' in word else word for word in expression_only_str.split()] + 
                        all_punctuations)

def read_text_file(opts, user_id):
    path = "%s/text/%s.txt" % (opts.inputdir, user_id)
    file = open(path, "rb")
    status = tokenize(file.read().decode('utf-8', 'ignore'))
    file.close()
    return status

def age_bucket_calculator(age):
    if age < 25:
        return 0
    elif age < 35:
        return 1
    elif age < 49:
        return 2
    else:
        return 3

def personality(trait):
    from math import floor
    return trait

class_fncs = {
    'gender': lambda gender: float(gender),
    'age': age_bucket_calculator,
    'ope': personality,
    'con': personality,
    'ext': personality,
    'agr': personality,
    'neu': personality,
}

def create_input(opts, profile_data, field):
    outfile = open("%s/megam_input_%s.txt" % (opts.outputdir,field), "w")

    # Check input value and convert to a class
    value_fnc = class_fncs.get(field)

    for user_id,data in profile_data['training_data'].items():
        status = read_text_file(opts, user_id)
        outfile.write("%d %s\n" % (value_fnc(data[field]), status))

    """
    import re
    import csv
    import sys
    csv.field_size_limit(sys.maxsize)

    facebook_file = open("scrapper/pageUserMapping.csv", "r", encoding="iso-8859-1")
    #csv_file = csv.reader(facebook_file.read().decode('utf-8', 'ignore'), delimiter=',')
    #csv_file = csv.reader("scrapper/pageUserMapping.csv", delimiter=',')
    #for line in csv_file:
    for params in csv.reader(facebook_file):
        user_id = params[0]
        desc    = params[18]
        category= params[10]
        daily_users   = params[20]
        monthly_users = params[21]
        weekly_users  = params[22]
        data    = profile_data['training_data'].get(user_id)
        if data:
            #print(monthly_users)
            status = tokenize(desc)
            outfile.write("%d %s\n" % (value_fnc(data[field]), status))
            status = tokenize(category)
            outfile.write("%d %s\n" % (value_fnc(data[field]), status))

            for value in [daily_users, monthly_users, weekly_users]:
                if value == 'NA':
                    continue
                outfile.write("%d %s\n" % (value_fnc(data[field]), value))
    """

    outfile.close()

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

    create_input(opts, data)
