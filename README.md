# Sutra Research Paper Translator

![Sutra Logo](https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png)

## About

Sutra Research Paper Translator is a powerful tool designed to translate academic and research papers into various Indian languages using the Sutra LLM (Large Language Model). This application leverages the multilingual capabilities of Sutra to make academic knowledge more accessible across linguistic boundaries.

## Features

- **Multiple Indian Language Support**: Translate papers into 13 Indian languages:
  - Hindi, Gujarati, Bengali, Tamil, Telugu, Kannada, Malayalam
  - Punjabi, Marathi, Urdu, Assamese, Odia, Sanskrit

- **Multiple File Format Support**:
  - PDF documents
  - Microsoft Word (DOCX) files
  - Plain text (TXT) files

- **Intelligent Text Processing**:
  - Preserves document structure (headings, subheadings, paragraphs)
  - Maintains scientific terminology accuracy
  - Chunks large documents for optimal processing

- **User-Friendly Interface**:
  - Real-time streaming translation
  - Progress tracking for large documents
  - Document preview functionality
  - One-click download of translated papers

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sutra-paper-translator.git
cd sutra-paper-translator

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Requirements

```
streamlit==1.32.0
langchain-openai==0.0.5
langchain==0.1.9
PyPDF2==3.0.1
python-docx==1.0.1
```

## Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Access the application in your web browser (typically at http://localhost:8501)

3. Enter your Sutra API key in the sidebar
   - If you don't have an API key, you can get one from [Sutra API](https://www.two.ai/sutra/api)

4. Select your target Indian language

5. Upload your research paper (PDF, DOCX, or TXT format)

6. Click "Start Translation" and wait for the process to complete

7. Review the translation and download the translated document

## How It Works

1. **Document Processing**: The application extracts text from the uploaded document based on its file format.

2. **Text Chunking**: Large documents are broken down into manageable chunks while preserving paragraph structure.

3. **Translation**: Each chunk is sent to the Sutra LLM with specific language instructions for accurate academic translation.

4. **Streaming Output**: Translations are displayed in real-time as they're generated.

5. **Final Assembly**: All translated chunks are assembled into a complete document, which can be downloaded.

## Language-Specific Instructions

The system provides tailored instructions for each language to ensure high-quality translations. For example:

- **Hindi**: "निम्नलिखित शोध पत्र को हिंदी में अनुवादित करें। अनुवाद स्पष्ट, सटीक और वैज्ञानिक शब्दावली के साथ होना चाहिए।"
- **Tamil**: "பின்வரும் ஆராய்ச்சி கட்டுரையை தமிழில் மொழிபெயர்க்கவும். மொழிபெயர்ப்பு தெளிவாக, துல்லியமாக, அறிவியல் கலைச்சொற்களுடன் இருக்க வேண்டும்."

## Best Practices

- **Document Preparation**: Ensure your document is well-structured with clear headings and paragraphs.
- **Technical Content**: For highly technical papers, consider post-editing by subject matter experts.
- **Large Documents**: For very large papers (50+ pages), consider splitting them into smaller files.
- **API Usage**: Be mindful of your API usage limits when translating multiple or large documents.

## Limitations

- Highly domain-specific terminology may require review by subject matter experts
- Complex mathematical equations, tables, and figures are not preserved in their original format
- Processing very large documents may take considerable time

## Disclaimer

While the Sutra LLM provides high-quality translations, this tool is designed to assist researchers and academics, not to replace professional translation services. The accuracy of technical and specialized terminology should be verified by subject matter experts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Sutra LLM](https://www.two.ai/sutra/api) for providing the multilingual AI model
- [Streamlit](https://streamlit.io/) for the web application framework
- [LangChain](https://www.langchain.com/) for AI framework integration

---

Developed with ❤️ for advancing multilingual academic accessibility
