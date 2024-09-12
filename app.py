import streamlit as st
import requests
from model import role_mapping_df,vectorize_role_descriptions, recommend_sap_role

def provision_sap_role(user_id, sap_role):
    url = f"https://emnov08:init1234@https://sapidm.mydomain.com:50001/idmrestapi/v2/service/ET_MX_PERSON(ID=25475,TASK_GUID=guid'65EF6F8B-E0E3-4E11-B092-C82BC6F57376" 
    payload = {
        "userId": user_id,
        "role": sap_role,
        "validFrom": "2024-01-01",
        "validTo": "2024-12-31"
    }

    response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        return f"Role '{sap_role}' successfully assigned to user '{user_id}'!"
    else:
        return f"Failed to assign role. Error {response.status_code}: {response.text}"
    
role_descriptions = role_mapping_df['mcDisplayName'].values
sap_roles = role_mapping_df['mcMSKEYVALUE'].values
mskeys = role_mapping_df['mcMSKEY'].values

vectorizer, tfidf_matrix = vectorize_role_descriptions(role_descriptions)

st.title("AI-Powered SAP Role Recommendation System")
role_description_input = st.text_area("Enter a role description:")
user_id_input = st.text_input("Enter the user ID:")
if st.button("Generate Role"):
    mskey, sap_role, display_name = recommend_sap_role(role_description_input, vectorizer, tfidf_matrix, mskeys, sap_roles, role_descriptions)

    st.session_state['sap_role'] = sap_role
    st.session_state['mskey'] = mskey
    st.session_state['display_name'] = display_name
    
    st.write(f"Recommended SAP Role: {sap_role}")
    st.write(f"Role Display Name: {display_name}")
    st.write(f"Role MSKEY: {mskey}")
else:
    st.write("Please enter a valid role description.")   
if st.button("Provision Role"):
    sap_role = st.session_state.get('sap_role', None)
    if user_id_input and sap_role:
        provision_result = provision_sap_role(user_id_input, sap_role)
        st.write(provision_result)
    else:
        st.write("Please provide both a role description and a user ID.")
