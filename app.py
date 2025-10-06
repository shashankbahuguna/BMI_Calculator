"""
HealthTrack Pro - Professional BMI Calculator
A secure, optimized Flask application for BMI calculation
"""

from flask import Flask, render_template, request, jsonify, session
from flask_wtf.csrf import CSRFProtect
from datetime import datetime, timedelta
from functools import wraps
import logging
import os

# Initialize Flask app with configurations
app = Flask(__name__, 
            static_url_path='/static',
            template_folder='templates')

# ===================================
# CONFIGURATION
# ===================================
class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    MAX_CONTENT_LENGTH = 16 * 1024  # 16KB max request size
    
    # BMI Constants
    MIN_HEIGHT = 50.0
    MAX_HEIGHT = 300.0
    MIN_WEIGHT = 20.0
    MAX_WEIGHT = 500.0
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 30

app.config.from_object(Config)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Make Python built-in functions available in templates
app.jinja_env.globals.update(min=min, max=max, round=round)

# ===================================
# LOGGING CONFIGURATION
# ===================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('healthtrack.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ===================================
# MODELS / DATA STRUCTURES
# ===================================
class BMICategory:
    """BMI category definitions with thresholds and messages"""
    
    CATEGORIES = [
        {
            'name': 'Severely Underweight',
            'range': (0, 16),
            'message': 'Consult a healthcare provider immediately',
            'color': '#ef4444',
            'icon': 'exclamation-triangle',
            'health_risk': 'High'
        },
        {
            'name': 'Underweight',
            'range': (16, 18.5),
            'message': 'Consider consulting a nutritionist for a healthy diet plan',
            'color': '#3b82f6',
            'icon': 'info-circle',
            'health_risk': 'Moderate'
        },
        {
            'name': 'Normal Weight',
            'range': (18.5, 25),
            'message': 'Excellent! Maintain your healthy lifestyle',
            'color': '#10b981',
            'icon': 'check-circle',
            'health_risk': 'Low'
        },
        {
            'name': 'Overweight',
            'range': (25, 30),
            'message': 'Consider increasing physical activity and balanced diet',
            'color': '#f59e0b',
            'icon': 'exclamation-circle',
            'health_risk': 'Moderate'
        },
        {
            'name': 'Obese Class I',
            'range': (30, 35),
            'message': 'Consult a healthcare provider for weight management',
            'color': '#f97316',
            'icon': 'exclamation-triangle',
            'health_risk': 'High'
        },
        {
            'name': 'Obese Class II',
            'range': (35, 40),
            'message': 'Medical intervention recommended - consult a doctor',
            'color': '#dc2626',
            'icon': 'exclamation-triangle',
            'health_risk': 'Very High'
        },
        {
            'name': 'Obese Class III',
            'range': (40, 100),
            'message': 'Immediate medical attention required',
            'color': '#991b1b',
            'icon': 'ban',
            'health_risk': 'Extremely High'
        }
    ]
    
    @classmethod
    def get_category(cls, bmi):
        """Get BMI category based on value"""
        for category in cls.CATEGORIES:
            if category['range'][0] <= bmi < category['range'][1]:
                return category
        return cls.CATEGORIES[-1]  # Return highest category if out of range

# ===================================
# VALIDATORS
# ===================================
class InputValidator:
    """Validate and sanitize user inputs"""
    
    @staticmethod
    def validate_height(height):
        """Validate height input"""
        try:
            height = float(height)
            if not (Config.MIN_HEIGHT <= height <= Config.MAX_HEIGHT):
                raise ValueError(
                    f'Height must be between {Config.MIN_HEIGHT} and {Config.MAX_HEIGHT} cm'
                )
            return height
        except (ValueError, TypeError) as e:
            logger.warning(f'Invalid height input: {height}')
            raise ValueError('Please enter a valid height in centimeters')
    
    @staticmethod
    def validate_weight(weight):
        """Validate weight input"""
        try:
            weight = float(weight)
            if not (Config.MIN_WEIGHT <= weight <= Config.MAX_WEIGHT):
                raise ValueError(
                    f'Weight must be between {Config.MIN_WEIGHT} and {Config.MAX_WEIGHT} kg'
                )
            return weight
        except (ValueError, TypeError) as e:
            logger.warning(f'Invalid weight input: {weight}')
            raise ValueError('Please enter a valid weight in kilograms')
    
    @staticmethod
    def validate_gender(gender):
        """Validate gender input"""
        valid_genders = ['male', 'female']
        if gender not in valid_genders:
            logger.warning(f'Invalid gender input: {gender}')
            raise ValueError('Please select a valid gender')
        return gender

# ===================================
# BMI CALCULATOR SERVICE
# ===================================
class BMICalculator:
    """Core BMI calculation logic"""
    
    @staticmethod
    def calculate(height, weight):
        """
        Calculate BMI using the formula: weight (kg) / (height (m))^2
        
        Args:
            height (float): Height in centimeters
            weight (float): Weight in kilograms
            
        Returns:
            dict: BMI calculation results with category and recommendations
        """
        try:
            # Convert height from cm to meters
            height_in_meters = height / 100
            
            # Calculate BMI
            bmi = weight / (height_in_meters ** 2)
            bmi_rounded = round(bmi, 1)
            
            # Get category information
            category_info = BMICategory.get_category(bmi_rounded)
            
            # Calculate ideal weight range for this height
            ideal_weight_min = round(18.5 * (height_in_meters ** 2), 1)
            ideal_weight_max = round(24.9 * (height_in_meters ** 2), 1)
            
            # Calculate weight difference
            weight_difference = None
            if bmi_rounded < 18.5:
                weight_difference = round(ideal_weight_min - weight, 1)
                weight_action = 'gain'
            elif bmi_rounded > 25:
                weight_difference = round(weight - ideal_weight_max, 1)
                weight_action = 'lose'
            else:
                weight_action = 'maintain'
            
            result = {
                'bmi': bmi_rounded,
                'category': category_info['name'],
                'message': category_info['message'],
                'health_risk': category_info['health_risk'],
                'color': category_info['color'],
                'icon': category_info['icon'],
                'ideal_weight_range': {
                    'min': ideal_weight_min,
                    'max': ideal_weight_max
                },
                'weight_difference': weight_difference,
                'weight_action': weight_action,
                'bmi_display_percentage': min(max((bmi_rounded - 15) / 25 * 100, 0), 100)
            }
            
            logger.info(f'BMI calculated successfully: {bmi_rounded} - {category_info["name"]}')
            return result
            
        except ZeroDivisionError:
            logger.error('Division by zero in BMI calculation')
            raise ValueError('Invalid height value - cannot be zero')
        except Exception as e:
            logger.error(f'BMI calculation error: {str(e)}')
            raise ValueError('Error calculating BMI. Please check your inputs.')

# ===================================
# RATE LIMITING
# ===================================
def rate_limit():
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Initialize rate limit tracking
            if 'requests' not in session:
                session['requests'] = []
                session['requests_start'] = datetime.now().timestamp()
            
            # Clean old requests (older than 1 minute)
            current_time = datetime.now().timestamp()
            session['requests'] = [
                req for req in session['requests'] 
                if current_time - req < 60
            ]
            
            # Check rate limit
            if len(session['requests']) >= Config.MAX_REQUESTS_PER_MINUTE:
                logger.warning('Rate limit exceeded')
                return render_template(
                    'index.html',
                    error='Too many requests. Please wait a moment and try again.',
                    bmi=None,
                    bmi_category=None,
                    bmi_message=None
                ), 429
            
            # Add current request
            session['requests'].append(current_time)
            session.modified = True
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ===================================
# ROUTES
# ===================================
@app.route('/', methods=['GET', 'POST'])
@rate_limit()
def index():
    """Main route for BMI calculator"""
    
    # Initialize response variables
    error = None
    result = None
    
    if request.method == 'POST':
        try:
            # Get and validate form inputs
            height_input = request.form.get('height', '').strip()
            weight_input = request.form.get('weight', '').strip()
            gender_input = request.form.get('gender', 'male').strip().lower()
            
            # Validate inputs
            height = InputValidator.validate_height(height_input)
            weight = InputValidator.validate_weight(weight_input)
            gender = InputValidator.validate_gender(gender_input)
            
            # Calculate BMI
            result = BMICalculator.calculate(height, weight)
            result['gender'] = gender
            result['height'] = height
            result['weight'] = weight
            
            # Store in session for history (optional feature)
            if 'bmi_history' not in session:
                session['bmi_history'] = []
            
            session['bmi_history'].append({
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'bmi': result['bmi'],
                'category': result['category']
            })
            
            # Keep only last 10 calculations
            session['bmi_history'] = session['bmi_history'][-10:]
            session.modified = True
            
            logger.info(f'BMI calculation completed for height: {height}, weight: {weight}')
            
        except ValueError as e:
            error = str(e)
            logger.warning(f'Validation error: {error}')
            
        except Exception as e:
            error = 'An unexpected error occurred. Please try again.'
            logger.error(f'Unexpected error in BMI calculation: {str(e)}')
    
    return render_template(
        'index.html',
        error=error,
        result=result,
        bmi=result['bmi'] if result else None,
        bmi_category=result['category'] if result else None,
        bmi_message=result['message'] if result else None,
        bmi_data=result  # Full result object for advanced display
    )

@app.route('/api/calculate', methods=['POST'])
@csrf.exempt  # Only if you want to allow external API access
def api_calculate():
    """API endpoint for BMI calculation (returns JSON)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate inputs
        height = InputValidator.validate_height(data.get('height'))
        weight = InputValidator.validate_weight(data.get('weight'))
        gender = InputValidator.validate_gender(data.get('gender', 'male'))
        
        # Calculate BMI
        result = BMICalculator.calculate(height, weight)
        result['gender'] = gender
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
        
    except Exception as e:
        logger.error(f'API error: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'An error occurred processing your request'
        }), 500

@app.route('/history')
def history():
    """View BMI calculation history"""
    history_data = session.get('bmi_history', [])
    return render_template('history.html', history=history_data)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear BMI calculation history"""
    session.pop('bmi_history', None)
    return jsonify({'success': True, 'message': 'History cleared'})

# ===================================
# ERROR HANDLERS
# ===================================
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    logger.warning(f'404 error: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f'500 error: {str(error)}')
    return render_template('500.html'), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'Request too large'}), 413

# ===================================
# SECURITY HEADERS
# ===================================
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data:;"
    )
    return response

# ===================================
# TEMPLATE FILTERS
# ===================================
@app.template_filter('format_date')
def format_date(date_string):
    """Format date string for display"""
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M')
        return date_obj.strftime('%B %d, %Y at %I:%M %p')
    except:
        return date_string

# ===================================
# CONTEXT PROCESSORS
# ===================================
@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'app_name': 'HealthTrack Pro',
        'current_year': datetime.now().year,
        'version': '2.0.0'
    }

# ===================================
# MAIN EXECUTION
# ===================================
if __name__ == '__main__':
    # Check if running in production
    is_production = os.environ.get('FLASK_ENV') == 'production'
    
    if is_production:
        logger.info('Starting HealthTrack Pro in PRODUCTION mode')
        # Use a production WSGI server like Gunicorn in production
        # gunicorn -w 4 -b 0.0.0.0:8000 app:app
        app.run(host='0.0.0.0', port=8000, debug=False)
    else:
        logger.info('Starting HealthTrack Pro in DEVELOPMENT mode')
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=True
        )
