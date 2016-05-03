from getopt import getopt,GetoptError

class get_opts:
    inputdir  = None
    outputdir = None
    client_id = None
    client_secret  = None
    training_ratio = 0.7
    trainingdir    = None

    def __init__(self, args):
        try:
            opts,args = getopt(args, "i:o:m:th", ["client_id=", "client_secret=", "training_ratio=", "help"])
        except GetoptError as e:
            print("Error invalid option: " + str(e))
            self.print_help()
        for opt,arg in opts:
            if opt in ['-i']:
                self.inputdir = arg
            elif opt in ['-o']:
                self.resultsdir = arg
            elif opt in ['-m']:
                self.outputdir = arg
            elif opt == '--client_id':
                self.client_id = arg
            elif opt == '--client_secret':
                self.client_secret = arg
            elif opt == '--training_ratio':
                self.training_ratio = float(arg)
            elif opt == '-t':
                self.trainingdir = True
            elif opt in ['-h', '--help']:
                self.print_help()
    def print_help(self):
        print("\t" + "-i               inputdir")
        print("\t" + "-o               outputdir")
        print("\t" + "-t               perform training")
        print("\t" + "--training_ratio <split data into this ratio, 0-1>")
     
        from sys import exit
        exit(1)
