# Uni-Guide: M.Tech Advisor

## Overview
Uni-Guide is an AI-powered platform to help students find the best M.Tech programs in Artificial Intelligence in Australia.

## Features
- University Ranking
- Scholarship Information
- Application Assistance
- Web Scraping for University Details

## Prerequisites
- Python 3.9+
- pip (Python Package Manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/uni-guide.git
cd uni-guide
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Create a `.env` file in the project root
- Add necessary API keys:
```
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

## Running the Application

1. Start the Streamlit app:
```bash
streamlit run main.py
```

## Project Structure
- `main.py`: Streamlit web interface
- `crew.py`: AI agent coordination
- `agents.py`: Individual AI agent definitions
- `task.py`: Task definitions for agents
- `scrape.py`: Web scraping utilities

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/uni-guide](https://github.com/yourusername/uni-guide)
