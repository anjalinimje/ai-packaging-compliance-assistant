import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go

from checks.folder_checks import *
from checks.document_checks import *
from checks.vendor_source_checks import *
from checks.intune_checks import *
from checks.psadt_checks import *
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet


# --------------------------------
# Configure page title and layout
# ---------------------------------


st.set_page_config(
    page_title="🤖 AI Packaging Compliance Assistant",
    layout="wide"
)
# -------------------------
# Sidebar Navigation
# -------------------------

with st.sidebar:

    st.image(
        "assets/logo.png",
        width=180
    )

    st.header("🤖 AI Assistant")

    st.success("Ready to Scan")

    st.markdown("---")

    st.write("📂 Package Validation")
    st.write("📈 Compliance Dashboard")
    st.write("🤖 AI Recommendations")
    st.write("📄 Executive Reports")

#-------------------------
# Custom UI Styling
#-------------------------
st.markdown("""
<style>

.stButton > button {
    background: linear-gradient(90deg,#00D4FF,#0099FF);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 200px;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Header Section
# -------------------------

col1, col2, col3 = st.columns([1,1,3])

with col2:
    st.image(
        "assets/logo.png",
        width=150
    )

with col3:
    st.title(
        "🤖 AI Packaging Compliance Assistant"
    )



st.markdown("""
### 🚀 Enterprise Packaging Intelligence Platform

Automatically validate:

✅ PowerShell deployment scripts

✅ Intune packaging standards

✅ Vendor source integrity

✅ QA documentation compliance

✅ Deployment readiness

""")

st.success(
    "💰 Reduces manual QA effort, improves packaging quality, and accelerates deployment readiness through automation."
)

st.markdown("""
<style>

.stTextInput input {
    background-color: #1E2530;
    color: white;
    border: 2px solid #00D4FF;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# Package Path Input
# -------------------------

package_path = st.text_input(
    "📂 Enter Package Path"
)

# -------------------------
# Results Storage
# -------------------------
results = []

def add_result(check, status, remark=""):
    results.append({
        "Check": check,
        "Status": status,
        "Remark": remark
    })

scan = st.button(
    "🚀 Run Compliance Scan",
    use_container_width=True
)

# -------------------------
# Scan Execution
# -------------------------
if scan:

    if not os.path.exists(package_path):
        st.error("❌ Package path does not exist")
        st.stop()

    

    # -------------------------
    # Naming Standard
    # -------------------------

    info = validate_naming_standard(package_path)

    if not info:

        add_result(
            "Naming Standard",
            "❌ FAIL",
            "Unable to determine Vendor/Application/Version"
        )

        vendor = "--"
        application = "--"
        version = "--"

    elif not info["valid"]:

        add_result(
        "Naming Standard",
            "❌ FAIL",
            info["remark"]
        )

        vendor = "--"
        application = "--"
        version = "--"

    else:

        vendor = info["vendor"]
        application = info["application"]
        version = info["version"]

        add_result(
            "Naming Standard",
            "✅ PASS",
            f"{vendor}\\{application}\\{version}"
        )

    st.markdown("---")

    st.subheader("📦 Package Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🏢 Vendor", vendor)

    with col2:
        st.metric("📦 Application", application)

    with col3:
        st.metric("🔖 Version", version)

    # -------------------------
    # Folder Paths
    # -------------------------

    documents = os.path.join(
        package_path,
        "Documents"
    )

    package = os.path.join(
        package_path,
        "Package"
    )

    intune = os.path.join(
        package_path,
        "Intune"
    )

    vendor_source = os.path.join(
        package_path,
        "VendorSource"
    )

    # -------------------------
    # Required Folders
    # -------------------------

    required_folders = {
        "Documents": documents,
        "Package": package,
        "Intune": intune,
        "VendorSource": vendor_source
    }

    for name, path in required_folders.items():

        if os.path.isdir(path):

            add_result(
                f"{name} Folder",
                "✅ PASS",
                f"{name} folder exists"
            )

        else:

            add_result(
                f"{name} Folder",
                "❌ FAIL",
                f"{name} folder missing"
            )

    # -------------------------
    # Logs Check
    # -------------------------

    try:

        status, msg = check_logs(documents)

        add_result(
            "Logs",
            "✅ PASS" if status else "❌ FAIL",
            msg
        )

    except Exception as e:

        add_result(
            "Logs",
            "❌ FAIL",
            str(e)
        )

    # -------------------------
    # QA Checklist
    # -------------------------

    try:

        status, msg = check_qa_checklist(
            documents
        )

        add_result(
            "QA Checklist",
            "✅ PASS" if status else "❌ FAIL",
            msg
        )

    except Exception as e:

        add_result(
            "QA Checklist",
            "❌ FAIL",
            str(e)
        )

    # -------------------------
    # Readme Validation
    # -------------------------

    try:

        status, msg = validate_readme(
            documents,
            vendor,
            application,
            version
        )

        add_result(
            "Readme",
            "✅ PASS" if status else "❌ FAIL",
            msg
        )

    except Exception as e:

        add_result(
            "Readme",
            "❌ FAIL",
            str(e)
        )

    # -------------------------
    # VendorSource Validation
    # -------------------------

    installers = []

    try:

        installers = check_vendor_source(
            vendor_source
        )

        if installers:

            add_result(
                "VendorSource Installer",
                "✅ PASS",
                f"{len(installers)} installer file(s) found: {', '.join(installers)}"
            )

        else:

            add_result(
                "VendorSource Installer",
                "❌ FAIL",
                "No installer files found in VendorSource"
            )

    except Exception as e:

        add_result(
            "VendorSource Installer",
            "❌ FAIL",
            str(e)
        )

    # -------------------------
    # Intune Validation
    # -------------------------

    try:
        
        status, msg = check_intune(
            intune
        )

        if status:

            add_result(
                "Intune",
                "✅ PASS",
                f"IntuneWin file found: {msg}"
            )

        else:

            add_result(
                "Intune",
                "❌ FAIL",
                msg
            )

    except Exception as e:

        add_result(
            "Intune",
            "❌ FAIL",
            str(e)
        )

    # -------------------------
    # Deploy-Application.ps1
    # -------------------------

    deploy_ps1 = os.path.join(
        package,
        "Deploy-Application.ps1"
    )

    if os.path.exists(deploy_ps1):

        #add_result(
        #    "Deploy-Application.ps1",
        #    "✅ PASS",
        #    "Deploy-Application.ps1 exists"
        #)

        try:

            ps = analyze_ps1(
                deploy_ps1
            )

            if ps["hardcoded_c"] or ps["hardcoded_d"]:

                add_result(
                    "Hardcoded Paths",
                    "❌ FAIL",
                    "Hardcoded C:\\ or D:\\ path found"
            )

            else:

                add_result(
                    "Hardcoded Paths",
                    "✅ PASS",
                    "No hardcoded local paths found"
            )

            add_result(
                "Silent Install",
                "✅ PASS" if ps["silent_install"] else "❌ FAIL",
                "Silent install command found"
                if ps["silent_install"]
                else "Silent install command not found"
            )

            add_result(
                "Silent Uninstall",
                "✅ PASS" if ps["silent_uninstall"] else "❌ FAIL",
                "Silent uninstall command found"
            if ps["silent_uninstall"]
            else "Silent uninstall command not found"
        )

            add_result(
                "Upgrade Logic",
                "✅ PASS" if ps["upgrade_logic"] else "❌ FAIL",
                "Upgrade/removal commands found"
                if ps["upgrade_logic"]
                else "No upgrade commands used"
            )

            add_result(
                "Shortcut Removal",
                "✅ PASS" if ps["shortcut_logic"] else "❌ FAIL",
                "Shortcut removal commands found"
                if ps["shortcut_logic"]
                else "No shortcut removal commands used"
            )

        except Exception as e:

            add_result(
                "PSADT Analysis",
                "❌ FAIL",
                str(e)
            )

    else:

        add_result(
            "Deploy-Application.ps1",
            "❌ FAIL",
            "Deploy-Application.ps1 missing"
        )

    
    # -------------------------
    # Results
    # -------------------------

    st.subheader("📊 Detailed Compliance Results")

    df = pd.DataFrame(results)

    pass_count = len(
        df[df["Status"].str.contains("PASS", na=False)]
    )

    fail_count = len(
        df[df["Status"].str.contains("FAIL", na=False)]
    )

    def color_status(val):

        if "PASS" in val:
            return "background-color:#d4edda"

        if "FAIL" in val:
            return "background-color:#f8d7da"

        return ""
      


    passed = len(
        df[df["Status"] == "✅ PASS"]
    )

    failed = len(
        df[df["Status"] == "❌ FAIL"]
    )



    compliance = 0

    if (passed + failed) > 0:

        compliance = round(
            (
                passed /
                (passed + failed)
            ) * 100,
            2
        )
    # -------------------------
    # Risk Level
    # -------------------------
    

    if compliance >= 90:
        risk = "Low"
    elif compliance >= 75:
        risk = "Medium"
    else:
        risk = "High"

    # -------------------------
    # Compliance Gauge
    # -------------------------

    fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=compliance,
    title={'text': "Compliance Score"},
    gauge={
        'axis': {'range': [0,100]},
        'bar': {'color': "green"},
        'steps': [
            {'range': [0,50], 'color': "red"},
            {'range': [50,80], 'color': "orange"},
            {'range': [80,100], 'color': "lightgreen"}
        ]
    }
))
    
    fig.update_layout(
    height=400,
    font=dict(size=18)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric("Compliance",f"{compliance}%")

    with col2:
        st.metric("Passed",pass_count)

    with col3:
        st.metric("Failed",fail_count)

    with col4:
        st.metric("Risk",risk)


    # -------------------------
    # Executive Summary
    # -------------------------

    if compliance >= 90:
        summary = "🟢 Package is deployment ready."
    elif compliance >= 75:
        summary = "🟡 Minor compliance issues detected."
    else:
        summary = "🔴 Significant compliance issues found."

    st.subheader("📋 Executive Summary")
    st.success(summary)

    

    # -------------------------
    # AI Recommendations
    # -------------------------

    st.subheader("🤖 AI Recommendations")

    failed_df = df[
    df["Status"].str.contains("FAIL", na=False)
    ]

    for _, row in failed_df.iterrows():
        st.warning(
            f"{row['Check']} → {row['Remark']}"
    )

    st.subheader("📋 Compliance Validation Results")
    
    def color_status(val):
        if val == "PASS":
            return "background-color: #d4edda"
        elif val == "FAIL":
            return "background-color: #f8d7da"
        return ""

    styled_df = df.style.map(
        color_status,
        subset=["Status"]
    )

    st.dataframe(styled_df)

    # -------------------------
    # Downloadable Reports
    # -------------------------

    pdf_file = "QA_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    # Title
    content.append(
        Paragraph(
            "AI Packaging Compliance Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1,12))

    # Package Details
    content.append(
        Paragraph(
            f"<b>Vendor:</b> {vendor}",
            styles["Normal"]
        )
    )


    content.append(
        Paragraph(
            f"<b>Application:</b> {application}",
            styles["Normal"]
        )
    )


    content.append(
        Paragraph(
            f"<b>Version:</b> {version}",
            styles["Normal"]
        )
    )


    content.append(Spacer(1,12))

    # Executive Summary
    content.append(
        Paragraph(
            f"<b>Compliance Score:</b> {compliance}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Risk Level:</b> {risk}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Passed Checks:</b> {passed}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Failed Checks:</b> {failed}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1,12))

    # Failed Checks
    content.append(
        Paragraph(
            "Critical Findings",
            styles["Heading2"]
        )
    )


    for _, row in failed_df.iterrows():
        content.append(
            Paragraph(
                f"• {row['Check']} : {row['Remark']}",
                styles["Normal"]
            )
        )

    doc.build(content)

    with open(pdf_file, "rb") as f:

        st.download_button(
            "📄 Download Executive PDF",
            f,
            file_name=f"{application}_{version}_QA_Report.pdf"
        )
    

    csv = df.to_csv(
    index=False
    )

    st.download_button(
        "📊 Download CSV Report",
        csv,
        file_name=f"{application}_{version}_QA_Report.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.caption(
        "AI Packaging Compliance Assistant | Built with Python, Streamlit and Enterprise Packaging Automation"
    )