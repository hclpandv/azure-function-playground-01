import azure.functions as func
from google import genai
import os
import logging

app = func.FunctionApp()

# Configuration for Gemini API
GEMINI_MODEL = "gemini-2.0-flash-lite-preview-02-05"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FUNCTION_KEY = os.getenv("AZURE_FUNCTION_KEY")  # Securely fetch function key from environment

if not GEMINI_API_KEY:
    logging.error("GEMINI_API_KEY is not set in the environment.")

if not FUNCTION_KEY:
    logging.warning("AZURE_FUNCTION_KEY is not set. Ensure it is configured in the environment.")


def generate_gemini_response(prompt: str) -> str:
    """Helper function to generate a response from Gemini API."""
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text
    except Exception as e:
        logging.error("Error calling Gemini API: %s", e)
        raise


@app.route(route="gen_norsk_text", auth_level=func.AuthLevel.FUNCTION, methods=["GET"])
def gen_norsk_text(req: func.HttpRequest) -> func.HttpResponse:
    """Generate a beginner-friendly Norwegian text."""
    logging.info("Processing request for gen_norsk_text.")

    prompt = (
        "Please generate a beginner-friendly Norwegian paragraph for learning. "
        "It should be around 10 sentences and in the form of a short story. "
        "The story should cover different grammar topics and introduce new vocabulary. "
        "Ensure each response is unique and does not repeat previous stories. "
        "Do not always use the title 'En dag i Oslo'; instead, vary the title to match the story. "
        "Return only the paragraph with a creative and varied title at the beginning."
    )

    try:
        generated_text = generate_gemini_response(prompt)
        return func.HttpResponse(generated_text, status_code=200, mimetype="text/plain")
    except Exception:
        return func.HttpResponse("Error generating Norwegian text.", status_code=500)


@app.route(route="eval_translation", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])
def eval_translation(req: func.HttpRequest) -> func.HttpResponse:
    """Evaluate the user's Norwegian translation."""
    logging.info("Processing request for eval_translation.")

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON payload.", status_code=400)

    original_text = req_body.get("original_text")
    user_translation = req_body.get("user_translation")

    if not original_text or not user_translation:
        return func.HttpResponse(
            "Both 'original_text' and 'user_translation' are required.",
            status_code=400
        )

    evaluation_prompt = (
        "Evaluate the following translation. \n\n"
        f"Original text:\n{original_text}\n\n"
        f"User translation:\n{user_translation}\n\n"
        "Provide feedback on the accuracy, fluency, and errors in the translation."
    )

    try:
        evaluation_result = generate_gemini_response(evaluation_prompt)
        return func.HttpResponse(evaluation_result, status_code=200, mimetype="text/plain")
    except Exception:
        return func.HttpResponse("Error evaluating the translation.", status_code=500)


@app.route(route="serve_html", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET"])
def serve_html(req: func.HttpRequest) -> func.HttpResponse:
    """Serve the HTML page for user interaction."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Norwegian Learning</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f2f2f2;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            h1 {{
                color: #333;
            }}
            button {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                margin: 10px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }}
            button:hover {{
                background-color: #45a049;
            }}
            textarea {{
                width: 100%;
                max-width: 600px;
                padding: 10px;
                margin: 10px 0;
                border-radius: 4px;
                border: 1px solid #ccc;
                font-size: 16px;
            }}
            p {{
                max-width: 600px;
                background: #fff;
                padding: 10px;
                border-radius: 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .container {{
                width: 100%;
                max-width: 700px;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
        </style>
        <script>
            async function generateText() {{
                try {{
                    const response = await fetch('/api/gen_norsk_text?code=' + getFunctionKey());
                    const text = await response.text();
                    document.getElementById("generatedText").innerText = text;
                    document.getElementById("originalText").value = text;
                }} catch (error) {{
                    alert("Error generating text.");
                }}
            }}

            async function evaluateTranslation() {{
                const originalText = document.getElementById("originalText").value;
                const userTranslation = document.getElementById("userTranslation").value;

                if (!userTranslation) {{
                    alert("Please enter your translation.");
                    return;
                }}

                try {{
                    const response = await fetch('/api/eval_translation?code=' + getFunctionKey(), {{
                        method: "POST",
                        headers: {{ "Content-Type": "application/json" }},
                        body: JSON.stringify({{ original_text: originalText, user_translation: userTranslation }})
                    }});
                    const evaluation = await response.text();
                    document.getElementById("evaluationResult").innerText = evaluation;
                }} catch (error) {{
                    alert("Error evaluating translation.");
                }}
            }}
            
            function getFunctionKey() {{
                return "{FUNCTION_KEY}";
            }}
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Norwegian Learning App</h1>

            <button onclick="generateText()">Generate Norwegian Text</button>
            <p id="generatedText"></p>

            <h3>Your Translation:</h3>
            <textarea id="userTranslation" rows="5" placeholder="Enter your translation here..."></textarea>

            <input type="hidden" id="originalText">

            <button onclick="evaluateTranslation()">Evaluate Translation</button>

            <h3>Evaluation Feedback:</h3>
            <p id="evaluationResult"></p>
        </div>
    </body>
    </html>
    """
    return func.HttpResponse(html_content, status_code=200, mimetype="text/html")
