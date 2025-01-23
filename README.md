# Slimr - Smart Analytics for Belgian SMEs 🚀

> Making data-driven decisions accessible for every business

## What is Slimr?
Slimr is a SaaS analytics and pricing optimization platform that helps small businesses in Belgium make smarter decisions. Built with Python and ML, it turns complex data into actionable insights.

## Features
### MVP (Coming Soon)
- 📊 Easy-to-understand analytics dashboard
- 📈 Sales trend analysis
- 🔄 Simple CSV data upload
- 📱 Mobile-friendly interface

### Future Releases
- 🤖 ML-powered pricing optimization
- 🎯 Customer segmentation
- 📊 Advanced visualizations
- 🔌 API integrations

## Tech Stack
- **Backend**: FastAPI, PostgreSQL
- **Analytics**: Python (pandas, scikit-learn)
- **Frontend**: Streamlit (MVP), React (future)
- **Cloud**: Azure (planned)

## Getting Started
```bash
# Clone the repository
git clone https://github.com/yourusername/slimr.git

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Unix
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload
