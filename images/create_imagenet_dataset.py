#!/bin/env python2

import os
from subprocess import call

def create_dataset(opts, profile_data):
    samples = []
    for root, directories, filenames in os.walk("%s/image/" % opts.inputdir):
        for filename in filenames:
            id,ext = filename.split('.')
            if ext != 'jpg':
                continue
            complete_path = "%s/image/%s" % (opts.inputdir, filename)
            samples.append([complete_path, profile_data[id]['age']])
    train_file    = "%s/%s" % (opts.outputdir, "train_image.txt")
    image_db_path = "%s/DB_train" % (opts.outputdir)
    proto_path    = "%s/proto.txt" % (opts.outputdir)
    with open(train_file, "w") as f:
        for sample in samples:
            filename,age = sample
            if age < 24:
                age = 0
            elif age >= 24 and age < 35:
                age = 1
            elif age >= 35 and age < 45:
                age = 2
            elif age >= 45 and age < 55:
                age = 3
            else:
                age = 4
            f.write("%s\r" % " ".join([filename,str(age)]))
    call(["convert_imageset", "-resize_height", "256", "-resize_width", "256", "/", train_file, image_db_path])
    call(["compute_image_mean", image_db_path, proto_path])

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

    create_dataset(opts, data)
