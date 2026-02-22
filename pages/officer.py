import streamlit as st
from database import get_complaints_by_domain, update_status
from streamlit_autorefresh import st_autorefresh
from twilio.rest import Client

# --------------------------------------------------
# TWILIO CONFIGURATION
# --------------------------------------------------
TWILIO_ACCOUNT_SID = "ACc5d5d33d02b9a44b7afa6016e6b373a1"
TWILIO_AUTH_TOKEN = "507cbdf43cd0ccde7d82cda37ba4d519"
TWILIO_MESSAGING_SERVICE_SID = "MGf835365c5e01cbc3a806a5a530204574"
RECIPIENT_PHONE = "+91 8788150369"  # Hardcoded recipient

# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(message):
    try:
        client.messages.create(
            body=message,
            messaging_service_sid=TWILIO_MESSAGING_SERVICE_SID,
            to=RECIPIENT_PHONE
        )
        return True
    except Exception as e:
        print(f"SMS sending failed: {e}")
        return False

# --------------------------------------------------
# OFFICER DASHBOARD
# --------------------------------------------------
def show_officer():
    st_autorefresh(interval=5000, key="officer_refresh")

    officer_domain = st.session_state.get("officer_domain")

    if not officer_domain:
        st.error("Officer domain not found. Please login again.")
        return

    st.title(f"👮 {officer_domain} Department Dashboard")

    data = get_complaints_by_domain(officer_domain)

    # --------------------------------------------------
    # SUMMARY SECTION
    # --------------------------------------------------
    total = len(data)
    pending = len([row for row in data if row[4] != "Completed"])
    completed = len([row for row in data if row[4] == "Completed"])

    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Total Complaints", total)
    col2.metric("⏳ Pending", pending)
    col3.metric("✅ Completed", completed)

    st.divider()

    # --------------------------------------------------
    # COMPLAINT LIST
    # --------------------------------------------------
    if total > 0:
        for row in data:
            cid = row[0]
            text = row[1]
            domain = row[2]
            priority = row[3]
            status = row[4]
            timestamp = row[5]

            with st.container():
                st.markdown(f"### 🆔 Complaint ID: {cid}")
                st.write("📝 Complaint:", text)
                st.write("🏷 Domain:", domain)
                st.write("🔥 Priority:", priority)

                # Status Styling
                if status == "Completed":
                    st.success(f"📌 Status: {status}")
                else:
                    st.warning(f"📌 Status: {status}")

                st.write("⏰ Submitted:", timestamp)

                # Button to mark as completed
                if status != "Completed":
                    if st.button("✅ Mark as Completed", key=f"complete_{cid}"):
                        # Update status
                        update_status(cid, "Completed")
                        
                        # Send SMS notification
                        message = f"Complaint ID {cid} under {domain} has been marked as Completed."
                        if send_sms(message):
                            st.success("Complaint marked as Completed and SMS sent!")
                        else:
                            st.warning("Complaint marked as Completed, but SMS failed to send.")

                        st.rerun()

                st.divider()
    else:
        st.info("No complaints assigned to your department.")
