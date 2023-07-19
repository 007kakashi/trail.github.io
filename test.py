from flask import Flask, request, render_template, session, jsonify
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your own secret key for session

# Function to load the existing data.csv file into a DataFrame and store it in the session
@app.before_request
def load_data():
    # Set a default value for the 'data' key in the session as an empty DataFrame
    session.setdefault('data', pd.DataFrame(columns=['Name', 'Email', 'Message']))
    
    try:
        data = pd.read_csv('data.csv', index_col=0)
    except FileNotFoundError:
        data = pd.DataFrame(columns=['Name', 'Email', 'Message'])
    # Convert DataFrame to list of dictionaries before storing it in the session
    session['data'] = data.to_dict('records')

# Route for displaying a simple form (GET method)
@app.route('/', methods=['GET'])
def show_form():
    return render_template('index.html')

# Route for processing the form data (POST method)
@app.route('/submit', methods=['POST'])
def process_form():
    Name = request.form.get('name')
    Email = request.form.get('email')
    Message = request.form.get('message')

    # Retrieve the data from the session and convert it back to DataFrame
    data = pd.DataFrame(session['data'])
    
    # Append the new data to the DataFrame
    new_data = {'Name': Name, 'Email': Email, 'Message': Message}
    # data_to_append = pd.DataFrame(new_data, index=[len(data) + 1])
    data = pd.concat([data,pd.DataFrame(new_data,index=[1])])

    # Save the updated DataFrame to the data.csv file
    data.to_csv('data.csv', index_label='Index')

    # Convert DataFrame to list of dictionaries before storing it in the session
    session['data'] = data.to_dict('records')

    # You can perform further processing with the form data here
    # For simplicity, we'll just print the data
    print(f"Name: {Name}, Email: {Email}, Message: {Message}")

    return render_template('thank.html')

# Route to get the data as JSON (optional)
@app.route('/get_data', methods=['GET'])
def get_data():
    # Retrieve the data from the session
    data = pd.DataFrame(session['data'])

    # Convert DataFrame to JSON format and send as the response
    return jsonify(data.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)
