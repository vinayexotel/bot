# CSM Helper Bot

A Flask-based chatbot that looks up Customer Success Managers (CSM) for accounts using data from an Excel file.

## Features

- Look up CSM assignments by account name
- RESTful API endpoint for Google Chat integration
- Health check endpoint
- Production-ready with logging and error handling

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:8080`

## Deployment Options

### Option 1: Railway (Recommended - Easiest)

Railway provides automatic HTTPS, easy deployment, and a generous free tier.

1. **Install Railway CLI** (optional but helpful):
```bash
npm install -g @railway/cli
```

2. **Deploy to Railway**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Connect your GitHub repository
   - Railway will automatically detect the Dockerfile and deploy

3. **Get your HTTPS endpoint**:
   - After deployment, Railway will provide a URL like: `https://your-app-name.railway.app`
   - This URL will be your webhook endpoint for Google Chat

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Option 3: Heroku

1. Install Heroku CLI
2. Create a `Procfile`:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```
3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## API Endpoints

### POST /
Main webhook endpoint for Google Chat integration.

**Request Body:**
```json
{
  "message": {
    "text": "csm account_name"
  }
}
```

**Response:**
```json
{
  "text": "✅ CSM for 'account_name' is: John Doe"
}
```

### GET /
Health check endpoint.

**Response:**
```
CSMHelperBot is running!
```

## Google Chat Integration

1. In Google Chat, go to the space where you want to add the bot
2. Click the space name → "Apps and integrations"
3. Click "Add webhook"
4. Enter your deployed HTTPS URL (e.g., `https://your-app-name.railway.app`)
5. Save the webhook

## Usage

In Google Chat, users can type:
- `csm account_name` - Look up CSM for a specific account
- Any other message will return usage instructions

## Environment Variables

- `PORT` - Port number (automatically set by cloud platforms)

## File Structure

```
├── app.py              # Main Flask application
├── accounts.xlsx       # Excel file with account-CSM mappings
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── railway.json       # Railway deployment config
└── README.md          # This file
```

## Troubleshooting

1. **Excel file not found**: Make sure `accounts.xlsx` is in the root directory
2. **Deployment fails**: Check that all files are committed to your repository
3. **Bot not responding**: Verify the webhook URL is correct and the service is running

## Security Notes

- The current implementation loads the Excel file into memory on startup
- Consider using environment variables for sensitive data in production
- Add authentication if needed for your use case 