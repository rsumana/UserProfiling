from __future__ import division

def extract_classes_and_mine_words_from_training_file(filename):
    f = open(filename, 'rU')
    lines = f.readlines()
    f.close()
    classes = {}

    all_words = set()
    update = all_words.update
    
    def process_line(line):
        clazz,text = line.split(' ', 1)
        classes[clazz] = 1
        update(line.split())
    list(map(process_line, lines))
    word_hash = dict((word,i+1) for i,word in enumerate(all_words))
    return classes, word_hash, len(word_hash)

def init_hashes(classes, words):
    g_hash = {}
    for clazz in classes.keys():
        clazz_hash = {}
        for word in words.keys():
            clazz_hash[word] = 0
        g_hash[clazz] = clazz_hash
    return g_hash

def update_g_hash(training_file_name, g_hash):
    f = open(training_file_name, 'r')
    lines = f.readlines()
    f.close()

    def iter_g_hash():
        def process_line(line):
            from datetime import datetime
            clazz,text = line.split(' ', 1)

            def update_g_hash_with_a_file():
                words = text.split()
                def update_class_scores(_clazz_hash):
                    _clazz,_hash = _clazz_hash
                    try:
                        return _clazz,sum(map(_hash.get, words))
                    except TypeError as e:
                        print([(word,_hash.get(word)) for word in words if _hash.get(word) == None])
                        raise(e)
                        import sys
                        sys.exit(0)
                score_hash = dict(list(map(update_class_scores, g_hash.items())))

                predicted_class,predicted_score = max(score_hash.items(), key=lambda obj: obj[1])
                accuracy_adddendum = 0	
                if not predicted_class == clazz:
                    alpha = 0.00001
                    def re_update_class_scores(_clazz_hash):
                        _clazz,_hash = _clazz_hash
                        update = _hash.update
                        get    = _hash.get
                        if _clazz == clazz:
                            update(dict([(word,get(word)+alpha) for word in words]))
                        else:
                            update(dict([(word,get(word)-alpha) for word in words]))
                        g_hash[_clazz] = _hash
                    list(map(re_update_class_scores, g_hash.items()))
                else:
                    accuracy_adddendum = 1
                return accuracy_adddendum
            return update_g_hash_with_a_file()
        return sum(map(process_line, lines))

    i = 0
    correct_guesses = 0
    while i < 100 and correct_guesses < 0.99:
        correct_guesses = iter_g_hash()/len(lines)
        print('... accuracy '+str(correct_guesses) + " iteration " + str(i))
        i += 1
    print('trained by '+str(i+1)+' iterations')
    return g_hash, correct_guesses, len(lines)
