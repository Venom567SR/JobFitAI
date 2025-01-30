# JobFitAI

JobFitAI is an AI-powered tool designed to match job descriptions with resumes, providing insights and recommendations to improve job applications.

## Features
- Extract and analyze job descriptions and resumes
- AI-powered suggestions to enhance resume alignment
- Visualization of matching scores and key insights
- Web-based interface for easy interaction

## Project Structure
```
JobFitAI/
│── app.py                    # Main application script
│── requirements.txt          # List of dependencies
│── .env                      # Environment variables
│
├── sample/
│   ├── JD.txt                # Sample job description
│   ├── Sample Resume.pdf     # Sample resume for testing
│
├── static/
│   ├── styles.css            # CSS styling for the frontend
│
├── utils/
│   ├── file_processors.py    # Handles file processing
│   ├── prompt_templates.py   # Contains AI prompt templates
│   ├── response_parser.py    # Parses responses from the AI
│   ├── visualizations.py     # Handles data visualization
│   ├── __init__.py           # Package initialization file
|
├── media/
│   ├── JobFitAI.mp4          # Demo video
│   ├── Mind Map - Frame 1.jpg # Mind map image
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/JobFitAI.git
   cd JobFitAI
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables in `.env` file.
4. Run the application:
   ```sh
   python app.py
   ```

## Mind Map
![Mind Map](media/Mind%20Map%20-%20Frame%201.jpg)

## Demo Video
[Watch the Demo](media/JobFitAI.mp4)

