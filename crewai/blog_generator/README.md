
# Blog Generator App - README

## Overview
The **Blog Generator App** is a Streamlit-based application powered by **CrewAI** that enables users to generate high-quality blog content using AI models like **LLaMA 3, OpenAI, Deepseek, and Claude**. This tool allows users to input a topic, adjust creativity settings, and select a preferred AI model for content generation.

## Features
- **User-Friendly Interface**: Simple and intuitive UI built with Streamlit.
- **Content Customization**:
  - Enter a blog topic.
  - Adjust temperature for creativity control.
  - Choose from multiple AI models.
- **Dynamic Content Generation**: Generates content instantly upon user input.
- **Expandable Help Section**: Provides guidance on how to use the app.

## Installation
### Prerequisites
Ensure you have  **Python >=3.10 <3.13**  installed along with the required dependencies.

### Steps

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage
1. Open the **Streamlit sidebar**.
2. Enter a blog topic.
3. Adjust the **temperature** slider to control creativity.
4. Select an AI model (**LLaMA 3, GPT-4o Mini, Claude**).
5. Click **Generate Content** to produce blog content.

## Customization
- Modify `main.py` to change UI elements or integrate additional models.
- Adjust temperature settings for different levels of creativity.

---
Enjoy generating blogs effortlessly with **CrewAI**! 🚀


