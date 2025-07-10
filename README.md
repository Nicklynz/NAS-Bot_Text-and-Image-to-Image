# 🖼️ Discord AI Image Editing Bot

This is a Discord bot that uses **Google Gemini** (via the Generative AI SDK) to generate or edit images based on user prompts and attachments. Users can send a command along with an image and a description, and the bot will generate an edited version of the image using AI.

---

## 📦 Features

- `!start` — Starts the interaction with the bot
- `!help` — Shows command usage
- `!edit <description>` — AI edits the attached image based on the provided description
- Bot shows a "typing..." indicator while processing
- Sends a "Processing..." message that gets removed after image creation
- Automatically deletes temporary image files to save disk space

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/discord-ai-image-bot.git
cd discord-ai-image-bot
