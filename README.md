# Meditation Guidance Project

## Project Overview
This project provides guided meditation scripts based on user preferences such as wellness goals, experience level, and duration. The generated scripts help users practice meditation effectively.

## Prerequisites
Ensure you have the following installed on your system:
- Python (>=3.8)
- Flask
- OpenAI API Key (or another model's API key if using a different LLM)
- Any necessary front-end dependencies

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project
1. Start the backend server:
   ```bash
   python main.py
   ```

2. Open `index12.html` in a browser to access the meditation guide.

## Setting the API Key
Ensure you set up the OpenAI API key before running the project.
- Create a `.env` file in the project root and add the following line:
  ```
  OPENAI_API_KEY=your_api_key_here
  ```
- Alternatively, you can set it in the terminal:
  ```bash
  export OPENAI_API_KEY=your_api_key_here  # For Linux/macOS
  set OPENAI_API_KEY=your_api_key_here    # For Windows
  ```

## Modifying the Prompt
To customize the meditation script generation:
1. Open `prompt_templates.py`.
2. Modify the `MEDITATION_SCRIPT_PROMPT` template.
3. Change parameters such as goal, duration, and voice tone.
4. Save the file and restart the server to apply changes.

## Redirecting Webpage
If you need to change the default landing page:
1. Edit `index12.html` and modify navigation links accordingly.
2. Ensure that `styles.css` is properly linked for consistent styling.

## Contributions
If you’d like to contribute, feel free to open a pull request with improvements or new features.

## License
This project is licensed under [insert license type].

