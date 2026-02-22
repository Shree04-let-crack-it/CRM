import streamlit as st
import pandas as pd
import plotly.express as px
from database import get_complaints, update_priority, delete_complaint


def show_admin():
    st.title("🛠 Admin Dashboard")

    data = get_complaints()

    if not data:
        st.info("No complaints found.")
        return

    # -------------------------------
    # DATAFRAME
    # -------------------------------
    df = pd.DataFrame(
        data,
        columns=["ID", "Text", "Domain", "Priority", "Status", "Timestamp"]
    )

    # -------------------------------
    # METRICS SECTION
    # -------------------------------
    total = len(df)
    pending = len(df[df["Status"] != "Completed"])
    completed = len(df[df["Status"] == "Completed"])

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Total Complaints", total)
    col2.metric("⏳ Pending", pending)
    col3.metric("✅ Completed", completed)

    st.divider()

    # -------------------------------
    # CHART SECTION
    # -------------------------------
    st.subheader("📈 Complaint Analytics")

    chart_col1, chart_col2 = st.columns(2)

    # Priority Distribution Pie
    priority_counts = df["Priority"].value_counts().reset_index()
    priority_counts.columns = ["Priority", "Count"]

    priority_colors = {
        "Low": "#4CAF50",
        "Normal": "#2196F3",
        "High": "#F44336"
    }

    fig_priority = px.pie(
        priority_counts,
        names="Priority",
        values="Count",
        title="Priority Distribution",
        color="Priority",
        color_discrete_map=priority_colors,
        hole=0.4
    )

    chart_col1.plotly_chart(fig_priority, use_container_width=True)

    # Status Distribution Pie
    df["StatusGroup"] = df["Status"].apply(
        lambda x: "Completed" if x == "Completed" else "Incomplete"
    )

    status_counts = df["StatusGroup"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    status_colors = {
        "Completed": "#4CAF50",
        "Incomplete": "#FF9800"
    }

    fig_status = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Completion Status",
        color="Status",
        color_discrete_map=status_colors,
        hole=0.4
    )

    chart_col2.plotly_chart(fig_status, use_container_width=True)

    st.divider()

    # -------------------------------
    # TABLE DISPLAY
    # -------------------------------
    st.subheader("📋 All Complaints")
    st.dataframe(df.drop(columns=["StatusGroup"]), 
                 use_container_width=True, 
                 hide_index=True)

    st.divider()

    # -------------------------------
    # ACTION SECTION
    # -------------------------------
    st.subheader("⚙ Complaint Management")

    action_col1, action_col2 = st.columns(2)

    complaint_ids = df["ID"].tolist()

    # -------- PRIORITY UPDATE --------
    with action_col1:
        st.markdown("### 🔥 Update Priority")

        selected_id = st.selectbox(
            "Select Complaint ID",
            complaint_ids,
            key="update_priority"
        )

        new_priority = st.selectbox(
            "Select New Priority",
            ["Low", "Normal", "High"]
        )

        if st.button("Update Priority"):
            update_priority(selected_id, new_priority)
            st.success("Priority Updated Successfully")
            st.rerun()

    # -------- DELETE --------
    with action_col2:
        st.markdown("### 🗑 Delete Complaint")

        delete_id = st.selectbox(
            "Select Complaint ID",
            complaint_ids,
            key="delete_complaint"
        )

        if st.button("Delete Complaint"):
            delete_complaint(delete_id)
            st.success("Complaint Deleted Successfully")
            st.rerun()
