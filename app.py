from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import re

app = Flask(__name__)
app.secret_key = 'devops_lab_mid_secret_key'

# In-memory database for submissions
submissions = []

def is_valid_url(url):
    regex = re.compile(
        r'^(https?):\/\/'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?(?:$|[/?#])', re.IGNORECASE)
    return bool(regex.match(url))

@app.route('/')
def index():
    return render_template('index.html', submissions=submissions)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    reg_no = request.form.get('reg_no', '').strip()
    title = request.form.get('title', '').strip()
    url = request.form.get('url', '').strip()

    # Validation: Missing registration number
    if not reg_no:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return jsonify({'error': 'Registration number is required'}), 400
        flash('Error: Registration number is required!', 'danger')
        return redirect(url_for('index'))

    # Validation: Missing required fields
    if not name or not title or not url:
        flash('Error: All fields are required!', 'danger')
        return redirect(url_for('index'))

    # Validation: Invalid submission URL
    if not is_valid_url(url):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return jsonify({'error': 'Invalid submission URL'}), 400
        flash('Error: Invalid submission URL format!', 'danger')
        return redirect(url_for('index'))

    # Save valid submission
    submission_entry = {
        'name': name,
        'reg_no': reg_no,
        'title': title,
        'url': url
    }
    submissions.append(submission_entry)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return jsonify({'message': 'Submission saved successfully'}), 200

    flash('Assignment submitted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/api/submissions', methods=['GET'])
def get_submissions():
    return jsonify(submissions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)