from flask import Flask, request, render_template, jsonify
import openai
from PyPDF2 import PdfReader
import os

app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = 'MY_API_KEY' # change openai key here

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def generate_slogan(company_concept, style):
    prompt = f"Du bist eine erfahrene und kreative Werbetexterin in einem Marketingunternehmen, das andere Unternehmen dabei unterstützt, passende Werbeslogans zu entwickeln. Ein neuer Kunde hat seinen Businessplan eingereicht und wünscht sich einen Werbeslogan, der seine Unternehmensphilosophie und Ziele widerspiegelt. Das Unternehmen möchte als innovativ, verantwortungsbewusst und trendbewusst wahrgenommen werden. Dein Ziel ist es, einen {style} Werbeslogan zu entwerfen, der die Aufmerksamkeit der Zielgruppe erregt und die Marke erfolgreich positioniert. Basierend auf dem folgenden Unternehmenskonzept, entwickle bitte einen Slogan: {company_concept}. Der Slogan sollte die Kernwerte des Unternehmens klar kommunizieren und bei der Zielgruppe Anklang finden."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Du bist ein kreativer Werbetexter."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    slogan = response.choices[0].message['content'].strip()
    return slogan

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_slogan', methods=['POST'])
def generate_slogan_route():
    pdf_file = request.files['companyConcept']
    slogan_style = request.form['sloganStyle']
    company_concept = extract_text_from_pdf(pdf_file)
    
    styles = {
        "kreativ": "kreativen und verrückten",
        "klassisch": "klassischen und formellen",
        "interessant": "interessanten und ansprechenden"
    }

    style = styles.get(slogan_style, "kreativen und verrückten")
    slogan = generate_slogan(company_concept, style)
    return jsonify({'slogan': slogan})

if __name__ == '__main__':
    app.run(debug=True)
