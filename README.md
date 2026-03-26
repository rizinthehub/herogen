

# 📚 HeroGen — AI-Powered Personalized Storybook Generator

<p align="center">
  <img src="assets/HeroGenLogoText.png" alt="HeroGen Logo" width="300"/>
</p>

<p align="center">
  <strong>Be the Hero of Your Own Story</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue?style=flat-square&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?style=flat-square&logo=streamlit" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?style=flat-square&logo=openai" alt="OpenAI"/>
  <img src="https://img.shields.io/badge/DALL--E%203-Image%20Gen-412991?style=flat-square&logo=openai" alt="DALL-E 3"/>
  <img src="https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat-square&logo=mongodb" alt="MongoDB"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
</p>

---

## 🌟 What is HeroGen?

HeroGen is an AI-powered web application that generates **personalized educational storybooks** for children aged 4–8. Parents upload a child's photo, pick a moral theme, and the AI creates a complete storybook in under **90 seconds** — with illustrations, coloring pages, and a teacher's guide.

> **The Problem:** Kids prefer screens over books. Personalized books cost $30+ and take weeks to deliver.
>
> **Our Solution:** Instant, AI-generated storybooks with age-adapted text, interactive quizzes, and a complete educational package.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📖 **AI Story Generation** | GPT-4o-mini writes personalized 5-page stories with the child as the hero |
| 🎨 **AI Illustrations** | DALL-E 3 generates beautiful watercolor-style images for each page |
| 🧒 **LexiLevel Engine** | Automatically adjusts vocabulary complexity based on age (4-5, 6-7, 8) |
| 🤔 **Interactive Quizzes** | Each page has a moral-themed quiz question that must be answered to continue |
| 🖍️ **Coloring Pages** | Auto-generated black & white outlines from story illustrations |
| 📝 **Teacher's Guide** | Vocabulary words, discussion questions, classroom activities & learning objectives |
| 📥 **Edu-Pack PDF** | One-click download of complete storybook, coloring pages, and teacher's guide |
| 🛡️ **Face Cloning** | Optional Replicate InstantID integration for character face matching |

---

## 🖥️ Screenshots

<details>
<summary>Click to view screenshots</summary>

### Home Page
> Landing page with logo, tagline, and "How It Works" section

### Create Story
> Form to enter child's name, age, moral theme, and upload photo

### Story Reader
> Side-by-side image and text with interactive quiz and progress bar

### Dashboard
> Download storybook, coloring pages, and teacher's guide PDFs

</details>

---

## 🏗️ Tech Stack

```
Frontend:    Streamlit (Python)
AI Text:     OpenAI GPT-4o-mini
AI Images:   OpenAI DALL-E 3 / Replicate InstantID
Database:    MongoDB Atlas (Free Tier)
PDF Engine:  FPDF2 + Pillow
Hosting:     Streamlit Community Cloud (Free)
Version Control: Git + GitHub
```

---

## 📁 Project Structure

```
herogen/
├── main.py                  # App entry point & router
├── requirements.txt         # Python dependencies
├── .streamlit/
│   ├── config.toml          # Theme & server settings
│   └── secrets.toml         # API keys (not in repo)
├── assets/
│   ├── style.css            # Custom CSS theme
│   ├── HeroGenLogo.png      # Shield logo
│   └── HeroGenLogoText.png  # Logo with text
├── services/
│   ├── ai_text.py           # Story generation (OpenAI)
│   ├── ai_image.py          # Image generation (DALL-E 3 / Replicate)
│   ├── pdf_maker.py         # PDF generation (Storybook, Coloring, EduSheet)
│   └── db.py                # MongoDB connection & storage
└── views/
    ├── home.py              # Landing page
    ├── create.py            # Story creation form & loading screen
    ├── reader.py            # Interactive story reader with quizzes
    └── dashboard.py         # Download page for PDFs
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))
- MongoDB Atlas Account ([Free tier](https://www.mongodb.com/cloud/atlas/register))

### Setup

```bash
# Clone the repository
git clone https://github.com/rizinthehub/herogen.git
cd herogen

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure API Keys

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=sk-proj-your-key-here
REPLICATE_API_TOKEN=r8_your-token-here
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
```

### Run

```bash
streamlit run main.py
```

The app opens at `http://localhost:8501`

---

## 💰 Cost

| Service | Cost |
|---------|------|
| OpenAI (per story) | ~$0.21 |
| Replicate (optional) | ~$0.20 |
| MongoDB Atlas | Free |
| Streamlit Cloud | Free |
| **Total per story** | **~$0.21** |

---

## 🌐 Deployment

The app is deployed on **Streamlit Community Cloud**:

🔗 **Live App:** [herogen.streamlit.app](https://herogen-4mls8rwacmq34zv4vdqevp.streamlit.app)

To deploy your own:
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → Add secrets → Deploy

---

## 👥 Team

| Member | Role |
|--------|------|
| rizinthehub | Project Lead, Backend AI Services |
| Imaadh-Rushdee | PDF Engine, Database |
| kosaladathapththu | Frontend UI, Styling |
| Tharu127 | Testing, Documentation, Deployment |

**Course:** Higher Diploma in Software Engineering
**Institution:** National Institute of Business Management (NIBM)

---

## 📄 License

This project is licensed under the MIT License.

---

<p align="center">
  Made with ❤️ for little readers everywhere
</p>

