import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_role_mapping_data():

    file_path = 'Book1(Sheet1).csv'
    role_mapping_df = pd.read_csv(file_path)
    return role_mapping_df

role_mapping_df = load_role_mapping_data()

role_descriptions = role_mapping_df['mcDisplayName'].values
sap_roles = role_mapping_df['mcMSKEYVALUE'].values
mskeys = role_mapping_df['mcMSKEY'].values

def vectorize_role_descriptions(descriptions):

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = vectorize_role_descriptions(role_descriptions)

def recommend_sap_role(input_description, vectorizer, tfidf_matrix, mskeys, sap_roles, descriptions):

    input_tfidf = vectorizer.transform([input_description])
    cosine_similarities = cosine_similarity(input_tfidf, tfidf_matrix).flatten()
    best_match_index = cosine_similarities.argmax()
    return mskeys[best_match_index], sap_roles[best_match_index], descriptions[best_match_index]


