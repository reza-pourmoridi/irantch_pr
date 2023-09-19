from flask import Flask, render_template, jsonify
from recommendation import index as recom_index  # Import the recommendation/index module
from modular import modular as modular_index


app = Flask(__name__)

@app.route('/home', methods=['GET'])
def home():
    header = render_template('header.html')
    footer = render_template('footer.html')
    return header + footer

@app.route('/recom-back-end', methods=['GET'])
def recom_back_end():
    # Execute the recommendation/index module's code for the '/recom-back-end' route
    return recom_index.run_app()

@app.route('/recom', methods=['GET'])
def recom():
    with open('recommendation/index.html', 'r') as index_file:
        index_html = index_file.read()
    header = render_template('header.html')
    footer = render_template('footer.html')
    full_html = header + index_html + footer
    return full_html

@app.route('/modular', methods=['GET'])
def modular():
    with open('modular/index.html', 'r') as index_file:
        index_html = index_file.read()
    header = render_template('header.html')
    footer = render_template('footer.html')
    full_html = header + index_html + footer
    return full_html

@app.route('/modular-back-end', methods=['GET'])
def modular_back_end():
    # Execute the recommendation/index module's code for the '/recom-back-end' route
    return modular_index.run_app()

@app.route('/upload', methods=['POST'])
def upload_file():
    # Execute the recommendation/index module's code for the '/recom-back-end' route
    return modular_index.upload_file()


if __name__ == '__main__':
    app.run(debug=True)
