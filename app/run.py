import data as dp
import settings as st
if __name__ == '__main__':
    knowledge=dp.csv_to_knowledge(st.DATA_FILE)
    trained_data=dp.knowledge_to_probs(knowledge)
    data_to_predict=dp.csv_to_predict(st.PREDICT_FILE)
    dp.predict(trained_data, data_to_predict)