import os
import openai
from django.conf import settings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

from myapp.models import FAQ, FacultyAnnouncements, Materials

# Set the OpenAI API key from Django settings
openai.api_key = settings.OPENAI_API_KEY

def create_course_docs(course_id):
    documents = []

    # Fetch and format Materials
    materials = Materials.objects.filter(course_id=course_id)
    for m in materials:
        text = f"Title: {m.material_title}\nDescription: {m.description}"
        documents.append(Document(page_content=text, metadata={"type": "material"}))

    # Fetch and format FAQs
    faqs = FAQ.objects.all()  # Optional: filter by course if FAQ model includes course_id
    for f in faqs:
        text = f"Q: {f.faq_qsn}\nA: {f.faq_ans}"
        documents.append(Document(page_content=text, metadata={"type": "faq"}))

    # Fetch and format Announcements
    announcements = FacultyAnnouncements.objects.filter(course_id=course_id)
    for a in announcements:
        if a.notice_id:  # Extra check for null safety
            text = f"Announcement: {a.notice_id.title}\n{a.notice_id.description}"
            documents.append(Document(page_content=text, metadata={"type": "announcement"}))

    return documents

def build_chatbot_for_course(course_id):
    documents = create_course_docs(course_id)

    if not documents:
        return None  # Avoid errors if course has no documents

    # Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = splitter.split_documents(documents)

    # Generate embeddings and set up retrieval
    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    db = FAISS.from_documents(texts, embeddings)
    retriever = db.as_retriever()

    # Create the RetrievalQA chain
    llm = OpenAI(temperature=0)
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    return qa
