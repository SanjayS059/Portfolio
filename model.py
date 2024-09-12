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

def provision_sap_role(user_id, sap_role):

    url = f"https://emnov08:init1234@https://sapidm.mydomain.com:50001/idmrestapi/v2/service/ET_MX_PERSON(ID=25475,TASK_GUID=guid'65EF6F8B-E0E3-4E11-B092-C82BC6F57376"
    
    # Create the payload with user ID and role
    payload = {
        "MSKEYVALUE": user_id,
        "MXREF_MX_ROLE": sap_role,
        "validFrom": "2024-01-01",
        "validTo": "2024-12-31"
    }
    
    # Include authentication headers (can be empty if credentials are passed in URL)
    headers = {
        "Content-Type": "application/json"
    }
    
    # Make the API request
    response = requests.post(url, json=payload, headers=headers)
    
    # Check the API response
    if response.status_code == 200:
        return f"Role '{sap_role}' successfully assigned to user '{user_id}'!"
    else:
        return f"Failed to assign role. Error {response.status_code}: {response.text}"

