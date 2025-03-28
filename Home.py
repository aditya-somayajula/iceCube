# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
warehouse_sql = f"USE WAREHOUSE COMPUTE_WH"
session.sql(warehouse_sql)
role_sql = f"USE ROLE ACCOUNTADMIN"
session.sql(role_sql)


# ---------- ---------- ---------- Login Page ---------- ---------- ---------- #
def login():
    """Login Page of the application"""
   
    # Set page config
    st.set_page_config(layout = "centered", initial_sidebar_state="collapsed")

    # Set the login container
    col1, col2, col3 = st.columns([2, 6, 2])
    with col2:
        with st.container(border=True):
            st.markdown("""<style>.centered-title {text-align: center;}</style><h1 class="centered-title">🧊</h1>""", unsafe_allow_html=True)
            st.markdown("""<style>.centered-text {text-align: center;font-size: 1.5em;font-weight: normal;color: black;}</style><p class="centered-text">Sign in to IceCube</p>""", unsafe_allow_html=True)
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Sign in", use_container_width=True, type='primary'):
                userInfo_login = f"SELECT * FROM IC_DB_APPLICATION.IC_SM_USERS.IC_TB_USER_INFO WHERE USERNAME = '" + username + "'"
                userAccess_login = f"SELECT * FROM IC_DB_APPLICATION.IC_SM_USERS.IC_TB_USER_ACCESS WHERE USERNAME = '" + username + "'"
                dataFrame_userInfo = session.sql(userInfo_login).to_pandas()
                dataFrame_userAccess = session.sql(userAccess_login).to_pandas()
                if len(dataFrame_userInfo) == 0 :
                    st.error("Invalid username. Please try again.")
                else:               
                    match = dataFrame_userInfo[(dataFrame_userInfo['PASSWORD'] == password)]
                    if not match.empty:
                        if not dataFrame_userInfo.loc[0, 'ACTIVE_FLAG']:
                            st.error("User account is inactive. Please reach out to the administrator.")
                        elif dataFrame_userInfo.loc[0, 'LOCKED_FLAG']:
                            st.error("User account is locked. Please reach out to the administrator.")
                        else:
                            userInfo_update = f"UPDATE IC_DB_APPLICATION.IC_SM_USERS.IC_TB_USER_INFO SET LAST_LOGIN_DATE = CURRENT_TIMESTAMP() WHERE USERNAME = '" + username + "'"
                            session.sql(userInfo_update)
                            st.success("Login successful!")
                            st.session_state["authenticated"] = True
                            st.session_state["email"] = dataFrame_userInfo.loc[0, 'EMAIL']
                            st.session_state["user"] = username
                            if len(dataFrame_userAccess) != 0 :
                                st.session_state["DI_Module"] = dataFrame_userAccess.loc[0, 'DATA_INTEGRATION_ACCESS']
                                st.session_state["DM_Module"] = dataFrame_userAccess.loc[0, 'DATA_MASTERING_ACCESS']
                                st.session_state["DQ_Module"] = dataFrame_userAccess.loc[0, 'DATA_QUALITY_ACCESS']
                                st.session_state["DR_Module"] = dataFrame_userAccess.loc[0, 'DATA_REFERENCE_ACCESS']
                                st.session_state["DA_Module"] = dataFrame_userAccess.loc[0, 'DATA_ANALYTICS_ACCESS']
                                st.session_state["DC_Module"] = dataFrame_userAccess.loc[0, 'DATA_CATALOG_ACCESS']
                                st.session_state["DS_Module"] = dataFrame_userAccess.loc[0, 'DATA_SECURITY_ACCESS']
                            st.rerun()
                    else:
                        if st.session_state["retry_count"] > 3:
                            userInfo_update = f"UPDATE IC_DB_APPLICATION.IC_SM_USERS.IC_TB_USER_INFO SET LOCKED_FLAG = TRUE WHERE USERNAME = '" + username + "'"
                            session.sql(userInfo_update)
                            st.error("Maximum retry attempts reached. User account is locked. Please reach out to the administrator.")
                        else:
                            st.session_state["retry_count"] += 1
                            st.error("Invalid password. Please try again.")
            st.write("<center>Don't have an account? Contact your Snowflake customer admin to request an account.</center>", unsafe_allow_html=True)
# ---------- ---------- ---------- ---------- ---------- ---------- ---------- #



# ---------- ---------- ---------- Home Page ---------- ---------- ---------- #
def home():
    """Home Page of the application"""
    
    # Set page config
    st.set_page_config(layout = "wide", initial_sidebar_state="expanded")
    with st.sidebar:
        st.caption("_Home page for the IceCube application_")

    # Header Row
    col1, col2, col3 = st.columns([2, 20, 2], vertical_alignment="center")
    with col2:
        st.markdown("""<style>.centered-title {text-align: center;}</style><h1 class="centered-title">IceCube🧊</h1>""", unsafe_allow_html=True)
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
                st.rerun()
    st.divider()

    # Row 1
    col11, col12, col13, col14, col15, col16, col17, col18, col19 = st.columns(9, gap="small")
    with col12:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_integration.png" , decompress=False).read()
        col121, col122, col123 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col121:
            st.image(image, width = 100)
        with col122:
            st.page_link("pages/1_Data_Ingestion.py", label="Data Ingestion")
    with col15:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_mastering.png" , decompress=False).read()
        col151, col152, col153 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col151:
            st.image(image, width = 100)
        with col152:
            st.page_link("pages/2_Data_Mastering.py", label="Data Mastering")
    with col18:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_quality.png" , decompress=False).read()
        col181, col182, col183 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col181:
            st.image(image, width = 100)
        with col182:
            st.page_link("pages/3_Data_Quality.py", label="Data Quality")
    st.write('')
    st.write('')

    # Row 2
    col21, col22, col23, col24, col25, col26, col27, col28, col29 = st.columns([2, 2, 2, 2, 2, 2, 2, 2, 2], gap="small")
    with col22:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_reference.png" , decompress=False).read()
        col221, col222, col223 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col221:
            st.image(image, width = 100)
        with col222:
            st.page_link("pages/4_Data_Reference.py", label="Data Reference")
    with col25:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_science_analytics.png" , decompress=False).read()
        col251, col252, col253 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col251:
            st.image(image, width = 100)
        with col252:
            st.page_link("pages/5_Data_Analytics.py", label="Data Analytics")
    with col28:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_catalogue.png" , decompress=False).read()
        col281, col282, col283 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col281:
            st.image(image, width = 100)
        with col282:
            st.page_link("pages/6_Data_Catalog.py", label="Data Catalog")
    st.write('')
    st.write('')

    # Row 3
    col31, col32, col33, col34, col35, col36, col37, col38, col39 = st.columns([2, 2, 2, 2, 2, 2, 2, 2, 2], gap="small")
    with col35:
        image=session.file.get_stream("@IC_DB_APPLICATION.IC_SM_CONFIG.ICECUBE/images/data_access.png" , decompress=False).read()
        col351, col352, col353 = st.columns([0.7, 0.2, 0.2], gap="medium", vertical_alignment="center")
        with col351:
            st.image(image, width = 100)
        with col352:
            st.page_link("pages/7_Data_Security.py", label="Data Security")
    st.write('')
    st.write('')
# ---------- ---------- ---------- ---------- ---------- ---------- ---------- #



# ---------- ---------- ---------- Main Function ---------- ---------- ---------- #
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["page"] = "Login"
        st.session_state["retry_count"] = 0
        st.session_state["DI_Module"] = False
        st.session_state["DM_Module"] = False
        st.session_state["DQ_Module"] = False
        st.session_state["DR_Module"] = False
        st.session_state["DA_Module"] = False
        st.session_state["DC_Module"] = False
        st.session_state["DS_Module"] = False

    if not st.session_state["authenticated"]:
        login()
    else:
        st.session_state["page"] = "Home"
        home()
# ---------- ---------- ---------- ---------- ---------- ---------- ---------- #      


if __name__ == "__main__":
    main()