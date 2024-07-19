from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = 'sk-proj-quQ7bqUiQDviRy23FuYLT3BlbkFJTZRYYgOeS4y2HZjoPuGP'

@app.route('/api/filter', methods=['POST'])
def handle_filter():
    try:
        filter_data = request.json.get('filter')
        app.logger.info(f"Received filter data: {filter_data}")  # Debugging line
        prompt = f"Generate a description for the following filter data: {filter_data}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the appropriate model for your task
            messages=[
                {"role": "system", "content": "You are an assistant that generates descriptions for data."},
                {"role": "user", "content": prompt}
            ]
        )
        
        description = response.choices[0].message['content'].strip()
        app.logger.info(f"Generated description: {description}")  # Debugging line
        return jsonify({'description': description})
    except Exception as e:
        app.logger.error(f"Error: {e}")  # Debugging line
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)