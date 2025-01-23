from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, T5ForConditionalGeneration
import torch

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains (Security)

# Load FLAN-T5 model and tokenizer
MODEL_NAME = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("message")

        if not user_input:
            return jsonify({"error": "Message is required"}), 400

        prompt = f"Answer the following question: {user_input}"

        # Input von Model
        input_ids = tokenizer.encode_plus(
            prompt, 
            return_tensors="pt",
            max_length=512, 
            truncation=True
        ).input_ids

        # Output von Model
        output_ids = model.generate(
            input_ids, 
            max_length=200, 
            num_beams=5, 
            do_sample=True, 
            temperature=0.7 
        )

        response_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
