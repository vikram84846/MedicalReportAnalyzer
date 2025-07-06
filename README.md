# Medical Report Analyzer

A comprehensive medical report analysis system that uses AI to analyze medical reports and provide insights, summaries, and lifestyle recommendations.

## Features

- **Image Analysis**: Upload medical report images for analysis
- **PDF Processing**: Support for PDF medical reports
- **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash for intelligent analysis
- **Comprehensive Reports**: Provides summaries, key findings, and lifestyle recommendations
- **Modern React Frontend**: Beautiful, responsive UI with real-time analysis
- **Real-time API Integration**: Connected frontend and backend with proper error handling

## Architecture

- **Backend**: FastAPI for robust API endpoints
- **Frontend**: React with TypeScript, Vite, and Tailwind CSS
- **AI Integration**: LangChain with Google Gemini 2.0 Flash
- **File Processing**: Support for images and PDFs
- **State Management**: React Query for API state management

## Setup Instructions

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd medical-report-reader
npm install
```

### 3. Environment Configuration

1. Copy `env_example.txt` to `.env` (if it exists)
2. Add your Google Gemini API key to the `.env` file:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 4. Running the Application

#### Start the Backend (FastAPI)

```bash
python run_backend.py
```

The API will be available at `http://localhost:8000`

#### Start the Frontend (React)

```bash
cd medical-report-reader
npm run dev
```

The web interface will be available at `http://localhost:3000`

## API Endpoints

- `POST /analyze/image` - Analyze medical report images
- `POST /analyze/pdf` - Analyze PDF medical reports
- `GET /health` - Health check endpoint

## Project Structure

```
MedicalReportAnalyzer/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── services/
│   │   ├── ai_service.py       # AI analysis service
│   │   └── file_processor.py   # File processing service
│   └── utils/
│       └── config.py           # Configuration settings
├── medical-report-reader/       # React frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── hooks/             # Custom React hooks
│   │   ├── lib/               # Utility functions and API
│   │   └── pages/             # Page components
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt
├── run_backend.py              # Backend startup script
└── README.md
```

## Frontend Features

- **File Upload**: Drag-and-drop interface for images and PDFs
- **Real-time Analysis**: Live progress indicators and status updates
- **Comprehensive Results**: Detailed analysis with confidence scores
- **Medical Terms**: Expandable explanations of complex medical terms
- **Responsive Design**: Works on desktop and mobile devices
- **Error Handling**: Proper error messages and user feedback

## Usage

1. Start both backend and frontend servers
2. Open `http://localhost:3000` in your browser
3. Upload a medical report (image or PDF)
4. Click "Analyze Report"
5. View the AI-generated analysis including:
   - Summary of findings
   - Key medical insights
   - Lifestyle recommendations
   - Precautions and warnings
   - Confidence score
   - Medical terms explained

## Development

### Backend Development

The backend uses FastAPI with automatic API documentation available at `http://localhost:8000/docs`.

### Frontend Development

The frontend uses:

- **React 18** with TypeScript
- **Vite** for fast development
- **Tailwind CSS** for styling
- **React Query** for API state management
- **Shadcn/ui** for UI components
- **Lucide React** for icons

### API Integration

The frontend communicates with the backend through:

- `src/lib/api.ts` - API service functions
- `src/hooks/useMedicalAnalysis.ts` - React Query hooks
- Proper error handling and loading states

## Security Notes

- Never commit your actual API keys to version control
- Use environment variables for sensitive configuration
- Implement proper authentication for production use
- The current CORS settings allow all origins for development

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is for educational and research purposes. Please ensure compliance with medical data privacy regulations in your jurisdiction.
