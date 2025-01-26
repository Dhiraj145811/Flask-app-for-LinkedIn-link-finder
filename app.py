from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to LinkedIn Finder App!"

@app.route('/get-linkedin', methods=['POST'])
def get_linkedin():
    data = request.json
    company_name = data.get('company_name')
    # Add your LinkedIn fetching logic here
    return jsonify({'linkedin_url': f'https://linkedin.com/company/{company_name.lower()}'})

if __name__ == '__main__':
    app.run(debug=True)
