# SyncType — Romanized Khmer → Khmer Script

A full-stack translator built with **FastAPI** (backend) and **React + Vite** (frontend) featuring a modern UI with dark/light mode support.

## 🎨 New Features

- ✨ Beautiful gradient design with dark/light theme toggle
- 🔍 Real-time translation suggestions as you type
- 📊 Confidence scoring for translations
- 🎯 Matched pattern display
- 🌓 Persistent theme preference
- ⚡ Smooth animations and transitions
- 📱 Fully responsive design

---

## 📁 Project Structure

```
synctype-integrated/
├── backend/
│   ├── main.py                  ← FastAPI app with new endpoints
│   ├── requirements.txt
│   ├── synctype-final/          ← MarianMT model weights
│   └── combined_dataset_v2.csv  ← Dictionary CSV
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx              ← UI
│   │   └── index.css
│   ├── public/
│   │   └── mylogo.svg           ← Logo
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── training_model/              ← Model training & fine-tuning
    ├── train.py
    ├── preprocessing.py
    └── datasets/
```

---

## 🚀 Setup Instructions

### 1️⃣ Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**

### 2️⃣ Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## 🔌 API Endpoints

### Original Endpoints (backward compatible)
- `GET  /`          → API info
- `GET  /health`    → Health check
- `POST /translate` → Original translation endpoint with `mode` parameter

### New Endpoints (for updated frontend)
- `POST /api/translate` → Translation with confidence scoring
  ```json
  {
    "text": "som sok sabay"
  }
  ```
  Response:
  ```json
  {
    "translation": "សុំសុខសប្បាយ",
    "confidence": 0.95,
    "matched_roman": "som sok sabay"
  }
  ```

- `POST /api/suggest` → Real-time suggestions
  ```json
  {
    "text": "som",
    "max_results": 5
  }
  ```
  Response:
  ```json
  {
    "suggestions": [
      {
        "roman": "som",
        "khmer": "សុំ",
        "confidence": 0.9
      }
    ]
  }
  ```

---

## 🎯 Features Breakdown

### Backend Features
- **Hybrid Translation Mode**: Dictionary lookup first, AI fallback for unknown words
- **Confidence Scoring**: Calculate translation confidence based on dictionary matches
- **Auto-suggestions**: Real-time suggestions based on input prefix
- **GPU Support**: Automatic GPU/CPU detection for model inference
- **CORS Enabled**: Ready for local development

### Frontend Features
- **Dark/Light Mode**: Toggle theme with persistent preference
- **Real-time Suggestions**: Get suggestions as you type (400ms debounce)
- **Confidence Display**: Visual confidence indicator for translations
- **Matched Pattern**: Shows the closest learned pattern from training
- **Example Pills**: Quick-start with pre-filled examples
- **Smooth Animations**: Floating icons, breathing effects, gradient shifts
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Modern UI**: Glass-morphism effects, gradients, and shadows

---

## 🎨 UI Components

### Hero Section
- Floating animated logo
- Gradient text effects
- Theme toggle button

### Translation Interface
- Input area with character/word counter
- Real-time suggestion dropdown
- Confidence meter
- Matched pattern display
- Clear button

### Features Section
- AI-Powered training
- Instant results with sub-100ms translations
- Living language support

### How It Works
- 3-step visual process guide
- Animated step indicators

---

## 🛠️ Tech Stack

**Backend**
- FastAPI
- PyTorch
- Transformers (MarianMT)
- Pandas
- Uvicorn

**Frontend**
- React 18
- Vite
- Tailwind CSS
- Lucide React (icons)
- Custom CSS animations

---

## 🤖 Model Training

### Training the Model

The `training_model/` directory contains scripts and utilities for training/fine-tuning the MarianMT model:

```bash
cd training_model

# Install training dependencies
pip install -r requirements.txt

# Preprocess your dataset
python preprocessing.py --input data.csv --output processed_data.pkl

# Train the model
python train.py --dataset processed_data.pkl --epochs 10 --output ../backend/synctype-final/
```

### Dataset Format
Prepare your training data as CSV with columns:
- `roman` - Romanized Khmer text
- `khmer` - Khmer script text

Example:
```csv
roman,khmer
som sok sabay,សុំសុខសប្បាយ
hello,សួស្តី
```

### Training Parameters
- **Model**: MarianMT base model
- **Batch size**: 32
- **Learning rate**: 3e-5
- **Epochs**: Configurable (default: 10)
- **Device**: Auto-detects GPU/CPU

---

## 📝 Usage Examples

### Example 1: Simple Translation
Input: `som sok sabay te`
Output: `សុំសុខសប្បាយតែ`
Confidence: `0.95`

### Example 2: Slang Translation
Input: `eng tv na?`
Output: `អ្នកធ្វើអ្វី?`
Confidence: `0.87`

---

## 🔧 Development Tips

### Hot Reload
Both backend and frontend support hot reload:
- Backend: `--reload` flag in uvicorn
- Frontend: Vite's built-in HMR

### Theme Development
Themes are defined in CSS custom properties:
- Light mode: `.bg-[#faf8f3]` with warm tones
- Dark mode: `.bg-[#0a0f1e]` with cool tones

### Adding New Examples
Edit the `examples` array in `App.jsx`:
```javascript
const examples = [
  "your new example",
  // ... more examples
];
```

---

## 🚢 Production Build

### Backend
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build      # Outputs to frontend/dist/
npm run preview    # Preview production build
```

Serve the `dist` folder with any static file server.

---

## 🐛 Troubleshooting

### Backend not responding
1. Check if port 8000 is available
2. Verify model files exist in `backend/synctype-final/`
3. Check CSV file at `backend/combined_dataset_v2.csv`

### Frontend can't connect
1. Verify backend is running on `http://127.0.0.1:8000`
2. Check browser console for CORS errors
3. Ensure API_BASE in App.jsx matches backend URL

### Suggestions not working
1. Check that `/api/suggest` endpoint is responding
2. Verify dictionary CSV is loaded properly
3. Check browser network tab for request/response

### Model training failed
1. Check GPU availability: `nvidia-smi`
2. Verify training dataset format (CSV with `roman` and `khmer` columns)
3. Ensure sufficient disk space for checkpoints
4. Check training_model/logs/ for detailed error messages

---

## 📄 License

Built for the Khmer community 🇰🇭

---

## 🙏 Credits

- **Model**: MarianMT character-level transformer
- **Dataset**: Combined Khmer slang dataset v2
- **UI Design**: Modern gradient glass-morphism aesthetic
- **Icons**: Lucide React

---

## 📧 Support

For issues or questions, please check the GitHub repository.

**Happy Translating! 🎉**
