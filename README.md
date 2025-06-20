# AI SaaSquatch Leads Analyzer

A powerful B2B lead enrichment and scoring system that combines data processing with AI-powered insights to help sales teams prioritize leads effectively.

---

## Features

- **Automated Lead Scoring**: Algorithmically scores leads based on company size, age, and growth metrics  
- **AI-Powered Insights**: Generates natural language explanations for lead scores using Azure OpenAI  
- **Batch Processing**: Handles large lead lists efficiently with chunked processing  
- **CSV Export**: Download enriched lead data with scores and insights sorted on the basis of the lead scores in descending order  

---

## Tech Stack

**Backend**:
- FastAPI (Python) - REST API framework
- Pandas - Data processing
- Azure OpenAI - AI insights generation
- Uvicorn - ASGI server

**Frontend**:
- React.js - Frontend framework
- CSS Modules - Styling
- Fetch API - HTTP requests

---

## Installation

### Prerequisites

- Python 3.9+
- Node.js 16+
- Azure OpenAI API credentials

---

### Backend Setup

```bash
git clone https://github.com/yourusername/ai-saasquatch-leads-analyzer.git
cd ai-saasquatch-leads-analyzer/backend
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r ../requirements.txt
```

Create a `.env` file in the backend directory with your Azure OpenAI credentials:

```
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_KEY=your-api-key
OPENAI_API_VERSION=2024-02-01
```

Run the backend server:

```bash
uvicorn main:app --reload
```

---

### Frontend Setup

Navigate to the frontend directory:

```bash
cd ../frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm start
```

---

## Usage

1. Prepare your CSV file with lead data (required columns listed below)
2. Upload your CSV through the web interface
3. Download the enriched CSV sorted by lead scores

The enriched CSV will contain:

- Original lead data  
- **lead_score** (0–100)  
- **insights** (AI-generated explanation of the score)

---

## API Endpoints

| Endpoint                | Method | Description                  |
|-------------------------|--------|------------------------------|
| `/health`               | GET    | Health check                 |
| `/analyze/`             | POST   | Upload CSV for processing    |
| `/progress/{task_id}`   | GET    | Check processing progress    |
| `/download/{task_id}`   | GET    | Download processed CSV       |

---

## Input CSV Format

Ensure your input CSV includes the following columns:

- `name`: Company name  
- `website`: Company website URL  
- `founded`: Year founded (integer)  
- `industry`: Industry category  
- `size_range`: Employee size range (e.g., "1-10", "11-50")  
- `locality`: City/Location  
- `country`: Country  
- `current employee estimate`: Current employee count  
- `total employee estimate`: Total employee count  
- `linkedin_url`: LinkedIn profile URL (optional)

---

## Output CSV Format

The processed CSV will include all original columns plus:

- `lead_score`: Numeric score (0–100)  
- `insights`: AI-generated explanation of the score

---

## Deployment

The application can be deployed on any cloud platform that supports Python and Node.js.

### Production Backend (Uvicorn)

```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Production Frontend

```bash
cd frontend
npm run build
```

Serve the frontend using Nginx or upload the build to a CDN.

---

## Contact

For questions or support, please contact:

**R Sai Shivani** - saishivani0304@gmail.com  
**Project Link**: [https://leadgen-site.onrender.com/](https://leadgen-site.onrender.com/)
