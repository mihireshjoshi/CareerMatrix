from flask import Flask, render_template, send_file, redirect, url_for, request, session
import google.generativeai as genai
from google.generativeai import GenerationConfig,GenerativeModel
import PyPDF2
import re

app = Flask(__name__)


app.secret_key = 'your_secret_key'
api_key = "AIzaSyA81MQFSGGHrzZuGIGZgJ0Ej_uD2SUMyAg"
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")






def extract_text(pdf_path):
    extracted_text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        for page_number in range(num_pages):
            page = pdf_reader.pages[page_number]
            extracted_text += page.extract_text()
    print(extracted_text)
    return extracted_text



def get_model_response_pdf(pdf_path, job_role):
    text = extract_text(pdf_path)
    input_tech = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my work profile for a job role of {job_role} after 1 year from a technical point of view. Taking my current CV into consideration as {text}, please suggest specific skills and projects that I should focus on to significantly improve my CV from a technical perspective and increase my chances of securing a desirable job in this field.
    Generate the response in one paragraph with a heading of 'Technical Skills'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_tech = GenerationConfig(temperature=0.5)
    response_tech = model.generate_content(input_tech, generation_config=generated_config_tech)
    generated_tech = ""
    for part in response_tech.parts:
        generated_tech += part.text.strip() + "\n"
    generated_tech = generated_tech.replace("*", "")

    input_soft = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my work profile for a job role of {job_role} after 1 year specifically focusing on soft skills. Taking my current CV into consideration as {text}, please suggest the areas of soft skills that I should focus on to significantly improve my CV from a non-technical perspective and increase my chances of securing a desirable job in this field.
    Generate the response in one paragraph with a heading of 'Soft Skills'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_soft = GenerationConfig(temperature=0.5)
    response_soft = model.generate_content(input_soft, generation_config=generated_config_soft)
    generated_soft = ""
    for part in response_soft.parts:
        generated_soft += part.text.strip() + "\n"
    generated_soft = generated_soft.replace("*", "")

    input_inter = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my skillset and personality for a job role of {job_role} after 1 year. Taking my current CV into consideration as {text}, please give guidance for interview preparation that I should focus on to significantly improve my performance for the interview and increase my chances of securing a desirable job in this field.
    Please generate 5 frequently asked Interview Questions for the Interview round and 5 frequently asked interview questions for the technical round based on the job role {job_role}. Generate the response in two paragraphs with a heading of 'Interview Preparation' and for the other give a header 'Interview Questions' and two sub-headers as 'Technical Round Questions' and 'Interview Round Questions'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_inter = GenerationConfig(temperature=0.6)
    response_inter = model.generate_content(input_inter, generation_config=generated_config_inter)
    generated_inter = ""
    for part in response_inter.parts:
        generated_inter += part.text.strip() + "\n"
    generated_inter = generated_inter.replace("*", "")

    input_role2 = f"""
    Based on this CV : {text}
    Suggest 3 courses from Coursera and Udemy which I can do to boost my technical skills for the job role: {job_role}. 
    Generate response by providing URLs for every generated course. Give a heading as 'Courses to Consider' and generate response from the next line.
    """
    generated_config2 = GenerationConfig(temperature=0.8)
    response2 = model.generate_content(input_role2, generation_config=generated_config2)
    generated_courses = ""
    for part in response2.parts:
        generated_courses += part.text.strip() + "\n"
    generated_courses = generated_courses.replace("*", "")

    input_role1 = f"""
    Suggest 3 alternative career paths for the following job role: {job_role}.
    Give a title to the response as 'Additional Career Paths' and generate from the next line.
    """
    generated_config1 = GenerationConfig(temperature=0.8)
    response1 = model.generate_content(input_role1, generation_config=generated_config1)
    generated_path = ""
    for part in response1.parts:
        generated_path += part.text.strip() + "\n"
    generated_path = generated_path.replace("*", "")
    urls = re.findall(r'https?://\S+', generated_courses)
    return generated_tech, generated_soft, generated_inter, generated_courses, generated_path, urls


def get_model_response_text(text, job_role):
    
    input_tech = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my work profile for a job role of {job_role} after 1 year from a technical point of view. Taking my current CV into consideration as {text}, please suggest specific skills and projects that I should focus on to significantly improve my CV from a technical perspective and increase my chances of securing a desirable job in this field.
    Generate the response in one paragraph with a heading of 'Technical Skills'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_tech = GenerationConfig(temperature=0.5)
    response_tech = model.generate_content(input_tech, generation_config=generated_config_tech)
    generated_tech = ""
    for part in response_tech.parts:
        generated_tech += part.text.strip() + "\n"
    generated_tech = generated_tech.replace("*", "")

    input_soft = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my work profile for a job role of {job_role} after 1 year specifically focusing on soft skills. Taking my current CV into consideration as {text}, please suggest the areas of soft skills that I should focus on to significantly improve my CV from a non-technical perspective and increase my chances of securing a desirable job in this field.
    Generate the response in one paragraph with a heading of 'Soft Skills'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_soft = GenerationConfig(temperature=0.5)
    response_soft = model.generate_content(input_soft, generation_config=generated_config_soft)
    generated_soft = ""
    for part in response_soft.parts:
        generated_soft += part.text.strip() + "\n"
    generated_soft = generated_soft.replace("*", "")

    input_inter = f"""
    I want you to act as a Career Improviser and provide guidance on enhancing my skillset and personality for a job role of {job_role} after 1 year. Taking my current CV into consideration as {text}, please give guidance for interview preparation that I should focus on to significantly improve my performance for the interview and increase my chances of securing a desirable job in this field.
    Please generate 5 frequently asked Interview Questions for the Interview round and 5 frequently asked interview questions for the technical round based on the job role {job_role}. Generate the response in two paragraphs with a heading of 'Interview Preparation' and for the other give a header 'Interview Questions' and two sub-headers as 'Technical Round Questions' and 'Interview Round Questions'. Kindly provide detailed recommendations and any additional advice you deem valuable.
    """
    generated_config_inter = GenerationConfig(temperature=0.6)
    response_inter = model.generate_content(input_inter, generation_config=generated_config_inter)
    generated_inter = ""
    for part in response_inter.parts:
        generated_inter += part.text.strip() + "\n"
    generated_inter = generated_inter.replace("*", "")

    input_role2 = f"""
    Based on this CV : {text}
    Suggest 3 courses from Coursera and Udemy which I can do to boost my technical skills for the job role: {job_role}. 
    Generate response by providing URLs for every generated course. Give a heading as 'Courses to Consider' and generate response from the next line.
    """
    generated_config2 = GenerationConfig(temperature=0.8)
    response2 = model.generate_content(input_role2, generation_config=generated_config2)
    generated_courses = ""
    for part in response2.parts:
        generated_courses += part.text.strip() + "\n"
    generated_courses = generated_courses.replace("*", "")

    input_role1 = f"""
    Suggest 3 alternative career paths for the following job role: {job_role}.
    Give a title to the response as 'Additional Career Paths' and generate from the next line.
    """
    generated_config1 = GenerationConfig(temperature=0.8)
    response1 = model.generate_content(input_role1, generation_config=generated_config1)
    generated_path = ""
    for part in response1.parts:
        generated_path += part.text.strip() + "\n"
    generated_path = generated_path.replace("*", "")
    urls = re.findall(r'https?://\S+', generated_courses)
    return generated_tech, generated_soft, generated_inter, generated_courses, generated_path, urls


def ret_text(session, start_key, end_key):
    result = ""
    for key, value in session.items():
        if start_key and key < start_key:
            continue
        if end_key and key > end_key:
            break
        if isinstance(value, str):
            result += value
        elif isinstance(value, list):
            result += ' '.join(map(str, value))
  # Join list elements into a single string
    return result

    


@app.route('/')
def start():
    return render_template('opening.html')

@app.route('/form')
def index():
    return render_template('form.html')

@app.route('/form_pdf')
def index_b():
    return render_template('form_pdf.html')

@app.route('/sub_pdf', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        session['goal']=request.form['goal']
        # Check if file was uploaded
        if 'file' not in request.files:
            return render_template('form_pdf.html', error='No file uploaded.')
        
        file = request.files['file']
        
        # Check if the file is a PDF
        if file.filename.endswith('.pdf'):
            # Save the uploaded PDF file
            file_path = 'uploaded_file.pdf'
            file.save(file_path)
            
            # Extract text from PDF
            extracted_text = extract_text(file_path)
            
            # Extract information from text (example: using regular expressions)
            name = re.search(r'Name: (.+)', extracted_text)
            age = re.search(r'Age: (\d+)', extracted_text)
            work_exp = re.search(r'work: (\d+)', extracted_text)
            job_role= re.search(r'cociri: (\d+)', extracted_text)
            degree= re.search(r'degree: (\d+)', extracted_text)
            achieve = re.search(r'achieevee: (\d+)', extracted_text)
            skills =re.search(r'skills: (\d+)', extracted_text)
            
            # Extract other relevant information similarly
            
            # Generate model response based on extracted text
            techgen,softgen,interviewgen,coursegen,pathgen, urls = get_model_response_pdf(extracted_text,session['goal'])
            sug_a=techgen+"\n"+softgen
            # Render template with extracted information and recommendations
            return render_template('ind.html',name=name, age=age, work_exp=work_exp, job_role=job_role, degree=degree, achievements=achieve, skils=skills, sugg_a=sug_a, interview=interviewgen, course=coursegen, link_out=urls, sugg_b=pathgen)

        else:
            return render_template('form_pdf.html', error='Please upload a PDF file.')
    
    # If GET request, render form for PDF upload
    return render_template('form_pdf.html')

@app.route('/sub_form', methods=['GET', 'POST'])
def input():
    error = None
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['address'] = request.form['address']
        session['mobile'] = request.form['mobile']
        session['age'] = request.form['age']
        session['languages'] = request.form['languages']
        session['qualification'] = request.form['qualification']
        session['work_exp'] = request.form['work_exp']
        session['projects'] = request.form['projects']
        session['skills'] = request.form['skills']
        session['achievements'] = request.form['achievements']
        session['co_curricular'] = request.form['co_curricular']
        session['goal'] = request.form['goal']
        # call the llm function here to generate output
        text_og = ret_text(session,session['age'],session['co_curricular'])
        techgen,softgen,interviewgen,coursegen,pathgen, urls = get_model_response_text(text_og,session['goal'])
        sug_a=techgen+"\n"+softgen
        #print(techgen+" "+softgen+" "+interviewgen+" "+coursegen+" "+pathgen+" "+urls)
    #return render_template('ind.html',name=session['name'], age=session['age'], work_exp=session['work_exp'], job_role=session['co_curricular'], degree=session['qualification'], achievements=session['achievements'], skils=session['skills'], sugg_a=session['skills'], interview=session['skills'], course=session['skills'], link_out=session['skills'], sugg_b=session['skills'])
    return render_template('ind.html',name=session['name'], age=session['age'], work_exp=session['work_exp'], job_role=session['co_curricular'], degree=session['qualification'], achievements=session['achievements'], skils=session['skills'], sugg_a=sug_a, interview=interviewgen, course=coursegen, link_out=urls, sugg_b=pathgen)

if __name__ == '__main__':
    app.run(debug=True)


