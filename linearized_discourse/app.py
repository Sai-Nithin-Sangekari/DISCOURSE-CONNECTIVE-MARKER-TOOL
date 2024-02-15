from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import subprocess

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app)

# Function to read input sentences from file
def read_input_sentences():
    with open('input_web.txt', 'r') as input_file:
        return input_file.read().splitlines()

# Route to render the index.html template
@app.route('/')
def index():
    input_sentences = read_input_sentences()
    return render_template('index.html', input_sentences=input_sentences)

# Route to handle input processing
@app.route('/process_input', methods=['POST'])
def process_input():
    input_text = request.form['inputText']
    output_text = run_python_script(input_text)
    return output_text

# Route to handle discourse processing
@app.route('/process_discourse', methods=['POST'])
def process_discourse():
    input_text = request.form['output']
    result_text, relation_list = run_discourse_script(input_text)
    run_graph_script()
    output_data = {
        'result_text': result_text,
        'relation': relation_list
    }
    return jsonify(output_data)

# Function to run graph script
def run_graph_script():
    graph_script_path = 'graph.py'
    dot_command = "dot -Tpng input.dot -o static/output.png"
    subprocess.run(['/usr/bin/python3', graph_script_path], capture_output=True, text=True)
    subprocess.run(dot_command, shell=True)

# Function to run Python script
def run_python_script(input_text):  
    script_path = 'sentence_subparts.py'
    with open('sentence_input.txt', 'w') as result_file:
        result_file.write(input_text)
    result = subprocess.run(['/usr/bin/python3', script_path, input_text], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Subprocess failed with error: {result.stderr}")
    with open('sentence_output.txt', 'r') as result_file:
        result_text = result_file.read()
    return result_text

# Function to run discourse script
def run_discourse_script(input_text):
    script_path = 'discourse_Sent.py'
    with open('sentence_output.txt', 'w') as result_file:
        result_file.write(input_text)
    result_process = subprocess.run(['/usr/bin/python3', script_path], capture_output=True, text=True)
    if result_process.returncode != 0:
        raise Exception(f"Subprocess failed in discourse with error: {result_process.stderr}")
    with open('relation.txt', 'r') as result_file:
        relation = result_file.read()
    with open('sentence_output.txt', 'r') as result_file:
        result_text = result_file.read()
    relation_list = relation.split(',')
    return result_text, relation_list[:-1]

# SocketIO event handler to reload the page when input_web.txt changes
@socketio.on('reload')
def reload_page():
    input_sentences = read_input_sentences()
    socketio.emit('reload_template', {'input_sentences': input_sentences})

if __name__ == '__main__':
    socketio.run(app, debug=True)
