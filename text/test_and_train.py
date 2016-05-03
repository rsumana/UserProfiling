likes_test_data = []

def create_word2vec_input(opts, profile_data, field):
    from .megam_input import create_input,read_text_file
    outfile = open("%s/word2vec_input_%s.txt" % (opts.outputdir,field), "w")

    for user_id,data in profile_data['training_data'].items():
        status = read_text_file(opts, user_id)
        outfile.write("%s\n" % (status))

def test_and_train(opts, profile_data, field='gender'):
    from .perceplearn import extract_classes_and_mine_words_from_training_file, init_hashes, update_g_hash
    from .percepclassify import classify
    from .megam_input import create_input,read_text_file
    from .page_like_randomforest import bayes_randomforest_input as like_randomforest_classifier, get_test_data_likes
    from .randomforestimpl import bayes_randomforest_input,get_test_data

    def produce_g_hash():
        input_file = "%s/megam_input_%s.txt" % (opts.outputdir, field)
        create_input(opts, profile_data, field)
        classes,word_hash,word_count = extract_classes_and_mine_words_from_training_file(input_file)
        g_hash = init_hashes(classes, word_hash)
        g_hash, correct_guesses, total_lines = update_g_hash(input_file, g_hash)
        return g_hash
    def train_liwc_file():
        return bayes_randomforest_input(opts, profile_data, field)
    
    if not opts.trainingdir:
        import pickle

        #g_hash
        g_hash = pickle.load(open("text/models/%s_g_hash.pickle" % field, "rb"))

        #random_forest
        test_records  = get_test_data(opts, field)
        random_forest = pickle.load(open("text/models/%s_random_forest.pickle" % field, "rb"))

        #likes_random_forest
        likes_classifier = pickle.load(open("text/models/%s_likes_random_forest.pickle" % field, "rb"))
    else:
        likes_classifier = like_randomforest_classifier(opts, profile_data, field)
        g_hash = produce_g_hash()
        random_forest = train_liwc_file()
        test_records  = get_test_data(opts, field)
        
    from .megam_input import class_fncs
    value_fnc = class_fncs[field]

    rms_values = []

    average_lens = {'correct': [], 'incorrect': []}

    correct = 0
    incorrect = 0

    model_pred_corr  = 0
    model_pred_incorr = 0

    model_accuracy = {'percep': [0,0], 'liwc': [0,0], 'likes': [0,0], 'avg': [0,0]}
    model_feedback = []

    from math import pow

    for user_id,user_data in profile_data['testing_data'].items():
        status = read_text_file(opts,user_id)
        val    = value_fnc(user_data[field])

        # for liwc
        test_feature = test_records[user_id]
        # for page likes
        like_data    = user_data['page_counts']

        liwc_pred = 0
        like_pred = 0
        percep_pred = 0

        prediction,conf_score = classify(status, g_hash)
        percep_pred = float(prediction)

        if field == 'age':
            liwc_pred = float(random_forest.predict([test_feature])[0])
            liwc_conf = max(random_forest.predict_proba([test_feature]).tolist()[0])
            if liwc_conf > 0.5:
                pred = liwc_pred
            else:
                prediction,conf_score = classify(status, g_hash)
                pred = float(prediction)
        elif field == 'gender':
            liwc_conf = max(random_forest.predict_proba([test_feature]).tolist()[0])
            like_conf = -1
            if like_data:
                like_conf = max(likes_classifier.predict_proba(like_data).tolist()[0])
            if liwc_conf > 0.7:
                pred = float(random_forest.predict([test_feature])[0])
            elif like_conf > 0.7:
                pred = float(likes_classifier.predict(like_data)[0])
            else:
                prediction,conf_score = classify(status, g_hash)
                pred = float(prediction)
        else:
            if like_data:
                like_pred = float(likes_classifier.predict(like_data)[0])
                pred = like_pred
            else:
                pred = float(random_forest.predict([test_feature])[0])

        from numpy import mean
        from math import pow
        avg_pred = 0

        print("pref", pred, liwc_pred, percep_pred, like_pred, avg_pred)
        outcome_prob = 1

        if int(pred) == val:
            if outcome_prob == 1:
                model_pred_corr += 1
            else:
                model_pred_incorr += 1
            correct += 1
            #print("corr", percep_pred, liwc_pred, like_pred, pred, count, val, len(status.split()))
            feedback_result = "1"
        else:
            if outcome_prob == 0:
                model_pred_corr += 1
            else:
                model_pred_incorr += 1
            incorrect += 1
            #print("incorr", percep_pred, liwc_pred, like_pred, pred, count, val, len(status.split()))
            feedback_result = "0"
        print(correct,incorrect)
        print((correct*100)/(correct+incorrect))

        percep_acc = model_accuracy['percep']
        liwc_acc = model_accuracy['liwc']
        like_acc = model_accuracy['likes']
        avg_acc  = model_accuracy['avg']

        if int(percep_pred) == val:
            percep_acc[0] += 1
        else:
            percep_acc[1] += 1
        if int(liwc_pred) == val:
            liwc_acc[0] += 1
        else:
            liwc_acc[1] += 1
        if int(like_pred) == val:
            like_acc[0] += 1
        else:
            like_acc[1] += 1
        if int(avg_pred) == val:
            avg_acc[0] += 1
        else:
            avg_acc[1] += 1
        print("Percept:", percep_acc[0]*100/(sum(percep_acc)), " liwc:", liwc_acc[0]*100/(sum(liwc_acc)), 
                  " like:", like_acc[0]*100/(sum(like_acc)), " avg:", avg_acc[0]*100/sum(avg_acc)) 
        print((model_pred_corr*100)/(model_pred_corr+model_pred_incorr))

        # update data
        try:
            user_data['predictions'][field] = pred
        except KeyError:
            user_data['predictions'] = {field: pred}

    if opts.training_ratio == 0:
        import pickle
        #g_hash
        file = open("text/models/%s_g_hash.pickle" % field, "wb")
        pickle.dump(g_hash, file, protocol=2)

        #random_forest
        file = open("text/models/%s_random_forest.pickle" % field, "wb")
        pickle.dump(random_forest, file, protocol=2)

        #likes_random_forest
        file = open("text/models/%s_likes_random_forest.pickle" % field, "wb")
        pickle.dump(likes_classifier, file, protocol=2)
	
    try:
        rms = pow(sum(rms_values)/len(rms_values), 0.5)
        print(rms)
        print(correct, incorrect)
        print(correct*100/(correct+incorrect))
    except ZeroDivisionError:
        pass
