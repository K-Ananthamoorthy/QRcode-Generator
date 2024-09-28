import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO

# Helper function to generate and download QR code
def generate_qr_code(data):
    qr = qrcode.QRCode(version=3, box_size=10, border=3,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to a BytesIO object
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    return byte_im

# Function to get vCard data
def get_v_card():
    st.subheader("Generate vCard")
    name = st.text_input("First Name:", placeholder="John")
    surname = st.text_input("Last Name:", placeholder="Doe")
    address = st.text_input("Address:", placeholder="123 Main St")
    email = st.text_input("Email:", placeholder="john.doe@example.com")
    phone = st.text_input("Phone Number:", placeholder="(123) 456-7890")
    if name and surname and address and email and phone:
        contact = (f"BEGIN:VCARD\n"
                   f"VERSION:3.0\n"
                   f"N:{surname};{name};;;\n"
                   f"FN:{name} {surname}\n"
                   f"ADR;TYPE=home:{address}\n"
                   f"EMAIL:{email}\n"
                   f"TEL;TYPE=CELL:{phone}\n"
                   f"END:VCARD\n")
        return contact
    return None

# Function to get Event data
def get_event():
    st.subheader("Generate Event")
    start_date = st.text_input("Start Date (YYYYMMDD HHMM):", "20241231 2330")
    end_date = st.text_input("End Date (YYYYMMDD HHMM):", "20241231 2359")
    title = st.text_input("Event Title:", placeholder="My Event")
    description = st.text_area("Event Description:", placeholder="This is the event description.")
    url = st.text_input("Event URL (Optional):", placeholder="https://example.com")

    if start_date and end_date and title:
        event = (f"BEGIN:VEVENT\n"
                 f"SUMMARY:{title}\n"
                 f"DESCRIPTION:{description}\n"
                 f"DTSTART:{start_date.replace(' ', 'T')}\n"
                 f"DTEND:{end_date.replace(' ', 'T')}\n"
                 f"URL:{url}\n"
                 f"END:VEVENT\n")
        return event
    return None

# Function to get Wi-Fi data
def get_wifi():
    st.subheader("Generate Wi-Fi QR")
    encryption = st.selectbox("Encryption Type:", ["None", "WPA/WPA2", "WEP"])
    network_name = st.text_input("Wi-Fi Name:", placeholder="Network Name")
    password = st.text_input("Password:", placeholder="Password")

    if network_name:
        encryption_type = {"None": "nopass", "WPA/WPA2": "WPA", "WEP": "WEP"}[encryption]
        return f"WIFI:T:{encryption_type};S:{network_name};P:{password};;"
    return None

# Custom CSS for mobile-first design
st.markdown("""
    <style>
        @media only screen and (max-width: 600px) {
            .stButton button {
                width: 100%;  /* Full-width buttons on mobile */
                padding: 16px;
            }
            .stTextInput input {
                width: 100%; /* Full-width input fields */
            }
            .stTextArea textarea {
                width: 100%;  /* Full-width text areas */
            }
        }
        .stTextInput, .stTextArea {
            margin-bottom: 20px;
        }
        .stDownloadButton button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border-radius: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# Main Streamlit app
st.title("🎨 QR Code Generator - Mobile Ready")
st.markdown("""
Welcome to the **best** QR Code Generator! Choose the type of QR code you'd like to generate,
enter the relevant information, and download your personalized QR code. 
This web app is fully responsive and works great on both **mobile** and **desktop** devices!
""")

# Sidebar for selection
qr_type = st.sidebar.selectbox("Select QR Code Type", 
                               ["Text", "URL", "vCard", "Event", "Wi-Fi"])

# Logic for QR Code data
data = None
if qr_type == "Text":
    data = st.text_input("Enter the Text:", placeholder="Type your text here...")
elif qr_type == "URL":
    data = st.text_input("Enter the URL:", placeholder="https://example.com")
elif qr_type == "vCard":
    data = get_v_card()
elif qr_type == "Event":
    data = get_event()
elif qr_type == "Wi-Fi":
    data = get_wifi()

# Generate and display QR code
if data:
    st.markdown("### Generated QR Code 📷")
    
    # Generate the QR code and display it
    qr_image = generate_qr_code(data)
    st.image(qr_image, use_column_width=True)
    
    # Provide download button for the QR code
    st.download_button(
        label="📥 Download QR Code",
        data=qr_image,
        file_name=f"{qr_type.lower()}_qr_code.png",
        mime="image/png"
    )

    st.success("QR Code generated successfully! Download it using the button above.")
else:
    st.info("Please enter the required information to generate a QR code.")
