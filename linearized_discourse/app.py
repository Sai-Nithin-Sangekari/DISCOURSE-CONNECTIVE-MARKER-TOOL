from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_text = request.form['inputText']
    
    output_text = run_python_script(input_text)
    return output_text

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

def run_graph_script():
    graph_script_path = 'graph.py'
    dot_command = "dot -Tpng input.dot -o static/output.png"
    subprocess.run(['/usr/bin/python3', graph_script_path], capture_output=True, text=True)
    subprocess.run(dot_command, shell=True)

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

if __name__ == '__main__':
    app.run(debug=True)
