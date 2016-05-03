def softmax(x):
    import numpy as np

    """Compute softmax values for each sets of scores in x."""
    sf = np.exp(x)
    sf = sf/np.sum(sf, axis=0)
    return sf

from math import pow
def classify(text, g_hash):
    from numpy import std

    score_hash = {}
    words = text.split()
    #for clazz in g_hash.keys():
    def get_class_scores(clazz_hash):
        clazz,clazz_hash = clazz_hash
        #clazz_hash = g_hash[clazz]
        score = 0
        for word in words:
            if clazz_hash.get(word):
                score += clazz_hash[word]
        score_hash[clazz] = score
    list(map(get_class_scores, g_hash.items()))
		
    min_val = sorted(softmax(sorted(list(score_hash.values()))), reverse=True)
    predicted_class,predicted_score = max(score_hash.items(), key=lambda obj: obj[1])
    a = min_val
    """
    print(score_hash.items())
    ratio = min_val/max_val

    
    if ratio > 3.5326285722e-24:
        print("flipped")
        predicted_class,predicted_score = min(score_hash.items(), key=lambda obj: obj[1])
    """
    return predicted_class.strip(),a
