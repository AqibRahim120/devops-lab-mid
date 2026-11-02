from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

@app.route('/report', methods=['POST'])
def receive_report():
    try:
        report_data = request.json
        if not report_data:
            return jsonify({'error': 'No JSON payload received'}), 400

        # Save to test-report.json locally
        with open('test-report.json', 'w') as f:
            json.dump(report_data, f, indent=4)

        print("[INFO] Test report successfully received and saved as test-report.json")
        return jsonify({'status': 'success', 'message': 'Report saved successfully'}), 200
    except Exception as e:
        print(f"[ERROR] Failed to save report: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Runs locally on port 5000 (Expose this via Ngrok: `ngrok http 5000`)
    app.run(host='0.0.0.0', port=5000)