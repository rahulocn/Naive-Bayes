import utils as ut
def csv_to_knowledge(csv_file_path):
    csv_file_reader=open(csv_file_path,'r')
    knowledge={}
    first=True
    features_metadata=set()
    feature_data={}
    for line in csv_file_reader:
        if first:
            fet_and_cls=ut.splitter(line)
            features_names=fet_and_cls[:len(fet_and_cls)-1]
            for fn in features_names:
                feature_data[fn]=set()
            features_count=len(features_names)
            classes=[]
            first = False
        else:
            fet_and_cls = ut.splitter(line)
            features = fet_and_cls[:features_count]
            class_belonged = fet_and_cls[-1]
            class_data=knowledge.get(class_belonged,{})
            for i in range(features_count):
                features_metadata.add(features_names[i]+"_"+(features[i]))
                feature_data[features_names[i]].add(features[i])
                features_count_current=class_data.get(features_names[i]+"_"+features[i],0)
                features_count_current+=1
                class_data[features_names[i]+"_"+features[i]]=float(features_count_current)
            knowledge[class_belonged]=class_data
            classes.append(class_belonged)
    for class_name,class_data in knowledge.iteritems():
        eve=class_data.keys()
        for feature in features_metadata:
            if feature not in eve:
                class_data[feature]=0.0
    knowledge["classes"]=classes
    knowledge["features_data"]=feature_data
    return knowledge
def knowledge_to_probs(knowledge):
    trained_data={}
    classes=knowledge["classes"]
    del knowledge["classes"]
    features_data=knowledge["features_data"]
    del knowledge["features_data"]
    distinct_classes=list(set(classes))
    records=float(len(classes))
    for class_d in distinct_classes:
        count=float(len(filter(lambda x: x==class_d,classes)))
        trained_data[class_d]=count/records
    for class_c,set_of_probs in knowledge.iteritems():
        for indivi_probs,count_prob in set_of_probs.iteritems():
            features_name=indivi_probs.split("_")[0]
            count = float(len(filter(lambda x: x == class_c, classes)))
            trained_data[class_c+"_"+indivi_probs]=(count_prob+1)/(count+len(features_data[features_name]))
    trained_data["classes"]=distinct_classes
    return trained_data
def csv_to_predict(csv_file_path):
    csv_file_reader = open(csv_file_path, 'r')
    first = True
    predict=[]
    for line in csv_file_reader:
        if first:
            features=ut.splitter(line)
            features_count=len(features)
            first=False
        else:
            d = []
            vals=ut.splitter(line)
            for i in range(features_count):
                d.append(features[i]+"_"+vals[i])
            predict.append(d)
    return predict
def predict(trained_data,predict_it):
    classes=trained_data["classes"]
    del trained_data["classes"]
    for predictable in predict_it:
        likelihood = {}
        for class_i in classes:
            this_likli=1.0
            for features in predictable:
                this_likli=this_likli*trained_data[class_i+"_"+features]
            this_likli=this_likli*trained_data[class_i]
            likelihood[class_i]=this_likli
        max=0
        max_cate=""
        for cate,cate_vale in likelihood.iteritems():
            if cate_vale>max:
                max=cate_vale
                max_cate=cate
        print predictable,max_cate