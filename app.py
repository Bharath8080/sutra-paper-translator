import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler
import PyPDF2
import docx
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="Research Paper Translator - Sutra LLM",
    page_icon="📚",
    layout="wide"
)

# Define supported languages
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", 
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", 
    "Tagalog", "Swahili"
]

# Translation instructions for each language
translation_instructions = {
    "English": "Translate the following research paper into English. The translation should be clear, accurate, and maintain scientific terminology. Preserve the headings, subheadings, and paragraph structure.",
    "Hindi": "निम्नलिखित शोध पत्र को हिंदी में अनुवादित करें। अनुवाद स्पष्ट, सटीक और वैज्ञानिक शब्दावली के साथ होना चाहिए। हेडिंग, उपशीर्षक और पैराग्राफ संरचना को बनाए रखें।",
    "Gujarati": "નીચે આપેલા સંશોધન પેપરનું ગુજરાતીમાં અનુવાદ કરો. અનુવાદ સ્પષ્ટ, ચોક્કસ અને વૈજ્ઞાનિક શબ્દાવલી સાથે હોવો જોઈએ. હેડિંગ, સબહેડિંગ અને પેરાગ્રાફ સ્ટ્રક્ચર જાળવી રાખો.",
    "Bengali": "নিম্নলিখিত গবেষণা পেপারটি বাংলায় অনুবাদ করুন। অনুবাদটি স্পষ্ট, সঠিক এবং বৈজ্ঞানিক শব্দভাণ্ডারযুক্ত হতে হবে। শিরোনাম, উপশীর্ষক এবং অনুচ্ছেদের কাঠামো বজায় রাখুন।",
    "Tamil": "பின்வரும் ஆராய்ச்சி கட்டுரையை தமிழில் மொழிபெயர்க்கவும். மொழிபெயர்ப்பு தெளிவாக, துல்லியமாக, அறிவியல் கலைச்சொற்களுடன் இருக்க வேண்டும். தலைப்புகள், துணைத்தலைப்புகள் மற்றும் பத்தி கட்டமைப்பை பராமரிக்கவும்.",
    "Telugu": "కింది పరిశోధనా పత్రాన్ని తెలుగులోకి అనువదించండి. అనువాదం స్పష్టంగా, ఖచ్చితంగా మరియు శాస్త్రీయ పదజాలంతో ఉండాలి. శీర్షికలు, ఉపశీర్షికలు మరియు పేరా నిర్మాణాన్ని నిర్వహించండి.",
    "Kannada": "ಕೆಳಗಿನ ಸಂಶೋಧನಾ ಪತ್ರವನ್ನು ಕನ್ನಡಕ್ಕೆ ಅನುವಾದಿಸಿ. ಅನುವಾದವು ಸ್ಪಷ್ಟವಾಗಿ, ನಿಖರವಾಗಿ ಮತ್ತು ವೈಜ್ಞಾನಿಕ ಪದಾವಳಿಯೊಂದಿಗೆ ಇರಬೇಕು. ಶೀರ್ಷಿಕೆಗಳು, ಉಪಶೀರ್ಷಿಕೆಗಳು ಮತ್ತು ಪ್ಯಾರಾಗ್ರಾಫ್ ರಚನೆಯನ್ನು ಕಾಯ್ದುಕೊಳ್ಳಿ.",
    "Malayalam": "താഴെ പറയുന്ന ഗവേഷണ പ്രബന്ധം മലയാളത്തിലേക്ക് വിവർത്തനം ചെയ്യുക. വിവർത്തനം വ്യക്തവും കൃത്യവും ശാസ്ത്രീയ പദാവലി ഉൾക്കൊള്ളുന്നതും ആയിരിക്കണം. തലക്കെട്ടുകൾ, ഉപതലക്കെട്ടുകൾ, ഖണ്ഡികകളുടെ ഘടന എന്നിവ നിലനിർത്തുക.",
    "Punjabi": "ਹੇਠਾਂ ਦਿੱਤੇ ਖੋਜ ਪੇਪਰ ਦਾ ਪੰਜਾਬੀ ਵਿੱਚ ਅਨੁਵਾਦ ਕਰੋ। ਅਨੁਵਾਦ ਸਪਸ਼ਟ, ਸਹੀ ਅਤੇ ਵਿਗਿਆਨਕ ਸ਼ਬਦਾਵਲੀ ਦੇ ਨਾਲ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ। ਸਿਰਲੇਖ, ਉਪ-ਸਿਰਲੇਖ ਅਤੇ ਪੈਰਾਗ੍ਰਾਫ ਸੰਰਚਨਾ ਨੂੰ ਬਰਕਰਾਰ ਰੱਖੋ।",
    "Marathi": "खालील संशोधन पेपरचे मराठीत भाषांतर करा. भाषांतर स्पष्ट, अचूक आणि वैज्ञानिक शब्दावलीसह असावे. शीर्षके, उपशीर्षके आणि परिच्छेद संरचना कायम ठेवा.",
    "Urdu": "مندرجہ ذیل تحقیقی مقالے کا اردو میں ترجمہ کریں۔ ترجمہ واضح، درست اور سائنسی اصطلاحات کے ساتھ ہونا چاہیے۔ عنوانات، ذیلی عنوانات اور پیراگراف کی ساخت کو برقرار رکھیں۔",
    "Assamese": "নিম্নলিখিত গৱেষণা পত্ৰটো অসমীয়াত অনুবাদ কৰক। অনুবাদটো স্পষ্ট, সঠিক আৰু বৈজ্ঞানিক শব্দভাণ্ডাৰৰ সৈতে হ'ব লাগিব। শিৰোনাম, উপশীৰ্ষক আৰু অনুচ্ছেদৰ গাঁথনি বজাই ৰাখক।",
    "Odia": "ନିମ୍ନଲିଖିତ ଗବେଷଣା ପତ୍ରକୁ ଓଡ଼ିଆରେ ଅନୁବାଦ କରନ୍ତୁ। ଅନୁବାଦଟି ସ୍ପଷ୍ଟ, ସଠିକ୍ ଏବଂ ବୈଜ୍ଞାନିକ ଶବ୍ଦାବଳୀ ସହିତ ହେବା ଉଚିତ। ଶୀର୍ଷକ, ଉପଶୀର୍ଷକ ଏବଂ ଅନୁଚ୍ଛେଦ ଗଠନକୁ ବଜାୟ ରଖନ୍ତୁ।",
    "Sanskrit": "अधोलिखितं शोधपत्रं संस्कृते अनुवादयतु। अनुवादः स्पष्टः, यथार्थः वैज्ञानिकशब्दावल्या च भवेत्। शीर्षकम्, उपशीर्षकम् अनुच्छेदरचनां च संरक्षतु।",
    "Korean": "다음 연구 논문을 한국어로 번역하세요. 번역은 명확하고 정확하며 과학적 용어를 유지해야 합니다. 제목, 부제목 및 단락 구조를 유지하세요.",
    "Japanese": "以下の研究論文を日本語に翻訳してください。翻訳は明確で正確であり、科学的な用語を維持する必要があります。見出し、小見出し、段落構造を保持してください。",
    "Arabic": "قم بترجمة ورقة البحث التالية إلى العربية. يجب أن تكون الترجمة واضحة ودقيقة وتحافظ على المصطلحات العلمية. الحفاظ على العناوين والعناوين الفرعية وهيكل الفقرة.",
    "French": "Traduisez le document de recherche suivant en français. La traduction doit être claire, précise et maintenir la terminologie scientifique. Préserver les titres, sous-titres et la structure des paragraphes.",
    "German": "Übersetzen Sie das folgende Forschungspapier ins Deutsche. Die Übersetzung sollte klar, präzise und wissenschaftliche Terminologie beibehalten. Bewahren Sie die Überschriften, Unterüberschriften und Absatzstruktur.",
    "Spanish": "Traduzca el siguiente documento de investigación al español. La traducción debe ser clara, precisa y mantener la terminología científica. Preservar los encabezados, subtítulos y estructura de párrafos.",
    "Portuguese": "Traduza o seguinte artigo de pesquisa para português. A tradução deve ser clara, precisa e manter a terminologia científica. Preservar os títulos, subtítulos e estrutura de parágrafos.",
    "Russian": "Переведите следующую исследовательскую работу на русский язык. Перевод должен быть ясным, точным и сохранять научную терминологию. Сохраняйте заголовки, подзаголовки и структуру абзацев.",
    "Chinese": "将以下研究论文翻译成中文。翻译应清晰、准确并保持科学术语。保留标题、副标题和段落结构。",
    "Vietnamese": "Dịch bài nghiên cứu sau sang tiếng Việt. Bản dịch phải rõ ràng, chính xác và duy trì thuật ngữ khoa học. Giữ nguyên tiêu đề, tiêu đề phụ và cấu trúc đoạn văn.",
    "Thai": "แปลเอกสารวิจัยต่อไปนี้เป็นภาษาไทย การแปลต้องชัดเจน ถูกต้อง และรักษาศัพท์ทางวิทยาศาสตร์ เก็บรักษาหัวข้อ หัวข้อย่อย และโครงสร้างย่อหน้า",
    "Indonesian": "Terjemahkan makalah penelitian berikut ke dalam Bahasa Indonesia. Terjemahan harus jelas, akurat, dan mempertahankan terminologi ilmiah. Pertahankan judul, subjudul, dan struktur paragraf.",
    "Turkish": "Aşağıdaki araştırma makalesini Türkçeye çevirin. Çeviri açık, doğru ve bilimsel terminolojiyi korumalıdır. Başlıkları, alt başlıkları ve paragraf yapısını koruyun.",
    "Polish": "Przetłumacz poniższy artykuł badawczy na język polski. Tłumaczenie powinno być jasne, dokładne i zachowywać terminologię naukową. Zachowaj nagłówki, podtytuły i strukturę akapitów.",
    "Ukrainian": "Перекладіть наступну дослідницьку роботу українською мовою. Переклад має бути чітким, точним і зберігати наукову термінологію. Зберігайте заголовки, підзаголовки та структуру абзаців.",
    "Dutch": "Vertaal het volgende onderzoeksdocument naar het Nederlands. De vertaling moet duidelijk, nauwkeurig zijn en wetenschappelijke terminologie behouden. Behoud de koppen, subkoppen en alineastructuur.",
    "Italian": "Traduci il seguente documento di ricerca in italiano. La traduzione deve essere chiara, precisa e mantenere la terminologia scientifica. Preservare i titoli, i sottotitoli e la struttura dei paragrafi.",
    "Greek": "Μεταφράστε την παρακάτω ερευνητική εργασία στα ελληνικά. Η μετάφραση πρέπει να είναι σαφής, ακριβής και να διατηρεί την επιστημονική ορολογία. Διατηρήστε τους τίτλους, τους υπότιτλους και τη δομή των παραγράφων.",
    "Hebrew": "תרגם את מאמר המחקר הבא לעברית. התרגום צריך להיות ברור, מדויק ולשמור על טרמינולוגיה מדעית. שמור על כותרות, כותרות משנה ומבנה פסקאות.",
    "Persian": "مقاله تحقیقاتی زیر را به فارسی ترجمه کنید. ترجمه باید واضح، دقیق و اصطلاحات علمی را حفظ کند. عناوین، زیرعنوان‌ها و ساختار پاراگراف را حفظ کنید.",
    "Swedish": "Översätt följande forskningsdokument till svenska. Översättningen ska vara tydlig, korrekt och behålla vetenskaplig terminologi. Bevara rubriker, underrubriker och styckestruktur.",
    "Norwegian": "Oversett følgende forskningsdokument til norsk. Oversettelsen skal være tydelig, nøyaktig og beholde vitenskapelig terminologi. Bevar overskrifter, underoverskrifter og avsnittsstruktur.",
    "Danish": "Oversæt følgende forskningsdokument til dansk. Oversættelsen skal være klar, præcis og bevare videnskabelig terminologi. Bevar overskrifter, underoverskrifter og afsnitsstruktur.",
    "Finnish": "Käännä seuraava tutkimusasiakirja suomeksi. Käännöksen tulee olla selkeä, tarkka ja säilyttää tieteellinen terminologia. Säilytä otsikot, alaotsikot ja kappaleiden rakenne.",
    "Czech": "Přeložte následující výzkumný dokument do češtiny. Překlad musí být jasný, přesný a zachovat vědeckou terminologii. Zachovejte nadpisy, podnadpisy a strukturu odstavců.",
    "Hungarian": "Fordítsa le a következő kutatási dokumentumot magyarra. A fordításnak világosnak, pontosnak kell lennie és meg kell őriznie a tudományos terminológiát. Megőrizni a címsorokat, alcímsorokat és a bekezdések szerkezetét.",
    "Romanian": "Traduceți următorul document de cercetare în limba română. Traducerea trebuie să fie clară, precisă și să păstreze terminologia științifică. Păstrați titlurile, subtitlurile și structura paragrafelor.",
    "Bulgarian": "Преведете следния изследователски документ на български език. Преводът трябва да е ясен, точен и да запазва научната терминология. Запазете заглавията, подзаглавията и структурата на параграфите.",
    "Croatian": "Prevedite sljedeći istraživački dokument na hrvatski jezik. Prijevod mora biti jasan, točan i zadržati znanstvenu terminologiju. Zadržite naslove, podnaslove i strukturu odlomaka.",
    "Serbian": "Преведите следећи истраживачки документ на српски језик. Превод мора бити јасан, тачан и задржати научну терминологију. Задржите наслове, поднаслове и структуру пасуса.",
    "Slovak": "Preložte nasledujúci výskumný dokument do slovenčiny. Preklad musí byť jasný, presný a zachovať vedeckú terminológiu. Zachovajte nadpisy, podnadpisy a štruktúru odsekov.",
    "Slovenian": "Prevedite naslednji raziskovalni dokument v slovenščino. Prevajalec mora biti jasen, natančen in ohranjati znanstveno terminologijo. Ohranite naslove, podnaslove in strukturo odstavkov.",
    "Estonian": "Tõlkige järgmine uurimisdokument eesti keelde. Tõlge peab olema selge, täpne ja säilitama teadusliku terminoloogia. Säilitage pealkirjad, alapealkirjad ja lõikude struktuur.",
    "Latvian": "Tulkojiet šo pētniecības dokumentu latviešu valodā. Tulkojumam jābūt skaidram, precīzam un jāsaglabā zinātniskā terminoloģija. Saglabājiet virsrakstus, apakšvirsrakstus un rindkopu struktūru.",
    "Lithuanian": "Išverskite šį mokslinį dokumentą į lietuvių kalbą. Vertimas turi būti aiškus, tikslus ir išlaikyti mokslinę terminologiją. Išlaikykite antraštes, paantraštes ir pastraipų struktūrą.",
    "Malay": "Terjemahkan dokumen penyelidikan berikut ke dalam Bahasa Melayu. Terjemahan mestilah jelas, tepat dan mengekalkan terminologi saintifik. Mengekalkan tajuk, subtajuk dan struktur perenggan.",
    "Tagalog": "Isalin ang sumusunod na dokumento ng pananaliksik sa Tagalog. Ang pagsasalin ay dapat malinaw, tumpak at mapanatili ang siyentipikong terminolohiya. Panatilihin ang mga pamagat, subpamagat at istruktura ng talata.",
    "Swahili": "Tafsiri nyaraka zifuatazo za utafiti kwa Kiswahili. Tafsiri inapaswa kuwa wazi, sahihi na kudumisha istilahi za kisayansi. Dumisha vichwa, vichwa vidogo na muundo wa aya."
}

# Streaming callback handler
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# Initialize the ChatOpenAI model - base instance for caching
@st.cache_resource
def get_base_chat_model(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.3,  # Lower temperature for more accurate translations
    )

# Create a streaming version of the model with callback handler
def get_streaming_chat_model(api_key, callback_handler=None):
    # Create a new instance with streaming enabled
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.3,  # Lower temperature for more accurate translations
        streaming=True,
        callbacks=[callback_handler] if callback_handler else None
    )

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text() + "\n\n"
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to extract text from TXT
def extract_text_from_txt(txt_file):
    return txt_file.getvalue().decode("utf-8")

# Function to chunk text for processing
def chunk_text(text, max_chunk_size=5000):
    """Split text into chunks of max_chunk_size characters,
    trying to preserve paragraph integrity."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        # If adding this paragraph would exceed max size, save current chunk and start a new one
        if len(current_chunk) + len(paragraph) > max_chunk_size:
            if current_chunk:  # Only append if current_chunk is not empty
                chunks.append(current_chunk)
            current_chunk = paragraph + "\n\n"
        else:
            current_chunk += paragraph + "\n\n"
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Function to translate text using Sutra LLM
def translate_text(text, language, api_key, response_container):
    # Create stream handler
    stream_handler = StreamHandler(response_container)
    
    # Get streaming model with handler
    chat = get_streaming_chat_model(api_key, stream_handler)
    
    # Create message with translation instruction
    instruction = translation_instructions.get(language, f"Translate the following research paper into {language}. The translation should be clear, accurate, and maintain scientific terminology. Preserve the headings, subheadings, and paragraph structure.")
    
    message = f"{instruction}\n\n{text}"
    
    # Generate streaming response
    messages = [HumanMessage(content=message)]
    
    response = chat.invoke(messages)
    return response.content

# Sidebar for language selection and API key
st.sidebar.image("https://framerusercontent.com/images/3Ca34Pogzn9I3a7uTsNSlfs9Bdk.png", use_container_width=True)
with st.sidebar:
    st.title("📚 Research Paper Translator")
    
    # API Key section
    st.markdown("### API Key")
    st.markdown("Get your free API key from [Sutra API](https://www.two.ai/sutra/api)")
    api_key = st.text_input("Enter your Sutra API Key:", type="password")
    
    # Language selector
    target_language = st.selectbox("Select target language:", languages)
    
    st.divider()
    
    # About section
    st.markdown("### About Sutra LLM")
    st.markdown("Sutra is a multilingual model supporting 50+ languages with high-quality responses, making it ideal for academic translations.")
    
    # Disclaimer
    st.markdown("### Disclaimer")
    st.markdown("This tool uses AI for translation. While it strives for accuracy, some technical or specialized terms may require review by subject matter experts.")

# Main content
st.markdown('<h1><img src="https://cdn.pixabay.com/animation/2023/06/13/15/13/15-13-33-168_512.gif" width="70" height="70" style="vertical-align: middle;"> Research Paper Translator - Sutra LLM</h1>', unsafe_allow_html=True)
st.markdown(f"Upload a research paper and translate it into **{target_language}**. Supports PDF, DOCX, and TXT formats.")

# File uploader
uploaded_file = st.file_uploader("Upload your research paper", type=["pdf", "docx", "txt"])

# Process the file
if uploaded_file is not None:
    # Extract text based on file type
    with st.spinner("Extracting text from document..."):
        if uploaded_file.name.endswith('.pdf'):
            text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.name.endswith('.txt'):
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file format")
            text = None
    
    if text:
        # Display a sample of the extracted text
        with st.expander("Preview Extracted Text"):
            st.text(text[:1000] + "...")
        
        # Translation section
        st.markdown(f"## Translation to {target_language}")
        
        # Check if API key is provided
        if not api_key:
            st.error("Please enter your Sutra API key in the sidebar.")
        else:
            translate_button = st.button("Start Translation")
            
            if translate_button:
                # Split text into chunks for processing
                chunks = chunk_text(text)
                
                # Translation progress
                progress_bar = st.progress(0)
                translated_text_full = ""
                
                # Container for translated text
                translated_output = st.container()
                
                # Process each chunk
                for i, chunk in enumerate(chunks):
                    st.subheader(f"Translating part {i+1} of {len(chunks)}")
                    
                    # Create container for this chunk's translation
                    chunk_container = st.empty()
                    
                    # Translate chunk
                    translated_chunk = translate_text(chunk, target_language, api_key, chunk_container)
                    
                    # Append to full translation
                    translated_text_full += translated_chunk + "\n\n"
                    
                    # Update progress
                    progress_bar.progress((i + 1) / len(chunks))
                
                # Final output section
                st.markdown("## Completed Translation")
                st.markdown(translated_text_full)
                
                # Download option
                st.download_button(
                    label="Download Translated Paper",
                    data=translated_text_full,
                    file_name=f"translated_{target_language}_{uploaded_file.name.split('.')[0]}.txt",
                    mime="text/plain"
                )
else:
    # Placeholder example when no file is uploaded
    st.info("Please upload a research paper to begin translation.")
    
    # Example of what the tool does
    st.markdown("### How it works")
    st.markdown("""
    1. Upload your research paper (PDF, DOCX, or TXT format)
    2. Select your target Indian language
    3. Click 'Start Translation'
    4. Review and download the translated paper
    
    The tool processes large documents by breaking them into manageable chunks while preserving the document structure.
    """)
