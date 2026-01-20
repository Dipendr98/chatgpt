# 🚀 Deploy hackGPT to Railway

This guide will help you deploy hackGPT v23 to Railway.

## Prerequisites

- OpenAI API Key (get one from https://platform.openai.com/api-keys)
- Railway account (sign up at https://railway.app)

## Quick Deploy Steps

### 1. Create Railway Account
1. Go to https://railway.app
2. Sign up with GitHub (recommended) or email

### 2. Deploy from GitHub

#### Option A: Deploy via Railway Dashboard
1. Click "New Project" in Railway dashboard
2. Select "Deploy from GitHub repo"
3. Select your repository fork/clone
4. Select the branch: `claude/deploy-to-website-ukUtL`
5. Railway will automatically detect the Procfile and start deployment

#### Option B: Deploy via Railway CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Link to your GitHub repo
railway link

# Deploy
railway up
```

### 3. Configure Environment Variables

In Railway dashboard, add the following environment variable:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**To add environment variables:**
1. Go to your project in Railway
2. Click on your service
3. Go to "Variables" tab
4. Click "+ New Variable"
5. Add `OPENAI_API_KEY` with your OpenAI API key

### 4. Access Your App

Once deployed, Railway will provide you with a public URL like:
```
https://your-app-name.up.railway.app
```

You can also add a custom domain in Railway settings.

## Project Configuration

This project is already configured with:

- **Procfile**: Defines how to run the Streamlit app
  ```
  web: streamlit run hackGPTv23.py --server.port $PORT --server.address 0.0.0.0
  ```

- **runtime.txt**: Specifies Python version (3.10.12)

- **requirements.txt**: Lists all Python dependencies

## Troubleshooting

### Build Fails
- Check that all dependencies in requirements.txt are available
- Verify Python version compatibility
- Check Railway logs for specific error messages

### App Won't Start
- Ensure OPENAI_API_KEY is set in environment variables
- Check that the PORT environment variable is available (Railway sets this automatically)
- Review application logs in Railway dashboard

### API Key Issues
- Verify your OpenAI API key is valid
- Check that you have credits in your OpenAI account
- Ensure the key has proper permissions

## Alternative Deployment Options

### Streamlit Cloud
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Add OPENAI_API_KEY in "Advanced settings" → "Secrets"
   ```toml
   OPENAI_API_KEY = "your-key-here"
   ```
7. Click "Deploy"

### Render
1. Go to https://render.com
2. Create new Web Service
3. Connect your GitHub repository
4. Use these settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run hackGPTv23.py --server.port $PORT --server.address 0.0.0.0`
5. Add environment variable: `OPENAI_API_KEY`

## Updating Your Deployment

To update your deployed app:

```bash
# Make your changes
git add .
git commit -m "Update app"
git push origin claude/deploy-to-website-ukUtL
```

Railway will automatically detect the push and redeploy.

## Cost

- **Railway**: Generous free tier ($5 credit/month), then pay-as-you-go
- **Streamlit Cloud**: Free for public repositories
- **Render**: Free tier available with limitations

---

## Support

For issues specific to:
- **hackGPT**: Check https://github.com/NoDataFound/hackGPT
- **Railway**: Visit https://railway.app/help
- **OpenAI API**: Visit https://help.openai.com/
