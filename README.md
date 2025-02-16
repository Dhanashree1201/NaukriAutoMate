# **NaukriAutoMate**  
*Your Personal Job Application Assistant for Naukri.com*  

**NaukriAutoMate** automates the job application process on **Naukri.com**, leveraging AI to match job descriptions (JD) and automatically answer questions during the application process. This Python script uses **Selenium WebDriver** for web navigation and the **Gemini AI API** for job description matching and answering application questions.

---

### **Key Features**

- **Auto Search & Apply for Jobs**: Automatically search and apply for jobs based on your job preferences (e.g., job title, location, experience).
- **Pagination Support**: Navigate through multiple pages of job listings for seamless application.
- **AI-Powered Question Answering**: Automatically answers application questions using the Gemini AI API.
- **Job Description Matching Using AI**: Matches job descriptions to your preferences and skills before applying.
- **Logging**: Tracks the count of successful and failed job applications.

---

## **Features**

- **Automates job applications on Naukri.com** based on user-defined preferences.
- **Auto-search and apply** for jobs by location, title, experience, etc.
- **Handles pagination** to go through multiple pages of job listings.
- **AI-driven job description matching** ensures the job fits your profile.
- **AI-powered question answering** for a smooth application process.
- **Logs success and failure** counts for tracking performance.

---

## **Prerequisites**

Before you begin, ensure you have the following:

- Python 3.x installed on your local machine.
- **Virtual environment** (venv) set up.
- **Gemini AI API credentials** ([Gemini AI API](https://ai.google.dev/gemini-api/docs/api-key)).

---

## **Setup Instructions**

1. **Clone the Repository**:  
   Clone the repository using Git:  
   ```bash
   git clone https://github.com/GoliathReaper/NaukriAutoMate.git
   ```

2. **Create a Virtual Environment**:  
   Navigate to the project directory and create a virtual environment:  
   ```bash
   cd NaukriAutoMate
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:  
   - On Windows:  
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:  
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:  
   Install the required Python libraries using `requirements.txt`:  
   ```bash
   pip install -r requirements.txt
   ```

5. **Download Geckodriver**:  
   Download **Geckodriver** from the [Geckodriver releases page](https://github.com/mozilla/geckodriver/releases) and extract the executable to a directory of your choice.

6. **Prepare Your Firefox Browser**:  
   Ensure you have Firefox installed and note the path to your Firefox executable and Firefox profile path.

7. **Configuration**:  
   Update the following variables in the script with the correct paths and settings:  
   ```python
   driver_path = "path_to_geckodriver_executable"
   binary = "path_to_firefox_executable"
   profile_path = "path_to_firefox_profile"
   ```

8. **Run the Script**:  
   Once everything is set up, run the script using:  
   ```bash
   python apply_jobs.py
   ```

---

## **Usage**

- Define your job preferences (title, location, experience, etc.) within the script.
- Run the script to auto-search and apply for jobs on Naukri.com.
- The script will handle multiple pages of job listings, AI job description matching, and answering application questions.

---

## **Enhancements in the Latest Version**

- **AI-Powered Job Description Matching**: Matches jobs based on your profile and preferences before applying.
- **Auto-Search & Apply**: Allows automatic job search and application using filters like job title, location, and experience.
- **AI-Driven Question Answering**: Automatically answers application questions with Gemini AI for a smoother process.
- **Pagination Support**: Automatically handles multiple pages of job listings.

---

## **Disclaimer**

- **Use responsibly**: Automating job applications may violate Naukri.com's terms of service and could result in account suspension or other consequences.  
- **Compliance**: Ensure you comply with Naukri.com's terms and conditions when using this script.

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request for any improvements, bug fixes, or feature requests.

---

## **SEO Keywords**

- **Auto Apply Naukri**  
- **Naukri.com Automation**  
- **Naukri Job Bot**  
- **Automated Job Search Naukri**  
- **AI Job Application Automation**  
- **Gemini AI Job Matching**  
- **Job Application Automation Naukri**  
- **Naukri Auto Apply Script**  
- **Job Search Bot for Naukri.com**  
- **Automate Naukri Applications**  

---

## **License**

This project is licensed under the MIT License.