from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run-tests', methods=['GET'])
def run_tests():
    """Trigger the Selenium test suite."""
    try:
        # Run tests using pytest and capture output
        result = subprocess.run(['pytest', '--tb=short'], capture_output=True, text=True)
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
