from flask import Flask, request, jsonify
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize app first
app = Flask(__name__)

# Global variable for dataframe
df = None

def load_data():
    """Load Excel data - called on first request"""
    global df
    if df is not None:
        return df
    
    try:
        df = pd.read_excel("accounts.xlsx")  # Columns: Account Name | Account CSM
        df.columns = [c.strip() for c in df.columns]  # clean column names
        logger.info(f"Loaded {len(df)} accounts from Excel file")
    except Exception as e:
        logger.error(f"Failed to load Excel file: {e}")
        # Create a sample dataframe if Excel file is not available
        df = pd.DataFrame({
            "Account Name": ["sample_account", "test_company"],
            "Account CSM": ["John Doe", "Jane Smith"]
        })
        logger.info("Using sample data due to Excel file error")
    
    return df

@app.route("/", methods=["POST"])
def handle_chat():
    try:
        data = request.get_json(force=True)
        logger.info(f"Received request: {data}")

        # Load data on first request
        df = load_data()

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


@app.route("/health", methods=["GET"])
def healthcheck():
    return "CSMHelperBot is running!", 200

@app.route("/", methods=["GET"])
def root():
    return "CSMHelperBot API - Use POST / for webhook integration", 200

if __name__ == "__main__":
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting CSMHelperBot on port {port}")
    # Run locally for testing
    app.run(host="0.0.0.0", port=port, debug=False)
