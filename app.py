import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, url_for, session, redirect, render_template

load_dotenv(".env")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
app = Flask(__name__)
if __name__ == "__main__":
    app.run(debug=True)

api = OpenAI(api_key=OPENAI_API_KEY)

def get_response(user_input):
    response = api.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal:firstaidmodel16:9Il0mv2b:ckpt-step-116",
        messages=[
            {"role": "system", "content": "Act as a nurse who gives suggestions for first aid."},
            {"role": "user", "content": user_input}
        ])
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('index.html', title="First Aid")

@app.route('/result', methods=['POST'])
def get_result():
    query = request.form['search_query']
    response = get_response(query)
    #result = response.choices[0].message.content
    return render_template('result.html', query=query, result=response)

#user_input = input()
#print(get_response(user_input))