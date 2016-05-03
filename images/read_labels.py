import tensorflow as tf

from conv import f,apply_conv

def extract_image_labels(opts, profile_data):
    inputdir = "%s/image/" % opts.inputdir

    for id,profile_data in profile_data.items():
        name = "%s/%s.jpg" % (inputdir,id)
        name_label = "%s %f" % (name,profile_data['age'])
        apply_conv(name)
        """
        with open("%s/%s.jpg" % (inputdir,id)) as file:
            pass
        """
    return
    """Consumes a single filename and label as a ' '-delimited string.
    Args:
      filename_and_label_tensor: A scalar string tensor.
    Returns:
      Two tensors: the decoded image, and the string label.
    """
    filename, label = tf.decode_csv(filename_and_label_tensor, [[""], [""]], " ")
    file_contents = tf.read_file(filename)
    example = tf.image.decode_png(file_contents)
    return example, label

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

    extract_image_labels(opts, data)
