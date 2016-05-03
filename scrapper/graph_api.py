import json
import facebook
import requests
import sys

"""
#r = requests.get('https://graph.facebook.com/oauth/access_token', params=oauth_args)
try:
    message = json.loads(r.content)
    print(message)
    sys.exit(1)
except ValueError:
    access_token = r.content.split('=')[1]
print(r.content)
"""

"""
facebook.get_user_from_cookie
graph = facebook.GraphAPI(access_token=access_token)
"""

def extract(like_ids, outputdir, do_not_follow=False):
    import json
    print(like_ids)
    post_ids = like_ids
    posts = {}
    try:
        posts = graph.get_objects(ids=post_ids)
    except facebook.GraphAPIError as e:
        print(e)
        if not do_not_follow:
            posts.extend([extract([id], outputdir, do_not_follow=True) for id in like_ids])
    if not do_not_follow:
        for like_id,obj in posts.items():
            file = open("%s/%s" % (outputdir,like_id), "wb")
            file.write(json.dumps(obj))
    return posts

class facebook_obj:
    def __init__(self, opts):
        self.client_id = opts.client_id
        self.client_secret = opts.client_secret
    def connect(self):
        try:
            assert(self.client_id != None)
            assert(self.client_secret != None)
        except AssertionError:
            return 1, "client_id and client_secret parameters required"
        oauth_args = dict(client_id = self.client_id,
                          client_secret = self.client_secret,
                          grant_type    = 'client_credentials')
        r = requests.get('https://graph.facebook.com/oauth/access_token', params=oauth_args)
        try:
            message = json.loads(r.content)
            return 1, message
        except ValueError:
            access_token = r.content.split('=')[1]
            self.graph = facebook.GraphAPI(access_token=access_token)
            return 0, "Connection created"
    def get_pages(self, like_ids, outputdir, do_not_follow=False):
        print(like_ids)
        post_ids = like_ids
        posts = {}
        try:
            posts = self.graph.get_objects(ids=post_ids)
        except facebook.GraphAPIError as e:
            print(e)
            if not do_not_follow:
                [posts.update(self.get_pages([id], outputdir, do_not_follow=True)) for id in like_ids]
        if not do_not_follow:
            for like_id,obj in posts.items():
                file = open("%s/%s" % (outputdir,like_id), "wb")
                file.write(json.dumps(obj))
        return posts

if __name__ == "__main__":
    from sys import argv
    from getopt import getopt
    from os import walk

    from assert_return import assert_return
    from options import get_opts
    opts = get_opts(argv[1:])

    inputdir  = opts.inputdir
    outputdir = opts.outputdir

    facebook_conn = facebook_obj(opts)
    status,data = facebook_conn.connect()
    assert_return(opts, status, data)

    relations_path = "%s/relation/relation.csv" % inputdir

    like_ids = []
    with open(relations_path) as f:
        f.readline()
        for line in f.readlines():
            id,user_id,like_id = line[:-1].split(',')
            like_ids.append(like_id)
    like_ids = set(like_ids)
    for (dirpath, dirnames, filenames) in walk(outputdir):
        like_ids -= set(filenames)
    like_ids = list(like_ids)

    for i in range(0, len(like_ids), 10):
        facebook_conn.get_pages(like_ids[i:i+10], outputdir=outputdir)

