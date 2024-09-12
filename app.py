import streamlit as st
from model import role_mapping_df,vectorize_role_descriptions, recommend_sap_role


role_descriptions = role_mapping_df['mcDisplayName'].values
sap_roles = role_mapping_df['mcMSKEYVALUE'].values
mskeys = role_mapping_df['mcMSKEY'].values

vectorizer, tfidf_matrix = vectorize_role_descriptions(role_descriptions)

st.title("AI-Powered SAP Role Recommendation System")
role_description_input = st.text_area("Enter a role description:")
user_id_input = st.text_input("Enter the user ID:")
if st.button("Generate Role"):
    mskey, sap_role, display_name = recommend_sap_role(role_description_input, vectorizer, tfidf_matrix, mskeys, sap_roles, role_descriptions)
    st.write(f"Recommended SAP Role: {sap_role}")
    st.write(f"Role Display Name: {display_name}")
    st.write(f"Role MSKEY: {mskey}")
    
if st.button("Provision Role"):
    if MSKEYVALUE and MXREF_MX_ROLE:
        # Provision the role to the user using the SAP IDM REST API with basic authentication
        provision_result = provision_sap_role(MSKEYVALUE, MXREF_MX_ROLE)
        st.write(provision_result)
    else:
        st.write("Please provide all required information (role description, MSKEYVALUE).")
