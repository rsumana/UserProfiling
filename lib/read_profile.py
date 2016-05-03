def compare_feature(training_records):
    print(len(training_records))
    from sys import exit
    from numpy import abs

    feature_map = {'ext_con': {}, 'ope_agr': {}, 'age_ope': {}, 'gender_ope': {}, 'ext_ope':{}}

    for user_id,user_data in training_records.items():
        for feat1,feat2,bucket in [('ext', 'con', 'ext_con'), ('ope', 'agr', 'ope_agr'), ('age', 'ope', 'age_ope'), 
                                      ('gender', 'ope', 'gender_ope'), ('ext', 'ope', 'ext_ope')]:
            val1 = user_data[feat1]
            val2 = user_data[feat2]
            if feat1 in ['ext', 'con', 'agr'] and feat2 in ['ext', 'con', 'ope']:
                diff = abs(val1-val2)
                if diff < 1:
                    key = 1
                elif diff < 2:
                    key = 2
                elif diff < 3:
                    key = 3
                elif diff < 4:
                    key = 4
                else:
                    key = 5
            else:
                def parse_val(val):
                    return int(val/0.5)*0.5
                if feat1 == 'age':
                    if val1 < 24:
                        val1 = 0
                    elif val1 < 34:
                        val1 = 1
                    elif val1 < 48:
                        val1 = 2
                    else:
                        val1 = 3
                if feat2 in ['ext', 'con', 'agr']:
                    val2 = parse_val(val2)
                key = "%d_%d" % (val1, val2)
            try:
                feature_map[bucket][key] += 1
            except KeyError:
                feature_map[bucket][key] = 1
    #import json
    #print(json.dumps(feature_map, indent=4))
    #exit(1)    

def read_profile(opts):
    tmp_records = []
    append = tmp_records.append
    try:
        with open("%s/profile/profile.csv" % opts.inputdir) as file:
            file.readline()
            def read_line(line):
                line = line[:-1]
                user_id,age,gender,ope,con,ext,agr,neu = line.split(',')[1:]

                try:
                    age = float(age)
                    gender = float(gender)
                    ope = float(ope)
                    con = float(con)
                    ext = float(ext)
                    agr = float(agr)
                    neu = float(neu)
                except ValueError:
                    age = 0.0
                    gender = 0.0
                    ope = 0.0
                    con = 0.0
                    ext = 0.0
                    agr = 0.0
                    neu = 0.0
 
                append((user_id, {'age': float(age), 'gender': float(gender), 'ope': float(ope), 'con': float(con), 
                                      'ext': float(ext), 'agr': float(agr), 'neu': float(neu), 'likes': {}, 'averages': []}))
            list(map(read_line, file.readlines()))

            # Based on ratio, shuffle values
            if opts.trainingdir:
                training_count = int(opts.training_ratio * len(tmp_records))
                testing_count  = len(tmp_records) - training_count
            else:
                training_count = len(tmp_records)
                testing_count  = training_count
            
            # Generate two buckets to test and sample data
            import numpy
            numpy.random.shuffle(tmp_records)
            testing_data  = dict(tmp_records[:training_count])
            training_data = dict(tmp_records[training_count:])

        with open("%s/relation/relation.csv" % opts.inputdir) as file:
            for line in file.readlines():
                i,user_id,like_id = line[:-1].split(',')
                if user_id in testing_data:
                    testing_data[user_id]['likes'][like_id] = {}
                elif user_id in training_data:
                    training_data[user_id]['likes'][like_id] = {}
        
        compare_feature(training_data)

        page_type_features = {}
        with open("scrapper/pageInputFeatureTrend.csv") as file:
            file.readline()
            for line in file.readlines():
                page_type,page_like_count,page_user_count,avg_age,avg_ope,avg_ext,avg_agr,avg_con,avg_neu = line[:-1].split(',')
                page_like_count = float(page_like_count)
                if page_like_count < 10:
                    continue
                page_user_count = float(page_user_count)
                avg_age = float(avg_age)
                avg_ope = float(avg_ope)
                avg_ext = float(avg_ext)
                avg_agr = float(avg_agr)
                avg_con = float(avg_con)
                avg_neu = float(avg_neu)
                page_type_features[page_type] = {'page_like_count': page_like_count, 'page_user_count': page_user_count, 
                                                     'age': avg_age, 'ope': avg_ope, 'ext': avg_ext,
                                                     'agr': avg_agr, 'con': avg_con, 'neu': avg_neu}

        import pickle
        try:
            profile_map = pickle.load(open("text/models/profile_map.pickle", "rb"))
        except IOError:
            category_hash = {}
            profile_map   = {}
            from numpy import genfromtxt

            with open("scrapper/pagelikes.csv",'rb') as file:
                for i,record in enumerate(genfromtxt(file, delimiter=',', dtype=str, skip_header = 1)):
                    if i % 100 == 0:
                        print(i)
                    like_id      = record[0]
                    page_type    = record[1][1:-1]
                    values = [float(_val) for _val in record[2:]]
                    profile_map[like_id] = [page_type] + values
            pickle.dump(profile_map, open("text/models/profile_map.pickle", "wb"))
        for data_type in [testing_data, training_data]:
            for user_id,user_data in data_type.items():
                for like_id,like_data in user_data['likes'].items():
                    try:
                        src_like_data = profile_map[like_id]
                        average_vals  = page_type_features[src_like_data[0]]
                        user_data['averages'].append(average_vals)
                    except KeyError:
                        continue
                    like_data.update({'page_type': src_like_data[0], 'likes_count': src_like_data[1:]})
        return 0,{'testing_data': testing_data, 'training_data': training_data}
    except IOError as e:
        return 1, str(e)
