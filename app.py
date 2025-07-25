from flask import Flask, request, jsonify
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Excel into memory
try:
    df = pd.read_excel("accounts.xlsx")  # Columns: Account Name | Account CSM
    df.columns = [c.strip() for c in df.columns]  # clean column names
    logger.info(f"Loaded {len(df)} accounts from Excel file")
except Exception as e:
    logger.error(f"Failed to load Excel file: {e}")
    df = pd.DataFrame(columns=["Account Name", "Account CSM"])

app = Flask(__name__)

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

            # Search in dataframe
            match = df[df["Account Name"].str.lower() == account_name]
            if not match.empty:
                csm_name = match["Account CSM"].iloc[0]
                reply = f"✅ CSM for '{account_name}' is: {csm_name}"
                logger.info(f"Found CSM: {csm_name}")
            else:
                reply = f"❌ No CSM linked with this Account."
                logger.info(f"No CSM found for account: {account_name}")

        return jsonify({"text": reply})
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"text": "Sorry, I encountered an error processing your request."}), 500


@app.route("/", methods=["GET"])
def healthcheck():
    return "CSMHelperBot is running!", 200

if __name__ == "__main__":
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get("PORT", 8080))
    # Run locally for testing
    app.run(host="0.0.0.0", port=port, debug=False)
