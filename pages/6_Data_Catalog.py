# Import python packages
import streamlit as st

# ---------- ---------- ---------- Main Function ---------- ---------- ---------- #
def main():
    """Display Data Catalog Page elements"""
    with st.sidebar:
        st.caption("_Perform data cataloging activities in the IceCube application_")
        st.button("Discovery", type="primary")
        st.button("Governance", type="primary")
        st.button("Collaborate", type="primary")
# ---------- ---------- ---------- ---------- ---------- ---------- ---------- #


if __name__ == "__main__":
    # Set page config
    st.set_page_config(layout = "wide", initial_sidebar_state="expanded")
    if st.session_state["authenticated"]:
        st.session_state["page"] = "Data Catalog"
    else:
        st.switch_page("Home.py")
    
    # Header Row
    col1, col2, col3 = st.columns([2, 20, 2], vertical_alignment="center")
    with col2:
        st.markdown("""<style>.centered-title {text-align: center;}</style><h1 class="centered-title">Data Catalog</h1>""", unsafe_allow_html=True)
    with col3:
        with st.popover(label="", icon="📰", help="Profile"):
            st.write("**Email:** ", st.session_state["email"])
            st.write("**Data Integration:** ", "Yes" if st.session_state["DI_Module"] else "No")
            st.write("**Data Mastering:** ", "Yes" if st.session_state["DM_Module"] else "No")
            st.write("**Data Quality:** " , "Yes" if st.session_state["DQ_Module"] else "No")
            st.write("**Data Reference:** " , "Yes" if st.session_state["DR_Module"] else "No")
            st.write("**Data Analytics:** " , "Yes" if st.session_state["DA_Module"] else "No")
            st.write("**Data Catalog:** " , "Yes" if st.session_state["DC_Module"] else "No")
            st.write("**Data Security:** " , "Yes" if st.session_state["DS_Module"] else "No")
            if st.button("Logout", icon="🏃‍♂️"):
                st.session_state["authenticated"] = False
                st.rerun(scope="app")
    
    if st.session_state["DC_Module"]:
        main()
    else:
        st.error("You don't have access to this module", icon="🚨")