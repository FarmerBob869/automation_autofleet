from flask import Flask, jsonify
import subprocess
import os

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

@app.route('/get-results', methods=['GET'])
def get_results():
    """Get the contents of the generated_multiple_uuids.txt file."""
    try:
        if not os.path.isfile("generated_multiple_uuids.txt"):
            raise FileNotFoundError("generated_multiple_uuids.txt not found")
        with open("generated_multiple_uuids.txt", "r") as file:
            uuids = file.readlines()
        return jsonify({
            'status': 'success',
            'uuids': [uuid.strip() for uuid in uuids]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-test-logs', methods=['GET'])
def get_test_logs():
    """Get the contents of the test log file."""
    try:
        log_file_path = "test_logs.txt"
        if not os.path.isfile(log_file_path):
            raise FileNotFoundError(f"{log_file_path} not found")
        with open(log_file_path, "r") as file:
            logs = file.readlines()
        return jsonify({
            'status': 'success',
            'logs': [log.strip() for log in logs]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get-test-results', methods=['GET'])
def get_test_results():
    """Get the contents of the test results file."""
    try:
        result_file_path = "test_results.txt"
        if not os.path.isfile(result_file_path):
            raise FileNotFoundError(f"{result_file_path} not found")
        with open(result_file_path, "r") as file:
            results = file.readlines()
        return jsonify({
            'status': 'success',
            'results': [result.strip() for result in results]
        }), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
