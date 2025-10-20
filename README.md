# HireSight - ATS Resume Analyzer 🚀

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-red.svg)](https://streamlit.io)
[![spaCy](https://img.shields.io/badge/spaCy-3.7%2B-brightgreen.svg)](https://spacy.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An intelligent web application built to optimize your resume for modern Applicant Tracking Systems (ATS). Upload your CV, get an instant score, and receive actionable feedback to land your dream job.

---

### 

## ✨ Key Features

- **🎯 Instant ATS Score:** Get a percentage-based score that reflects your resume's compatibility and keyword optimization.
- **💡 Actionable Feedback:** Receive personalized, data-driven recommendations on how to improve your score and content.
- **🧠 Intelligent Parsing:** Automatically extracts and displays key information, including:
  - 👤 Personal & Professional Details
  - 🎓 Education History
  - 🛠️ Key Skills (as interactive tags)
  - 💼 Professional Experience
  - 🚀 Projects
- **🎨 Modern & Responsive UI:** A clean, attractive, and user-friendly interface powered by Streamlit.
- **🔒 Secure & Private:** Your resume is processed in real-time and is never stored or shared.



<img width="1858" height="689" alt="Screenshot 2025-10-20 181307" src="https://github.com/user-attachments/assets/49e0ce1b-c4c0-4613-8c5d-a05f17d1aabc" />
<img width="1742" height="914" alt="Screenshot 2025-10-20 181319" src="https://github.com/user-attachments/assets/100fa601-ff87-4fe8-8d7a-8097a6bd1397" />
<img width="1858" height="950" alt="Screenshot 2025-10-20 181339" src="https://github.com/user-attachments/assets/2e192870-0bff-416f-9dc7-ddc79c2ae25e" />
<img width="1685" height="526" alt="Screenshot 2025-10-20 181352" src="https://github.com/user-attachments/assets/bd3fc19a-3923-4d5b-9442-52a17d320291" />













## 🛠️ Tech Stack

<img width="1860" height="972" alt="Screenshot 2025-10-20 165154" src="https://github.com/user-attachments/assets/095d3a77-011d-45fb-a276-483d27253343" />
<img width="1746" height="814" alt="Screenshot 2025-10-20 164129" src="https://github.com/user-attachments/assets/115fc33f-16f4-422f-b15b-3a3f33e1aa30" />


HireSight leverages a powerful Python backend to perform its analysis. The core components are:

- **Frontend:** [Streamlit](https://streamlit.io/)
- **PDF Parsing:** [pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- **Natural Language Processing:** [spaCy](https://spacy.io/)
- **Deployment:** [Streamlit Community Cloud](https://streamlit.io/cloud)

## 🚀 Getting Started

Follow these instructions to get a local copy up and running for development and testing purposes.

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/HireSight.git
    cd HireSight
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run streamlit_app.py
    ```
    Your browser will automatically open with the application running!

## Usage

1. Launch the application using the command above.
2. Click the "Browse files" button to upload your resume in PDF format.
3. Wait for the analysis to complete.
4. Review your ATS score, feedback, and the extracted information.

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE.md` for more information.
