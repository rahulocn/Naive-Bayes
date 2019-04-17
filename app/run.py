import data as dp
import settings as st
if __name__ == '__main__':
    k=dp.csv_to_knowledge(st.DATA_FILE)
    t=dp.knowledge_to_probs(k)
    p=dp.csv_to_predict(st.PREDICT_FILE)
    dp.predict(t,p)