pip install --upgrade pip
pip install streamlit
import streamlit as st
from model import role_mapping_df,vectorize_role_descriptions, recommend_sap_role


role_descriptions = role_mapping_df['mcDisplayName'].values
sap_roles = role_mapping_df['mcMSKEYVALUE'].values
mskeys = role_mapping_df['mcMSKEY'].values

vectorizer, tfidf_matrix = vectorize_role_descriptions(role_descriptions)

st.title("AI-Powered SAP Role Recommendation System")
role_description_input = st.text_area("Enter a role description:")

if st.button("Generate Role"):
    mskey, sap_role, display_name = recommend_sap_role(role_description_input, vectorizer, tfidf_matrix, mskeys, sap_roles, role_descriptions)
    st.write(f"Recommended SAP Role: {sap_role}")
    st.write(f"Role Display Name: {display_name}")
    st.write(f"Role MSKEY: {mskey}")
