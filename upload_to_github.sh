#!/bin/bash

# GitHub upload script for Polyglot Podcaster
# Usage: ./upload_to_github.sh YOUR_GITHUB_USERNAME

if [ $# -eq 0 ]; then
    echo "❌ Error: Please provide your GitHub username"
    echo "Usage: ./upload_to_github.sh YOUR_USERNAME"
    exit 1
fi

USERNAME=$1
REPO_NAME="polyglot-podcaster"

echo "🚀 Uploading Polyglot Podcaster to GitHub..."
echo "Username: $USERNAME"
echo "Repository: $REPO_NAME"
echo ""

# Add remote
echo "📡 Adding GitHub remote..."
git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"

# Push to GitHub
echo "⬆️ Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully uploaded to GitHub!"
echo "🌐 Visit: https://github.com/$USERNAME/$REPO_NAME"
echo ""
echo "📖 Don't forget to:"
echo "   - Add a repository description"
echo "   - Make it public or private as desired"
echo "   - Add topics: streamlit, ai, voice-cloning, multilingual"