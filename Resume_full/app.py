import nltk
import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

nltk.download('punkt')
nltk.download('stopwords')


#loading models
clf = pickle.load(open('clf.pkl','rb'))
tfidfd = pickle.load(open('tfidf.pk1','rb'))

def cleanresume(resume_text):
    cleanTxt = re.sub(r'http\S+\s', ' ', resume_text)
    cleanTxt = re.sub('RT|cc',' ',cleanTxt)
    cleanTxt = re.sub('#\S+s',' ',cleanTxt)
    cleanTxt = re.sub('@\S+',' ',cleanTxt)
    cleanTxt = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"""),' ',cleanTxt)
    cleanTxt = re.sub(r'[^\x00-\x7f]',' ',cleanTxt)
    cleanTxt = re.sub('\s+',' ',cleanTxt)

    return cleanTxt

# webapp

def main():
    st.title('Resume Screening App')
    upload_file = st.file_uploader('Upload Resume',type = ['txt','pdf'])

    if upload_file is not None:
        try:
            resume_bytes = upload_file.read()
            resume_text = resume_bytes.decode('utf-8')
        except UnicodeDecodeError:
            resume_text = resume_bytes.decode('latin-1')



        cleaned_resume = cleanresume(resume_text)
        input_features = tfidfd.transform([cleaned_resume])
        prediction_id = clf.predict(input_features)[0]
        st.write(prediction_id)

        category_mapping = {
            15: 'Java Developer',
            23: 'Testing',
            8: 'DevOps Engineer',
            20: 'Python Developer',
            24: 'Web Designing',
            12: 'HR',
            13: 'Hadoop',
            3: 'Blockchain',
            10: 'ETL Developer',
            18: 'Operations Manager',
            6: 'Data Science',
            22: 'Sales',
            16: 'Mechanical Engineer',
            1: 'Arts',
            7: 'Database',
            11: 'Electrical Engineering',
            14: 'Health and Fitness',
            19: 'PMO',
            4: 'Businees Analyst',
            9: 'DotNet Developer',
            2: 'Automation Testing',
            17: 'Network Security Engineer',
            21: 'SAP Developer',
            5: 'Civil Engineer',
            0: 'Advocate',

        }

        category_name = category_mapping.get(prediction_id, "Unknown")

        st.write("Prediction Category: ", category_name)








if __name__ == "__main__":
    main()
