from flask import Flask, render_template, request, jsonify
from flask import send_from_directory
# from ai_agent.agent import YourAIAgent  # Import your AI agent
from test_llm import Agent
# from state import get_initial_state
# from graph import run_graph
from enhanced_graph import run_graph
from enhanced_state import get_initial_state
import os,time
# from state import get_initial_state
# from graph import run_graph
import phase0.doc_parse_old as d
from typing import cast
from side_bar_hover import get_side
from werkzeug.utils import secure_filename
from slider_value import change_value,get_value
app = Flask(__name__)
app.config['SHARED_DATA'] ={'show_sidebar':get_side(),'slider_value': None }
# agent = Agent()  # Initialize your AI agent

SLIDER_VALUE = get_value()
global zone
zone="Upload your Invoice"
def change_zone(msg):
    global zone
    zone=msg
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
import clean_json as cjson

# def change_side():
#     app.config['SHARED_DATA']['show_sidebar'] = True
# def get_side():
#     return app.config['SHARED_DATA']['show_sidebar']

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    
    if not file or not file.filename:
        return jsonify({'error': 'No selected file'}), 400
   
    # Now it's safe to assume file.filename is a str
    filename = secure_filename(cast(str, file.filename))  # Type checker-friendly
    file_path = 'uploads/' + filename
    change_zone("File uploaded successfully")

    try:
        file.save(file_path)
        state =get_initial_state(file_path)
        # app.config['SHARED_DATA']['show_sidebar'] = True
        change_zone("Processing started...")
        result = run_graph(state)
        time.sleep(1)
        change_zone("Processing completed, Generating Report...")
        response=result
        time.sleep(2)
        change_zone("")
        # change_zone("")
        #changing 10/07/2025 13:31
        # data_to_send=d.extract_invoice_data(file_path) #calls the doc_parse.py
        # format_query="Extract the items,quantity and price from the invoice,return in a form which is best for jsonfiy function to work, with keys itemname,quantity,price for each item,most importantly check if the item included is a valid product name and not ambiguous.", data_to_send
        # response = Agent(format_query)
        # print("\nWaiting for response...\n")
        #
        # time.sleep(15)
        # app.config['SHARED_DATA']['data']=str(response)
        # print(response)
        # print(jsonify({"report": result["final_report"]}))
        # return jsonify({"report": result["final_report"]})
        # print('Dec',jsonify({f'"report": {state["final_report"]}'}))
        return jsonify({
            "report": state["final_report"]
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
    
    
@app.route('/response', methods=['POST', 'GET'])
def get_response():
    return cjson.clean(app.config['SHARED_DATA']['data']), 201


@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML template (templates\index.html)
@app.route('/upload.ico')
def serve_upload_icon():
    return send_from_directory('templates', 'upload.ico')
@app.route('/logo.png')
def serve_upload_m_icon():
    return send_from_directory('templates', 'logo.png')
@app.route('/status', methods=['GET'])
def stat():
    print(get_slider_value())
    # status_flag = app.config['SHARED_DATA'].get('show_sidebar', False)
    print("Here the value of flag ",get_side())
    status_flag = get_side()
    return jsonify({'show_sidebar': status_flag})


@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    user_input = data.get('message', '')
    
    # Process the input with your AI agent
    response = Agent(user_input)
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@app.route('/feedback',methods=['GET'])
def feed():
    global zone
    return jsonify({
            'zone':zone,
            'status': 'success'
        }), 200

@app.route('/user_input', methods=['POST'])  # Fixed: Added missing leading slash
def get_user_input():
    global SLIDER_VALUE  # Access global variable
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        # Get slider value from the request
        slider_value = data.get('slider_value', None)
        
        if slider_value is None:
            return jsonify({'error': 'No slider_value provided'}), 400
        
        # Store slider value globally for LangGraph access
        SLIDER_VALUE = slider_value
        change_value(slider_value)
        
        # Also store in shared data
        app.config['SHARED_DATA']['slider_value'] = slider_value
        
        print(f"Slider value received and stored: {slider_value}")  # Debug print
        
        return jsonify({
            'message': 'Slider value received successfully',
            'slider_value': slider_value,
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to process slider value: {str(e)}'}), 500

# Function to get slider value for LangGraph
def get_slider_value():
    """Function that LangGraph can call to get the current slider value"""
    global SLIDER_VALUE
    return SLIDER_VALUE






if __name__ == '__main__':
    app.run(debug=True, port=5000)
