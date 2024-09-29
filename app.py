import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import datetime

# Function to generate QR code
def generate_qr_code(data, fill_color="#000000", back_color="#FFFFFF"):
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

# Function to convert image to bytes for Streamlit
def convert_to_bytes(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Function to download image
def download_image(img):
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Function to get vCard data
def get_v_card():
    st.subheader("Generate vCard")
    name = st.text_input("First Name", "")
    surname = st.text_input("Last Name", "")
    address = st.text_input("Address", "")
    email = st.text_input("Email", "")
    phone = st.text_input("Phone Number", "")
    if name and surname:
        contact = (f"BEGIN:VCARD\n"
                   f"VERSION:3.0\n"
                   f"N:{surname};{name};;;\n"
                   f"FN:{name} {surname}\n"
                   f"ADR;TYPE=HOME:;;{address};;;;\n"
                   f"EMAIL;TYPE=INTERNET:{email}\n"
                   f"TEL;TYPE=CELL:{phone}\n"
                   f"END:VCARD\n")
        return contact
    else:
        st.info("Please fill in at least the first and last name.")
        return None

# Function to get Event data
def get_event():
    st.subheader("Generate Event QR Code")
    
    # Date and time inputs
    start_date = st.date_input("Start Date", datetime.date.today())
    start_time = st.time_input("Start Time", datetime.datetime.now().time())
    end_date = st.date_input("End Date", start_date)
    end_time = st.time_input("End Time", (datetime.datetime.now() + datetime.timedelta(hours=1)).time())
    
    title = st.text_input("Event Title", "")
    description = st.text_area("Event Description", "")
    url = st.text_input("Event URL (Optional)", "")
    
    if title:
        # Formatting dates and times
        dt_format = "%Y%m%dT%H%M%S"
        dtstart = datetime.datetime.combine(start_date, start_time).strftime(dt_format)
        dtend = datetime.datetime.combine(end_date, end_time).strftime(dt_format)
        
        event = (f"BEGIN:VEVENT\n"
                 f"SUMMARY:{title}\n"
                 f"DESCRIPTION:{description}\n"
                 f"DTSTART:{dtstart}\n"
                 f"DTEND:{dtend}\n"
                 f"URL:{url}\n"
                 f"END:VEVENT\n")
        return event
    else:
        st.info("Please enter the event title.")
        return None

# Function to get Wi-Fi data
def get_wifi():
    st.subheader("Generate Wi-Fi QR Code")
    encryption = st.selectbox("Encryption Type", ["None", "WPA/WPA2", "WEP"])
    network_name = st.text_input("Wi-Fi Network Name (SSID)", "")
    password = st.text_input("Password", "", type="password")
    hidden = st.checkbox("Hidden Network")
    
    if network_name:
        encryption_type = {"None": "nopass", "WPA/WPA2": "WPA", "WEP": "WEP"}[encryption]
        hidden_str = 'true' if hidden else 'false'
        wifi_data = f"WIFI:T:{encryption_type};S:{network_name};P:{password};H:{hidden_str};;"
        return wifi_data
    else:
        st.info("Please enter the Wi-Fi network name.")
        return None

# Function to get SMS data
def get_sms():
    st.subheader("Generate SMS QR Code")
    phone_number = st.text_input("Phone Number", "")
    message = st.text_area("Message", "")
    
    if phone_number:
        sms_data = f"SMSTO:{phone_number}:{message}"
        return sms_data
    else:
        st.info("Please enter the phone number.")
        return None

# Function to get Email data
def get_email():
    st.subheader("Generate Email QR Code")
    to = st.text_input("To", "")
    subject = st.text_input("Subject", "")
    body = st.text_area("Body", "")
    
    if to:
        email_data = f"MATMSG:TO:{to};SUB:{subject};BODY:{body};;"
        return email_data
    else:
        st.info("Please enter the recipient's email address.")
        return None

# Function to get Phone Call data
def get_phone_call():
    st.subheader("Generate Phone Call QR Code")
    phone_number = st.text_input("Phone Number", "")
    
    if phone_number:
        call_data = f"TEL:{phone_number}"
        return call_data
    else:
        st.info("Please enter the phone number.")
        return None

# Main app function
def main():
    st.title("📱 QR Code Generator")
    st.markdown("Generate custom QR codes easily and efficiently.")

    # Sidebar for QR code type selection
    qr_type = st.sidebar.selectbox(
        "Select QR Code Type",
        ["Text", "URL", "vCard", "Event", "Wi-Fi", "SMS", "Email", "Phone Call"]
    )

    data = None
    if qr_type == "Text":
        st.subheader("Generate Text QR Code")
        text_input = st.text_area("Enter your text here", "")
        if text_input:
            data = text_input
        else:
            st.info("Please enter the text to encode.")

    elif qr_type == "URL":
        st.subheader("Generate URL QR Code")
        url_input = st.text_input("Enter the URL", "")
        if url_input:
            data = url_input
        else:
            st.info("Please enter a valid URL.")

    elif qr_type == "vCard":
        data = get_v_card()

    elif qr_type == "Event":
        data = get_event()

    elif qr_type == "Wi-Fi":
        data = get_wifi()

    elif qr_type == "SMS":
        data = get_sms()

    elif qr_type == "Email":
        data = get_email()

    elif qr_type == "Phone Call":
        data = get_phone_call()

    # QR code customization options
    st.markdown("### QR Code Customization")
    col1, col2 = st.columns(2)
    with col1:
        fill_color = st.color_picker("Select QR Code Color", "#000000")
    with col2:
        back_color = st.color_picker("Select Background Color", "#FFFFFF")

    # Generate and display QR code
    if data:
        st.markdown("### Generated QR Code")
        img = generate_qr_code(data, fill_color, back_color)

        # Convert to bytes for Streamlit
        img_bytes = convert_to_bytes(img)

        st.image(img_bytes, caption="Your QR Code", use_column_width=True)
        
        # Download option
        st.download_button(
            label="Download QR Code",
            data=img_bytes,
            file_name="qr_code.png",
            mime="image/png",
        )
    else:
        st.info("Fill in the required fields to generate a QR code.")

    # Footer
    st.markdown("---")
    st.markdown("Made with ❤️ by Ananthamoorthi")

# Run the app
if __name__ == "__main__":
    main()
