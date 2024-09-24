from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import textwrap
from IPython.display import Markdown

# Function to format text to markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configuration of the API key
GOOGLE_API_KEY = "Add your Google API key"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model with a system instruction
instruction = """
You are an expert in waste management. I will provide you with detailed information about my daily and weekly routines. Based on this information, you will:

Calculate the amount and type of waste generated.
Provide detailed statistics on waste generation.
Offer actionable recommendations for reducing and managing waste effectively.
Here is how we will proceed:

I will describe my daily and weekly routines, including activities related to food consumption, household chores, office work, and any other relevant details.
You will analyze this information to estimate the amount and type of waste produced.
You will present statistics on the waste generated (e.g., in kilograms per day/week).
You will provide recommendations on best practices for waste reduction, recycling, and disposal.
Let's start with my daily routine:

Use this structure to provide your routines and then prompt the API to give you the relevant waste management analysis and recommendations. Here is an example interaction to guide you:

User:
Here's my daily routine:

Breakfast: Cereal and milk, coffee with a disposable cup.
Lunch: Sandwich from a deli, packaged in plastic wrap.
Dinner: Home-cooked meal, mostly vegetables, some meat, cooked in disposable aluminum trays.
Office work: Print about 10 pages per day, use a plastic water bottle.
Household chores: Take out the trash daily, mainly food waste and packaging.
GPT API:
Based on your daily routine, here is the estimated waste generation:

Disposable cup from coffee: 15g
Plastic wrap from sandwich: 5g
Disposable aluminum trays: 30g
Printed paper: 50g
Plastic water bottle: 10g
Food waste: 200g
Packaging: 100g
Total estimated waste per day: 410g

Here are some recommendations for reducing waste:

Use a reusable coffee cup instead of a disposable one.
Choose reusable packaging or bring your own container for your lunch.
Cook in reusable dishes instead of disposable aluminum trays.
Reduce printing by using digital documents where possible.
Switch to a reusable water bottle.
Compost food waste to reduce landfill waste and create nutrient-rich soil.
Would you like to provide your weekly routine or get more details on any of these points?
"""

model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=instruction)

app = Flask(__name__)

# Route to serve the chat app HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Generate response with the current chat history as context
    response = model.generate_content(
        user_message,
        safety_settings={
            'HATE': 'BLOCK_NONE',
            'HARASSMENT': 'BLOCK_NONE',
            'SEXUAL': 'BLOCK_NONE',
            'DANGEROUS': 'BLOCK_NONE'
        }
    )
    
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
