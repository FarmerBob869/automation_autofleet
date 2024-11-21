from flask import Flask, jsonify



app = Flask(__name__)

@app.route('/run-tests', methods=['GET'])
def run_tests():
    """Trigger the Selenium test suite."""
    try:
        # Run tests using pytest and capture output
        result = subprocess.run(['pytest', '--tb=short', '--disable-warnings'], capture_output=True, text=True)
        
        # Write the test results to a file
        with open("test_results.txt", "w") as file:
            file.write(result.stdout)
            file.write(result.stderr)
        
        return jsonify({
            'status': 'success',
            'output': result.stdout,
            'errors': result.stderr
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
