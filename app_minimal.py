from flask import Flask, request, jsonify
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app
app = Flask(__name__)

# Sample data (no external file dependency)
SAMPLE_DATA = {
    "sample_account": "John Doe",
    "test_company": "Jane Smith",
    "demo_corp": "Bob Johnson"
}

@app.route("/health", methods=["GET"])
def healthcheck():
    logger.info("Health check requested")
    return "CSMHelperBot is running!", 200

@app.route("/", methods=["GET"])
def root():
    return "CSMHelperBot API - Use POST / for webhook integration", 200

@app.route("/", methods=["POST"])
def handle_chat():
    try:
        data = request.get_json(force=True)
        logger.info(f"Received request: {data}")

        # Extract message text from Google Chat JSON
        message_text = data.get("message", {}).get("text", "").strip()
        parts = message_text.split(maxsplit=1)

        # Default reply
        reply = "Usage: csm <Account Name>"

        if len(parts) >= 2 and parts[0].lower() == "csm":
            account_name = parts[1].strip().lower()
            logger.info(f"Looking up CSM for account: {account_name}")

            # Search in sample data
            if account_name in SAMPLE_DATA:
                csm_name = SAMPLE_DATA[account_name]
                reply = f"✅ CSM for '{account_name}' is: {csm_name}"
                logger.info(f"Found CSM: {csm_name}")
            else:
                reply = f"❌ No CSM linked with this Account."
                logger.info(f"No CSM found for account: {account_name}")

        return jsonify({"text": reply})
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"text": "Sorry, I encountered an error processing your request."}), 500

if __name__ == "__main__":
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting CSMHelperBot on port {port}")
    # Run locally for testing
    app.run(host="0.0.0.0", port=port, debug=False) 