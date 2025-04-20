# 🤖 Gemini Coding Agent

A simple AI-powered coding assistant that helps you write, debug, and run code using Google's Gemini API.

## ⚙️ Setup

1. **Clone the repo**  
```bash
git clone https://github.com/your-username/gemini-coding-agent.git
cd gemini-coding-agent
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Add your API key**  
Create a `.env` file and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. **Run the agent**  
```bash
python gemini.py
```

## 🧠 How It Works

- Understands your coding tasks
- Plans and breaks down steps
- Executes system commands
- Writes code files
- Gives step-by-step feedback

## 🔐 Note

Your `.env` file is already ignored by `.gitignore`.  
If you accidentally committed it:
```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -am "Removed .env from tracking"
```

---

Made with ❤️ by Om Tiwari
