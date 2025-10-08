# 🧮 Advanced Health Metrics Calculator (BMI, BMR, TDEE)

This is a professional, feature-rich web application built using *Python Flask* for the backend logic and *HTML, **Bootstrap 5, and **JavaScript* for a responsive, modern frontend with a *Dark Mode* feature.

It calculates the following key health metrics:

- *Body Mass Index (BMI)*: A measure of body fat based on height and weight.
- *Basal Metabolic Rate (BMR)*: The calories required to keep your body functioning at rest.
- *Total Daily Energy Expenditure (TDEE)*: The estimated calories burned per day, based on your BMR and activity level.

---

## 🚀 How to Run the Application (VS Code Guide)

Follow these steps to set up and run the project locally.

### 1. Project Setup and File Structure

Ensure all the provided code files are organized into the correct directories:

### 2. Prepare the Python Environment

Using a virtual environment is essential for managing project dependencies.

*Open the Integrated Terminal:*
- In VS Code, open the main project folder (bmi_calculator).
- Go to *Terminal > New Terminal* (Shortcut: Ctrl+')

*Create a Virtual Environment:*

Run the appropriate command below:

- *Windows:* python -m venv venv
- *macOS/Linux:* python3 -m venv venv

*Activate the Environment:*

Run the appropriate command below. You should see (venv) appear in your terminal prompt.

- *Windows (Command Prompt):* .\venv\Scripts\activate
- *Windows (PowerShell):* .\venv\Scripts\Activate.ps1
- *macOS/Linux:* source venv/bin/activate

*Install Flask:*

Install the necessary web framework dependency.
### 3. Run the Flask Server

With the environment activated and Flask installed, you can start the application.

*Set the Flask Application Entry Point:*

This tells Flask which file to run.

- *Windows (Command Prompt):* set FLASK_APP=app.py
- *Windows (PowerShell):* $env:FLASK_APP="app.py"
- *macOS/Linux:* export FLASK_APP=app.py

*Start the Server:*
The terminal will output the local development URL.

*Access the App:*

Open your web browser and navigate to the address shown in the terminal (usually http://127.0.0.1:5000/).

---

### 4. Stopping the Server

To stop the running application, go back to your VS Code terminal and press: Ctrl+C

---

## ✨ Key Features

- *Professional UI*: Built using Bootstrap 5 for a clean, modern, and responsive design.
- *Dark Mode*: Client-side toggle button to switch between light and dark themes.
- *Unit System Switch*: Supports Metric (kg, m/cm) and Imperial (lb, in) units with automatic conversion in the Python backend.
- *Height Options*: Choose between meters or centimeters when using the metric system.
- *Advanced Metrics*: Calculates and displays BMR and TDEE based on optional inputs (Age, Gender, Activity Level).
- *Color-Coded Feedback*: BMI category is highlighted using color-coded Bootstrap badges (e.g., green for Normal Weight).
- *Responsive Design*: Works seamlessly on desktop, tablet, and mobile devices.
- *Smooth Animations*: Professional transitions and hover effects for better user experience.
- *Local Storage*: Dark mode preference is saved and persists across sessions.

---

## 📊 Health Metrics Explained

### BMI (Body Mass Index)
- *Formula*: BMI = weight (kg) / height (m)²
- *Categories*:
  - Under 18.5: Underweight
  - 18.5 - 24.9: Normal Weight
  - 25.0 - 29.9: Overweight
  - 30.0+: Obesity

### BMR (Basal Metabolic Rate)
- *Formula*: Mifflin-St Jeor Equation
  - Men: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
  - Women: BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161

### TDEE (Total Daily Energy Expenditure)
- *Formula*: TDEE = BMR × Activity Multiplier
- *Activity Levels*:
  - Sedentary (1.2): Little or no exercise
  - Lightly Active (1.375): Exercise 1-3 days/week
  - Moderately Active (1.55): Exercise 3-5 days/week
  - Very Active (1.725): Exercise 6-7 days/week
  - Extra Active (1.9): Intense exercise 2x/day

---

## 🛠 Technologies Used

- *Backend*: Python, Flask
- *Frontend*: HTML5, CSS3, JavaScript (ES6+)
- *Styling*: Bootstrap 5, Custom CSS with CSS Variables
- *Icons*: Font Awesome 6
- *Fonts*: Google Fonts (Inter)

---

## 🔧 Troubleshooting

*Issue: Flask is not recognized*
- Solution: Make sure you've activated the virtual environment and installed Flask.

*Issue: Template not found*
- Solution: Ensure index.html is inside the templates/ folder.

*Issue: Static files not loading*
- Solution: Ensure style.css and script.js are inside the static/ folder.

*Issue: Port already in use*
- Solution: Run Flask on a different port: flask run --port 5001

---

## 📝 Notes

- All data is processed locally; no information is stored on servers.
- The calculator provides estimates. Always consult healthcare professionals for personalized medical advice.
- The application follows modern web development best practices with responsive design and accessibility considerations.

---

*Enjoy using the Advanced Health Metrics Calculator! 💪*
