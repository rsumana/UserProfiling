from sys import exit

def assert_return(opts,status,data):
    try:
        assert(status == 0)
    except AssertionError:
        print("Error:", data)
        exit(1)
