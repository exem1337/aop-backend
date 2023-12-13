from fastapi import APIRouter, UploadFile, File
from docx import Document
import PyPDF2
from io import BytesIO
import openai
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Установка ключа API
api_key = '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'
openai.api_key = api_key

router = APIRouter()

# Функция для извлечения текста из docx файлов
async def extract_text_from_docx(file):
    contents = BytesIO(await file.read())
    doc = Document(contents)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Функция для извлечения текста из pdf файлов
async def extract_text_from_pdf(file):
    contents = BytesIO(await file.read())
    pdf_reader = PyPDF2.PdfReader(contents)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Функция для генерации вопросов с нужной JSON-структурой
def generate_questions_answers(text, num_questions=5, max_tokens=100):
    cache_path = "D:/ai-cache"
    tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base", cache_dir=cache_path)
    model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base", cache_dir=cache_path)

    input_text = f"generate 3 random questions"
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids

    outputs = model.generate(input_ids, max_new_tokens=100)

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Ендпоинт для генерации вопросов с нужной JSON-структурой
@router.post("/generate_questions_with_json/", tags=['questions'])
async def generate_questions_with_json_from_document(file: UploadFile = File(...), num_questions: int = 5):
    file_extension = file.filename.split(".")[-1]
    if file_extension == "docx":
        text = await extract_text_from_docx(file)
    elif file_extension == "pdf":
        text = await extract_text_from_pdf(file)
    else:
        return {"error": "Unsupported file format. Only docx and pdf files are supported."}
    
    generated_json = generate_questions_answers(text, num_questions)
    return {"generated_json": generated_json}