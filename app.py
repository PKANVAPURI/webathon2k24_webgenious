from flask import Flask, render_template, request, redirect, url_for
from PyPDF2 import PdfReader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'pdf_file' not in request.files:
            return redirect(request.url)
        pdf_file = request.files['pdf_file']

        # If the user does not select a file, browser also
        # submit an empty part without filename
        if pdf_file.filename == '':
            return redirect(request.url)
        
        if pdf_file:
            pdf_reader = PdfReader(pdf_file)
            extracted_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                extracted_text += page.extract_text()

            # Redirect to display page with extracted text
            return redirect(url_for('display_text', text=extracted_text))
    
    return render_template('index.html')

@app.route('/display')
def display_text():
    text = request.args.get('text', '')
    return render_template('display.html', text=text)

if __name__ == '__main__':
    app.run(debug=True)