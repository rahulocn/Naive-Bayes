import data as d
import settings as st

if __name__ == '__main__':
    trained_data = d.train_data(st.DATA_FILE)
    predictions = d.predict(trained_data, d.get_predictable(st.PREDICT_FILE))
    for prediction in predictions:
        print(prediction)
