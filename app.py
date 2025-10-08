from flask import Flask, render_template, request, jsonify

app = Flask(_name_)

# Activity Level Multipliers (for TDEE calculation)
ACTIVITY_MULTIPLIERS = {
    'sedentary': 1.2,
    'light': 1.375,
    'moderate': 1.55,
    'very_active': 1.725,
    'extra_active': 1.9
}

def get_bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "info"      # Bootstrap Blue
    elif 18.5 <= bmi < 24.9: return "Normal Weight", "success" # Bootstrap Green
    elif 25 <= bmi < 29.9: return "Overweight", "warning"  # Bootstrap Yellow
    else: return "Obesity", "danger"    # Bootstrap Red

# Optional Feature: BMR Calculation (Mifflin-St Jeor Equation)
def calculate_bmr(weight_kg, height_cm, age_years, gender):
    if gender == 'male':
        # BMR = 10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) + 5
        return (10 * weight_kg) + (6.25 * height_cm * 100) - (5 * age_years) + 5
    else: # female
        # BMR = 10 * weight (kg) + 6.25 * height (cm) - 5 * age (years) - 161
        return (10 * weight_kg) + (6.25 * height_cm * 100) - (5 * age_years) - 161

# Optional Feature: TDEE Calculation
def calculate_tdee(bmr, activity_level):
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2) # Default to sedentary
    return bmr * multiplier


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            data = request.get_json()
            # Core Inputs
            weight = float(data['weight'])
            height = float(data['height'])
            unit_system = data['unit']
            
            # Advanced Inputs
            age = int(data.get('age', 25)) # Default for BMR/TDEE
            gender = data.get('gender', 'male') # Default for BMR/TDEE
            activity_level = data.get('activity_level', 'sedentary') # Default for TDEE

            # --- Unit Conversion ---
            weight_kg = weight
            height_m = height
            
            if unit_system == 'imperial':
                weight_kg = weight * 0.453592   # lb to kg
                height_m = height * 0.0254      # in to m

            # Input validation (must be positive)
            if weight_kg <= 0 or height_m <= 0:
                return jsonify({'error': 'Height and weight must be positive values.'}), 400

            # --- Calculation ---
            bmi = round(weight_kg / (height_m ** 2), 2)
            category, color = get_bmi_category(bmi)
            
            # BMR and TDEE (Requires height in cm for formula)
            height_cm = height_m * 100
            bmr = round(calculate_bmr(weight_kg, height_cm, age, gender), 0)
            tdee = round(calculate_tdee(bmr, activity_level), 0)

            min_normal_weight = round(18.5 * (height_m ** 2), 1)
            max_normal_weight = round(24.9 * (height_m ** 2), 1)

            result = {
                'bmi': bmi,
                'category': category,
                'color': color,
                'recommendation': f"A normal BMI for your height is between {min_normal_weight:.1f} kg and {max_normal_weight:.1f} kg.",
                'bmr': int(bmr), # Optional Feature
                'tdee': int(tdee) # Optional Feature
            }
            return jsonify(result)

        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid input: {e}. Please ensure all fields are correctly filled.'}), 400
        except Exception as e:
            return jsonify({'error': f'An unexpected server error occurred: {str(e)}'}), 500

    return render_template("index.html")

if _name_ == "_main_":
    app.run(debug=True)
