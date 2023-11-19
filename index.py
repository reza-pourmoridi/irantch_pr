from flask import Flask, render_template, jsonify
# from recommendation import index as recom_index  # Import the recommendation/index module
from modular import modular as modular_index
from update_data import update_main as up


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    header = render_template('header.html')
    footer = render_template('footer.html')
    return header + footer


@app.route('/modular', methods=['GET'])
def modular():
    with open('modular/index.html', 'r') as index_file:
        index_html = index_file.read()
    header = render_template('header.html')
    footer = render_template('footer.html')
    full_html = header + index_html + footer
    return full_html

@app.route('/update-data', methods=['GET'])
def update_data():
    with open('update_data/index.html', 'r') as index_file:
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


@app.route('/initiation_progress', methods=['POST'])
def initiation_progress():
    return modular_index.initiation_progress()

@app.route('/initiation_update', methods=['POST'])
def initiation_update():
    return up.initiation_update()

@app.route('/upload_styles', methods=['POST'])
def upload():
    return modular_index.upload()


if __name__ == '__main__':
    app.run(debug=True)
