import streamlit as st
from resumeparser import ats_extractor
import os
import time

# --- Custom CSS for Styling ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Main App Logic ---
def main():
    # --- Page Configuration ---
    st.set_page_config(
        page_title="ATS Resume Analyzer",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply custom styles
    # local_css("style.css") # Optional: If you have a separate CSS file

    # --- Header Section ---
    st.markdown("""
        <div style="text-align: center;">
            <h1>ATS Resume Analyzer 📄</h1>
            <p>Upload your resume in PDF format to see how it stacks up against Applicant Tracking Systems.</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # --- File Uploader ---
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        # --- Processing ---
        with st.spinner('Analyzing your resume... This might take a moment.'):
            # Save the uploaded file temporarily
            save_path = os.path.join("__DATA__", uploaded_file.name)
            os.makedirs("__DATA__", exist_ok=True)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract data and calculate score
            parsed_data = ats_extractor(save_path)
            time.sleep(2) # Simulate processing time

        # --- Display Results ---
        if "error" in parsed_data:
            st.error(f"An error occurred: {parsed_data['error']}")
        else:
            st.success("Resume parsed successfully!")

            # --- Score and Feedback Section ---
            score = parsed_data.get('score', 0)
            feedback = parsed_data.get('feedback', ["No feedback was generated."]) # Default feedback

            st.markdown("## ATS Score & Recommendations")
            
            # Create two columns for score gauge and feedback
            col1, col2 = st.columns([1, 2])

            with col1:
                 # Custom HTML/CSS for circular progress bar with color based on score
                if score >= 85:
                    color = "#4CAF50" # Green
                elif score >= 60:
                    color = "#FFC107" # Amber
                else:
                    color = "#F44336" # Red

                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="position: relative; width: 150px; height: 150px; margin: auto; background: conic-gradient({color} {score * 3.6}deg, #2c3e50 0deg); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="position: absolute; width: 120px; height: 120px; background: #0e1117; border-radius: 50%;"></div>
                        <span style="font-size: 2.5em; color: {color}; z-index: 1;">{score}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown("### How to improve your score:")
                for item in feedback:
                    st.markdown(f"- {item}")
            
            st.markdown("---")

            # --- Detailed Information Section ---
            st.markdown("## Extracted Information")
            
            # Personal & Professional Links in columns
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 👤 Personal Details")
                st.text(f"Name: {parsed_data.get('name', 'N/A')}")
                st.text(f"Email: {parsed_data.get('email', 'N/A')}")
                st.text(f"Mobile: {parsed_data.get('mobile_number', 'N/A')}")
            with col2:
                st.markdown("### 🌐 Professional Links")
                st.text(f"LinkedIn: {parsed_data.get('linkedin', 'N/A')}")
                st.text(f"GitHub: {parsed_data.get('github', 'N/A')}")

            # Education Section
            st.markdown("### 🎓 Education")
            if parsed_data.get('education'):
                for edu in parsed_data['education']:
                    st.markdown(f"- **{edu['degree']}** from {edu['institute']} ({edu['year']})")
            else:
                st.warning("No education details found.")
            
            # Skills Section
            st.markdown("### 🛠️ Skills")
            if parsed_data.get('skills'):
                # Display skills as tags
                skills_html = ''.join(f'<span style="background-color: #333; color: #eee; padding: 5px 10px; border-radius: 15px; margin: 3px;">{skill}</span>' for skill in parsed_data['skills'])
                st.markdown(skills_html, unsafe_allow_html=True)
            else:
                st.warning("No skills found.")

            # Projects Section
            with st.expander("🚀 View Projects"):
                if parsed_data.get('projects'):
                    for proj in parsed_data['projects']:
                        st.markdown(f"**{proj['title']}** | `{proj['date']}`")
                        st.markdown(proj['description'])
                        st.markdown("---")
                else:
                    st.info("No project details found.")
            
            # Experience Section
            with st.expander("💼 View Experience"):
                if parsed_data.get('experience'):
                    for exp in parsed_data['experience']:
                        st.markdown(f"**{exp['title']}** | `{exp['date']}`")
                        st.markdown(exp['description'])
                        st.markdown("---")
                else:
                    st.info("No experience details found.")

if __name__ == '__main__':
    main()

