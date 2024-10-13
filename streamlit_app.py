import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define scope for Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate with Google API credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name('/workspaces/blank-app/credentials/creds.json', scope)
client = gspread.authorize(credentials)
print(client);
# Open a Google Sheet by name or URL
sheet = client.open("StreamLit Form").sheet1

# Get data from a specific range or all values
existing_data = sheet.get_all_records()

def submit_record(data):
    sheet.append_row(data)

# Display data in Streamlit
st.dataframe(existing_data)

# List of Business Types and Products
BUSINESS_TYPES = [
    "Manufacturer",
    "Distributor",
    "Wholesaler",
    "Retailer",
    "Service Provider",
]
PRODUCTS = [
    "Electronics",
    "Apparel",
    "Groceries",
    "Software",
    "Other",
]

# Onboarding New Vendor Form
with st.form(key="vendor_form"):
    company_name = st.text_input(label="Company Name*")
    business_type = st.selectbox("Business Type*", options=BUSINESS_TYPES, index=None)
    products = st.multiselect("Products Offered", options=PRODUCTS)
    years_in_business = st.slider("Years in Business", 0, 50, 5)
    onboarding_date = st.date_input(label="Onboarding Date")
    additional_info = st.text_area(label="Additional Notes")

    # Mark mandatory fields
    st.markdown("**required*")

    submit_button = st.form_submit_button(label="Submit Vendor Details")

    # If the submit button is pressed
    if submit_button:
        submit_record([company_name, business_type, ", ".join(products), years_in_business, onboarding_date.strftime("%Y-%m-%d"), additional_info]);
        # submit_record(["John Doe", "johndoe@example.com", "New York", "October 12, 2024"]);
        existing_data = sheet.get_all_records()
        st.dataframe(existing_data)
        st.success("Vendor details successfully submitted!")
