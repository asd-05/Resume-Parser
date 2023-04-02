import streamlit as st
import pandas as pd
import base64,random
import time,datetime
import streamlit.components.v1 as com

from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
import pymysql
from Courses import ds_course,web_course,android_course,ios_course,uiux_course,resume_videos,interview_videos
import plotly.express as px
import spacy
nlp = spacy.load("en_core_web_sm")

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout='wide',
    page_title="Resume Parser",
    page_icon='./Logo/respas2.ico',
)

with open("designs.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: white;
    }}
    
    </style>
    """,
    unsafe_allow_html=True
    )


def get_table_download_link(df,filename,text):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    # href = f'<a href="data:file/csv;base64,{b64}">Download Report</a>'
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)



# def course_recommender(course_list):
#     st.subheader("**Courses & Certificates🎓 Recommendations**")
#     c = 0
#     rec_course = []
#     no_of_reco = st.slider('Choose Number of Course Recommendations:', 1, 10, 4)
#     random.shuffle(course_list)
#     for c_name, c_link in course_list:
#         c += 1
#         st.markdown(f"({c}) [{c_name}]({c_link})")
#         rec_course.append(c_name)
#         if c == no_of_reco:
#             break
#     return rec_course

#CONNECTING TO DATABASE--
connection = pymysql.connect(host='localhost',user='root',password='',db='sra')
cursor = connection.cursor()

def insert_data(name,email,res_score,timestamp,no_of_pages,reco_field,cand_level,skills,recommended_skills,courses):
    DB_table_name = 'user_data'
    insert_sql = "insert into " + DB_table_name + """
    values (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    rec_values = (name, email, str(res_score), timestamp,str(no_of_pages), reco_field, cand_level, skills,recommended_skills,courses)
    cursor.execute(insert_sql, rec_values)
    connection.commit()

def run():
    st.markdown("<html><head><link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css' rel='stylesheet' integrity='sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD' crossorigin='anonymous'></head></head><link rel='stylesheet' href='<link href='https://fonts.googleapis.com/css2?family=Lobster+Two:ital@1&display=swap' rel='stylesheet'><link href='https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;1,400&display=swap' rel='stylesheet'><body><div class='headtextdiv'> <h1 class='resumeParser'>🔍 Resume Parser</h1><div class='flexbox'><div><h3 class='abouttext'>Streamlined Hiring, Scalable to Your Talent Acquisition Needs</h3><h4 class='abouttext2'> Make the hiring process twice as easy!</h4><h4 class='abouttext2'>Extract better quality data from CVs and spend less time on fixing mistakes in candidate profiles!</h4></div><img src='bg.jpg'></div></div><div class='cardsdiv'><div class='cardd'><h4 class='titleheading'>MY TITLE</h4><p class='desc'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid, reprehenderit cupiditate voluptas odit consequuntur modi tempore ipsum cum et. Magnam quo dolorum perferendis sint corporis nesciunt fugiat</p></div><div class='cardd'><h4 class='titleheading'>MY TITLE</h4><p class='desc'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid, reprehenderit cupiditate voluptas odit consequuntur modi tempore ipsum cum et. Magnam quo dolorum perferendis sint corporis nesciunt fugiat? Doloremque</p></div><div class='cardd'><h4 class='titleheading'>MY TITLE</h4><p class='desc'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Aliquid, reprehenderit cupiditate voluptas odit consequuntur modi tempore ipsum cum et. Magnam quo dolorum perferendis sint corporis nesciunt fugiat? Doloremque</p></div></div></body></html>", unsafe_allow_html=True)
    
    
    
    # st.markdown("<div class='h1box'> <h1 class='resumeParser'>🔍 Resume Parser</h1></div>", unsafe_allow_html=True)
    # st.markdown("<h3 class='abouttext'>About this app:</h3>", unsafe_allow_html=True)
    # st.markdown("<h4 > The *Resume Parser* app is an easy-to-use interface built in Streamlit for the amazing results using various python libraries like pyresparser and pdfminer !</h4>", unsafe_allow_html=True)
      
    # with st.expander("ℹ️ - About this app", expanded=True):
    
      
    st.markdown("")
    st.sidebar.markdown("# Choose Login")
    activities = ["Candidate Login", "Admin"]
    choice = st.sidebar.selectbox("Choose among the given options:", activities)
    # st.sidebar.markdown('''
    # ---
    # Created with ❤️ by     
    # [ANISH](https://github.com/asd-05)   
    # [REUBEN](https://github.com/ReubenArakkaparambil)    
    # [JOANNE](https://github.com/jo-daniel)    
    # [LAUKIK](https://github.com/laukik123)   
    # ''')
    img = Image.open('./Logo/respas1.jpg')
    # st.markdown("<h4 class='uploadresume'>🤷Tired of Searching for Jobs?</h4>", unsafe_allow_html=True)
    # st.markdown("<html><div class='uploadresumediv'><h4 class='h4'>Review and know your resume's score now!</h4><p id='uploadtext'>Get instant grade and feedback on how to improve your resume to be as effective as possible. </p></div></html>", unsafe_allow_html=True)
    # img = img.resize((450,350))
    # left_co, cent_co,last_co = st.columns(3)
    # with cent_co:
    #     st.image(img)

    # Create the DB
    db_sql = """CREATE DATABASE IF NOT EXISTS SRA;"""
    cursor.execute(db_sql)

    # Create table
    DB_table_name = 'user_data'
    table_sql = "CREATE TABLE IF NOT EXISTS " + DB_table_name + """
                    (ID INT NOT NULL AUTO_INCREMENT,
                     Name varchar(100) NOT NULL,
                     Email_ID VARCHAR(50) NOT NULL,
                     resume_score VARCHAR(8) NOT NULL,
                     Timestamp VARCHAR(50) NOT NULL,
                     Page_no VARCHAR(5) NOT NULL,
                     Predicted_Field VARCHAR(25) NOT NULL,
                     User_level VARCHAR(30) NOT NULL,
                     Actual_skills VARCHAR(300) NOT NULL,
                     Recommended_skills VARCHAR(300) NOT NULL,
                     Recommended_courses VARCHAR(600) NOT NULL,
                     PRIMARY KEY (ID));
                    """
    cursor.execute(table_sql)
    if choice == 'Candidate Login':
        st.markdown("<html><div class='uploadresumediv'><h4 class='h4'>Review and know your resume's score now!</h4><p id='uploadtext'>Get instant grade and feedback on how to improve your resume to be as effective as possible. </p></div></html>", unsafe_allow_html=True)
        pdf_file = st.file_uploader("Choose your Resume", type=["pdf"])
        if pdf_file is not None:
            with st.spinner('Uploading your Resume....'):
                time.sleep(2)
            save_image_path = './Uploaded_Resumes/'+pdf_file.name
            with open(save_image_path, "wb") as f:
                f.write(pdf_file.getbuffer())
            show_pdf(save_image_path)
            resume_data = ResumeParser(save_image_path).get_extracted_data()
            if resume_data:
                ## Get the whole resume data
                resume_text = pdf_reader(save_image_path)

                st.header("Resume Analysis")
                st.success("Hello "+ resume_data['name'])
                st.subheader("Your Basic info")
                try:
                    st.text('Name: '+resume_data['name'])
                    st.text('Email: ' + resume_data['email'])
                    st.text('Contact: ' + resume_data['mobile_number'])
                    st.text('Resume pages: '+str(resume_data['no_of_pages']))
                except:
                    pass
                cand_level = ''
                if resume_data['no_of_pages'] == 1:
                    cand_level = "Fresher"
                    st.markdown( '''<h4 style='text-align: left; color: #d73b5c;'>You are looking Fresher.</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] == 2:
                    cand_level = "Intermediate"
                    st.markdown('''<h4 style='text-align: left; color: #00337C;'>You are at intermediate level!</h4>''',unsafe_allow_html=True)
                elif resume_data['no_of_pages'] >=3:
                    cand_level = "Experienced"
                    st.markdown('''<h4 style='text-align: left; color: #23425F;'>You are at experience level!''',unsafe_allow_html=True)

                st.subheader("Skills Recommendation💡")
                ## Skill shows
                keywords = st_tags(label='Skills that you have',
                text='',
                    value=resume_data['skills'],key = '1')

                ##  recommendation
                ds_keyword = ['tensorflow','keras','pytorch','machine learning','deep Learning','flask','streamlit']
                web_keyword = ['react', 'django', 'node jS', 'react js', 'php', 'laravel', 'magento', 'wordpress',
                               'javascript', 'angular js', 'c#', 'flask']
                android_keyword = ['android','android development','flutter','kotlin','xml','kivy']
                ios_keyword = ['ios','ios development','swift','cocoa','cocoa touch','xcode']
                uiux_keyword = ['ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping','wireframes','storyframes','adobe photoshop','photoshop','editing','adobe illustrator','illustrator','adobe after effects','after effects','adobe premier pro','premier pro','adobe indesign','indesign','wireframe','solid','grasp','user research','user experience']

                recommended_skills = []
                reco_field = ''
                rec_course = ''
                ## Courses recommendation
                for i in resume_data['skills']:
                    ## Data science recommendation
                    if i.lower() in ds_keyword:
                        print(i.lower())
                        reco_field = 'Data Science'
                        st.success(" Our analysis says you are looking for Data Science Jobs.")
                        recommended_skills = ['Data Visualization','Predictive Analysis','Statistical Modeling','Data Mining','Clustering & Classification','Data Analytics','Quantitative Analysis','Web Scraping','ML Algorithms','Keras','Pytorch','Probability','Scikit-learn','Tensorflow',"Flask",'Streamlit']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '2')
                        # st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        # rec_course = course_recommender(ds_course)
                        break

                    ## Web development recommendation
                    elif i.lower() in web_keyword:
                        print(i.lower())
                        reco_field = 'Web Development'
                        st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Our analysis says you are looking for Web Development Jobs!''',unsafe_allow_html=True)
                        recommended_skills = ['React','Django','Node JS','React JS','php','laravel','Magento','wordpress','Javascript','Angular JS','c#','Flask','SDK']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '3')
                        # st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        # rec_course = course_recommender(web_course)
                        break

                    ## Android App Development
                    elif i.lower() in android_keyword:
                        print(i.lower())
                        reco_field = 'Android Development'
                        st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Our analysis says you are looking for Android Devlopment Jobs!''',unsafe_allow_html=True)
                        recommended_skills = ['Android','Android development','Flutter','Kotlin','XML','Java','Kivy','GIT','SDK','SQLite']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '4')
                        # st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        # rec_course = course_recommender(android_course)
                        break

                    ## IOS App Development
                    elif i.lower() in ios_keyword:
                        print(i.lower())
                        reco_field = 'IOS Development'
                        st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Our analysis says you are looking for IOS Development Jobs!''',unsafe_allow_html=True)
                        recommended_skills = ['IOS','IOS Development','Swift','Cocoa','Cocoa Touch','Xcode','Objective-C','SQLite','Plist','StoreKit',"UI-Kit",'AV Foundation','Auto-Layout']
                        recommended_keywords = st_tags(label='### Recommended skills for you.',
                        text='Recommended skills generated from System',value=recommended_skills,key = '5')
                        # st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                        # rec_course = course_recommender(ios_course)
                        break

                    ## Ui-UX Recommendation
                    # elif i.lower() in uiux_keyword:
                    #     print(i.lower())
                    #     reco_field = 'UI-UX Development'
                    #     st.success(" Our analysis says you are looking for UI-UX Development Jobs ")
                    #     recommended_skills = ['UI','User Experience','Adobe XD','Figma','Zeplin','Balsamiq','Prototyping','Wireframes','Storyframes','Adobe Photoshop','Editing','Illustrator','After Effects','Premier Pro','Indesign','Wireframe','Solid','Grasp','User Research']
                    #     recommended_keywords = st_tags(label='### Recommended skills for you.',
                    #     text='Recommended skills generated from System',value=recommended_skills,key = '6')
                    #     # st.markdown('''<h4 style='text-align: left; color: #2E3840;'>Adding this skills to resume will boost🚀 the chances of getting a Job💼</h4>''',unsafe_allow_html=True)
                    #     # rec_course = course_recommender(uiux_course)
                    #     break

                ## Insert into table
                ts = time.time()
                cur_date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                cur_time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                timestamp = str(cur_date+'_'+cur_time)

                ### Resume writing recommendation
                st.subheader("**Resume Tips & Ideas💡🚀**")
                resume_score = 0
                if 'Objective' in resume_text:
                    resume_score = resume_score+20
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[+] Awesome! You have added Objective</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[-] According to our recommendation please add your career objective, it will give your career intension to the Recruiters.</h4>''',unsafe_allow_html=True)

                if 'Declaration'  in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[+] Awesome! You have added Delcaration✍/h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[-] According to our recommendation please add Declaration✍. It will give the assurance that everything written on your resume is true and fully acknowledged by you</h4>''',unsafe_allow_html=True)

                if 'Hobbies' or 'Interests'in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[+] Awesome! You have added your Hobbies⚽</h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[-] According to our recommendation please add Hobbies⚽. It will show your persnality to the Recruiters and give the assurance that you are fit for this role or not.</h4>''',unsafe_allow_html=True)

                if 'Achievements' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[+] Awesome! You have added your Achievements🏅 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[-] According to our recommendation please add Achievements🏅. It will show that you are capable for the required position.</h4>''',unsafe_allow_html=True)

                if 'PROJECTS' in resume_text:
                    resume_score = resume_score + 20
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[+] Awesome! You have added your Projects👨‍💻 </h4>''',unsafe_allow_html=True)
                else:
                    st.markdown('''<h5 style='text-align: left; color: #2E3840;'>[-] According to our recommendation please add Projects👨‍💻. It will show that you have done work related the required position or not.</h4>''',unsafe_allow_html=True)

                st.subheader(" Resume Score📝")
                st.markdown(
                    """
                    <style>
                        .stProgress > div > div > div > div {
                            background-color: #d73b5c;
                        }
                    </style=>""",
                    unsafe_allow_html=True,
                )
                my_bar = st.progress(0)
                score = 0
                for percent_complete in range(resume_score):
                    score +=1
                    time.sleep(0.1)
                    my_bar.progress(percent_complete + 1)
                st.success(' Your Resume Writing Score is: ' + str(score))
                st.warning(" Note: This score is calculated based on the content that you have added in your Resume.")
                st.balloons()

                insert_data(resume_data['name'], resume_data['email'], str(resume_score), timestamp,
                              str(resume_data['no_of_pages']), reco_field, cand_level, str(resume_data['skills']),
                              str(recommended_skills), str(rec_course))

                connection.commit()
            else:
                st.error('Something went wrong..')
            st.markdown("<div class='footer'><h2 class='footertext'>Created with ❤ by:<a class='a' href='https://github.com/asd-05'>Anish</a><a class='a' href='https://github.com/ReubenArakkaparambil'>Reuben</a><a class='a' href='https://github.com/jo-daniel'>Joanne</a><a class='a' href='https://github.com/laukik123'>Laukik</a></h2></div>", unsafe_allow_html=True)
            
            # st.markdown("<footer id='footer'><div class='container-fluid'><div class='footingfoot'><h2 id='foot1bada'>Contact us</h2><p id='foot1chota'><a href="">Our Institution</a></p><br><p id='foot1chota'><a href="">Contributors</a></p><h2 id='foot2bada'>Creators</h2><p id='foot2chota'><a href="">Reuben </a></p><br><p id='foot2chota'><a href="">Laukik</a></p><br><p id='foot2chota'><a href="">Joanne</a></p><br><p id='foot2chota'><a href=""> Anish</a></p><h6 id='finalending'>© Team LaJr | All rights reserved</h6></div></div></footer>", unsafe_allow_html=True)

            # st.markdown("<footer class='footer'><div class='container'><div class='row'><div class='footer-col'><h4>company</h4><ul><li><a href='#'>about us</a></li><li><a href='#'>our services</a></li><li><a href='#'>privacy policy</a></li></ul></div><div class='footer-col'><h4>Contributors</h4><ul><li><a href='#'>Reuben</a></li><li><a href='#'>Anish</a></li><li><a href='#'>Laukik</a></li><li><a href='#'>Joanne</a></li></ul></div><div class='footer-col'><h4>follow us</h4><div class='social-links'><a href='#'><i class='fab fa-facebook-f'></i></a><a href='#'><i class='fab fa-twitter'></i></a><a href='#'><i class='fab fa-instagram'></i></a><a href='#'><i class='fab fa-linkedin-in'></i></a></div></div></div></div></footer>",unsafe_allow_html=True )

    else:
        ## Admin Side
        st.markdown("<html><div class='uploadresumediv'><h4 class='h4'>Welcome to Admin Side</h4><h3 class='login'>Enter login credentials</h3></div></html>", unsafe_allow_html=True)
       
        ad_user = st.text_input("Enter Username")
        ad_password = st.text_input("Enter Password", type='password')
        if st.button('Login'):
            if ad_user == 'resume_parser' and ad_password == 'test1234':
                # st.success("Welcome Admin")
                st.markdown("<h4 class='adminwelcome'>Welcome Admin</h4>", unsafe_allow_html=True)
                # Display Data
                cursor.execute('''SELECT*FROM user_data''')
                data = cursor.fetchall()
                # st.header("User's👨‍💻 Data")
                st.markdown("<h4 class='admindisc'>Applicant's data</h4>", unsafe_allow_html=True)
                df = pd.DataFrame(data, columns=['ID', 'Name', 'Email', 'Resume Score', 'Timestamp', 'Total Page',
                                                 'Predicted Field', 'User Level', 'Actual Skills', 'Recommended Skills',
                                                 'Recommended Course'])
                st.dataframe(df)
                st.markdown(get_table_download_link(df,'User_Data.csv','Download Report'), unsafe_allow_html=True)
                ## Admin Side Data
                query = 'select * from user_data;'
                plot_data = pd.read_sql(query, connection)

                ## Pie chart for predicted field recommendations
                labels = plot_data.Predicted_Field.unique()
                print(labels)
                values = plot_data.Predicted_Field.value_counts()
                print(values)
                # st.subheader("📈 Pie-Chart for Predicted Field Recommendations ")
                st.markdown("<h4 class='admindisc'>Pie-Chart for Predicted Field Recommendations</h4>", unsafe_allow_html=True)
                fig = px.pie(df, values=values, names=labels, title='Predicted Field according to the Skills')
                st.plotly_chart(fig)

                ### Pie chart for User's👨‍💻 Experienced Level
                labels = plot_data.User_level.unique()
                values = plot_data.User_level.value_counts()
                # st.subheader("📈 Pie-Chart for User's👨‍💻 Experienced Level ")
                st.markdown("<h4 class='admindisc'>Pie-Chart for User's👨‍💻 Experience Level</h4>", unsafe_allow_html=True)
                fig = px.pie(df, values=values, names=labels, title="Pie-Chart📈 for User's👨‍💻 Experienced Level")
                st.plotly_chart(fig)

                # st.markdown("<div class='footer'><h2 class='footertext'>Created with ❤ by:<a class='a' href='https://github.com/asd-05'>Anish</a><a class='a' href='https://github.com/ReubenArakkaparambil'>Reuben</a><a class='a' href='https://github.com/jo-daniel'>Joanne</a><a class='a' href='https://github.com/laukik123'>Laukik</a></h2></div>", unsafe_allow_html=True)
                
                # st.markdown("<div class='footer'><h2 class='footertext'>Created with ❤ by:<a class='a' href='https://github.com/asd-05'>Anish</a><a class='a' href='https://github.com/ReubenArakkaparambil'>Reuben</a><a class='a' href='https://github.com/jo-daniel'>Joanne</a><a class='a' href='https://github.com/laukik123'>Laukik</a></h2></div>", unsafe_allow_html=True)
                # st.markdown("<footer id='footer'><div class='container-fluid'><div class='footingfoot'><h2 id='foot1bada'>Contact us</h2><p id='foot1chota'><a href="">Our Institution</a></p><br><p id='foot1chota'><a href="">Contributors</a></p><p id='foot2bada'>Creators</p><p id='foot2chota'><a href="">Reuben </a></p><br><p id='foot2chota'><a href="">Laukik</a></p><br><p id='foot2chota'><a href="">Joanne</a></p><br><p id='foot2chota'><a href=""> Anish</a></p><h6 id='finalending'>© Team LaJr | All rights reserved</h6></div></div></footer>", unsafe_allow_html=True)

                st.markdown("<footer class='footer'><div class='containerf'><div class='row'><div class='footer-col'><h4>company</h4><ul><li><a href='#'>about us</a></li><li><a href='#'>our services</a></li><li><a href='#'>privacy policy</a></li></ul></div><div class='footer-col'><h4>Contributors</h4><ul><li><a href='#'>Reuben</a></li><li><a href='#'>Anish</a></li><li><a href='#'>Laukik</a></li><li><a href='#'>Joanne</a></li></ul></div><div class='footer-col'><h4>follow us</h4><div class='social-links'><a href='#'><i class='fab fa-facebook-f'></i></a><a href='#'><i class='fab fa-twitter'></i></a><a href='#'><i class='fab fa-instagram'></i></a><a href='#'><i class='fab fa-linkedin-in'></i></a></div></div></div></div></footer>",unsafe_allow_html=True )
            else:
                st.error("Wrong ID & Password Provided")
run()