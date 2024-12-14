from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Definisikan model untuk request body
class Item(BaseModel):
    keyword: str    

# Buat instance dari FastAPI
app = FastAPI()

# Buat endpoint untuk menerima data dari request body
@app.post("/konsul/")
async def create_item(item: Item):

    # Konfigurasi API Key untuk Google Generative AI
    genai.configure(api_key="AIzaSyD4RxNIb-tHB60YlUDjYMDfLAJTfuIk_aI")

    # Konfigurasi model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    # Buat input untuk model
    input1 = '''Saya ingin berkonsultasi dengan anda, tolong jawab seperti anda adalah teman saya, singkat, padat, jelas, namun tetap ramah. '''
    input2 = item.keyword
    input3 = '''sebelum menjawab pertanyaan saya, ada beberapa catatan untuk jawaban yang harus anda berikan :

 1. output jawaban harus anda berikan seperti format ini
konsultasi = [
{
"answer": "jawaban anda terkait pertanyaan saya berada disini"
}
]
2. langsung dimulai dengan json
3. hanya jawab dengan format json
4. tanpa kata pembuka, tentu, oke, baiklah, penutup atau kesimpulan
5. dilarang menjawab dengan kata "tentu", "oke", atau semacamnya yang berbau pendahuluan
6. langsung poin format json nya
7. jangan menjawab dengan kata pembuka seperti "tentu, saya bantu"'''
    input = input1 + input2 + input3

    # Kirim pesan ke model
    response = chat_session.send_message(input)

    # Ambil teks dari respons
    output = response.text[8:-4]

    local_vars = {}
    exec(output, {}, local_vars)

    # Ambil variabel list_divisi dari local_vars
    konsultasi = local_vars.get('konsultasi', [])
    return {"data": konsultasi }
