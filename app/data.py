import utils as ut
from json import dumps


class Prediction:
    def __init__(self, *args):
        self.data = {}
        for arg in args[0]:
            label, feature = arg.split("_")
            self.data[label] = feature
        self.data["Prediction"] = args[1]

    def __str__(self):
        return dumps(self.data)


def train_data(csv_file_path):
    csv_file_generator = ut.csv_to_generator(csv_file_path)
    knowledge = {}
    trained_data = {}
    header = next(csv_file_generator)
    data = ut.splitter(header)
    feature_labels = data[:-1]
    total_features = len(feature_labels)
    for line in csv_file_generator:
        data = ut.splitter(line)
        features = data[:total_features]
        class_belonged = data[-1]
        class_data = knowledge.get(class_belonged, {})
        class_data["_count"] = class_data.get("_count", 0) + 1
        for i in range(total_features):
            base_label = feature_labels[i] + "_"
            label_value = features[i]
            label = base_label + label_value
            class_data[label] = class_data.get(base_label + label_value, 0.0) + 1.0
        knowledge[class_belonged] = class_data
    classes = [c for c in knowledge.keys() if c is not "features_metadata"]
    datasize = float(sum([knowledge[class_val]["_count"] for class_val in classes]))
    # calculating prior probability - the class probability
    for class_val in classes:
        trained_data[class_val] = {'prior': ut.get_probability(knowledge.get(class_val).get('_count'), datasize)}

    # calculating conditional probablity
    for class_val, data in knowledge.items():
        for feature, occurence in data.items():
            if feature is not '_count':
                trained_data[class_val][feature] = ut.get_probability(occurence, data['_count'])
    return trained_data


def get_predictable(csv_file_path):
    csv_file_reader = ut.csv_to_generator(csv_file_path)
    predictable = []
    header = next(csv_file_reader)
    features = ut.splitter(header)
    features_count = len(features)
    for line in csv_file_reader:
        d = []
        values = ut.splitter(line)
        for i in range(features_count):
            d.append(features[i] + "_" + values[i])
        predictable.append(d)
    return predictable


def predict(trained_data, predictables):
    classes = list(trained_data.keys())
    for predictable in predictables:
        probability = 0.0
        classification = ""
        for class_val in classes:
            class_likelihood = 1.0
            for feature in predictable:
                # calculating likelihood for a classes for all features

                class_likelihood = class_likelihood * trained_data[class_val][feature]

            # multiplying likelihood by prior probablity

            class_probability = class_likelihood * trained_data[class_val]['prior']
            if class_probability > probability:
                classification = class_val
                probability = class_probability
        yield Prediction(predictable, classification)
    return


if __name__ == '__main__':
    trained_data = train_data("dataset/data.csv")
    predictions = predict(trained_data, get_predictable('dataset/predict.csv'))
    for prediction in predictions:
        print(prediction)
