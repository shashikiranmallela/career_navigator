### ✨ **AI Career Navigator**

An AI-powered resume analysis tool to help you land your dream job. Get instant scores, skill detection, and personalized suggestions to elevate your resume\!

-----

### 🚀 **About the Project**

The job market is tough, and your resume is your first impression. The **AI Career Navigator** is a smart tool designed to give you a competitive edge. It's a full-stack application that acts as your personal career coach, analyzing your resume with advanced AI to provide actionable feedback.

  * **Front-end:** A smooth, animated web interface for a great user experience.
  * **Back-end:** A robust, high-performance API that does the heavy lifting.

-----

### 💻 **Tech Stack**

A fusion of powerful technologies working together to deliver a seamless experience.

#### **Front-end**

  * **HTML5**
  * **CSS3** (with modern variables and animations)
  * **JavaScript**

#### **Back-end**

  * **Python 3**
  * **FastAPI**: For a blazing-fast and efficient API.
  * **spaCy**: The heart of the AI analysis, handling all the NLP magic.
  * **PyMuPDF (`fitz`)**: For flawless text extraction from PDFs.
  * **`python-docx`**: For reading DOCX files.

-----

### ⚙️ **Key Features**

  * 📄 **Multi-Format Support**: Upload resumes in `.pdf`, `.docx`, or `.txt` formats.
  * 📊 **Smart Scoring**: Get an overall score out of 100 based on key resume metrics.
  * 🔍 **Detailed Breakdown**: See a score breakdown for different categories like `Skills`, `Experience`, and `Formatting`.
  * 🧠 **Intelligent Skill Detection**: The AI detects and lists relevant technical skills from your resume.
  * 💡 **Personalized Suggestions**: Receive custom tips to improve your resume and boost your score.
  * 🎨 **Sleek UI/UX**: Enjoy a modern and animated interface.

-----

### ▶️ **How to Run Locally**

Ready to take it for a spin? Follow these simple steps.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shashikiranmallela/career_navigator.git
    cd career_navigator
    ```

2.  **Set up the Back-end (Python):**

      * Create and activate a virtual environment.
      * Install the dependencies:
        ```bash
        pip install -r requirements.txt
        ```
      * Download the spaCy NLP model:
        ```bash
        python -m spacy download en_core_web_sm
        ```
      * Start the FastAPI server:
        ```bash
        uvicorn main:app --reload
        ```

3.  **Run the Front-end (Web):**

      * Simply open the `index.html` file in your browser. The JavaScript will automatically connect to your running back-end.

-----

### **License**

This project is licensed under the MIT License.

-----

### 🔗 **Connect with the Author**

  * **LinkedIn**: [Mallela Shashikiran](https://www.linkedin.com/in/mallelashashikiran/)
  * **GitHub**: [shashikiranmallela](https://github.com/shashikiranmallela)
