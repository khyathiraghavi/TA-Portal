# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

from gluon.sqlhtml import form_factory
import socket


CAS.login_url='https://login.iiit.ac.in/cas/login'
CAS.check_url='https://login.iiit.ac.in/cas/validate'
CAS.logout_url='https://login.iiit.ac.in/cas/logout'
CAS.my_url='http://127.0.0.1:8000/taship1/default/login'

# ---------- HOME PAGE IS SAME FOR ALL THE USERS --------------------

if not session.token and not request.function=='login':
	redirect(URL(r=request, f='login'))

def login():
    session.login = 0 
    session.token = CAS.login(request)	
    if (db(db.Semester.id ==2).select()):
       session.current_semester = db(db.Semester.id == 2 ).select()[0].semname
    return dict(mesg="taship")

def logout():
    session.token=None
    CAS.logout()


def home_page():
	if session.login == 0 :
		if (session.token and session.token.split('@')[1] == "students.iiit.ac.in"):
			emailValue = db(db.Admin.ademail_id == session.token).select(db.Admin.ademail_id)
			if( emailValue ):
				redirect(URL(r=request,f='sp_check'))
			else:
				session.login = 2
				session.student_email = session.token
		if (session.token and session.token.split('@')[1] == "research.iiit.ac.in"):
			emailValue = db(db.Admin.ademail_id == session.token).select(db.Admin.ademail_id)
			if( emailValue ):
				redirect(URL(r=request,f='sp_check'))
			else:
				session.login = 2
				session.student_email = session.token
		elif(session.token and session.token.split('@')[1] == 'iiit.ac.in' ):
		      	emailValue = db(db.Admin.ademail_id == session.token).select(db.Admin.ademail_id)	
			if( emailValue ):
				redirect(URL(r=request,f='sp_check'))
			else :
				session.faculty_login_emailid = session.token
				session.login = 3
				session.token = session.token
	else:
		session.token = session.token
	return dict(mesg=session.token)

def sp_check():
	return dict(mesg="taship")
	

#---- General Function for all -----------------     
def courses_info():
    r=db((db.Course.id==db.Teach.course_id) & (db.Teach.faculty_id == db.Faculty.id))\
    	.select(db.Course.cname,db.Course.cid,db.Course.cdts,db.Course.hours_per_week,db.Faculty.fname,orderby=db.Course.cname)
    return  dict(r=r)


def contacts():
	r=db(db.Admin.id>0).select()
	return dict(r=r)

     
def match_password(email, passwd,addr): 
# FUNCTION FOR VALIDATION OF USERNAME AND PASSWORD 
    f = email.split('@')
    username = f[0]
    try:
        address = addr 
        service_port = 61237
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address,service_port))
        tosend = 'auth ' + username + ' ' + passwd + '\r\n' # authorization format
        sent = s.send(tosend)
        chunk = s.recv(128)
        s.close()
        if (chunk == '1 match'+'\n' ):
            return '1';
    except:
        return False

## ---TEMPORARY----
#def truncate():
# FUNCTION TO DELETE ALL THE ENTRIES OF THE TABLE 
#   db.Course.truncate()
#   db.Applicant.truncate()
#   db.Faculty.truncate()
#   db.Semester.truncate()
#   db.AppliedFor.truncate()
#   db.OfferedTo.truncate()
#   db.Teach.truncate()
#   db.SelectedTA.truncate()

#   return dict()

# -----------  NEWMAIL FUNCTION FOR SENDING MAILS TO THE ADMIN FACULTY AND TAS -------------
import smtplib
import gluon

class NewMail(object):
	def __init__(self):
		self.settings = gluon.tools.Settings()
		self.settings.server = 'smtp.gmail.com:587'
		self.settings.use_tls = True
		self.settings.sender = ''
		self.settings.login = ""
		self.settings.lock_keys = True
	def send(self,to,subject,mesg):
			try:
				(host, port) = self.settings.server.split(':')
				server = smtplib.SMTP(host, port)
				if self.settings.login:
		         		server.ehlo()
				  	server.ehlo()
					(username, password) = self.settings.login.split(':')
				mesg = "From: %s\n"%(self.settings.sender)+"To: %s\n" %(to)+"Subject: %s\n" % (subject)+"\r\n"+(mesg)+"\r\n"
				server.sendmail(self.settings.sender, to, mesg)
			 	server.quit()
			except Exception, e:
				print e
				return False
			return True



def sendmail(sender,reciever,subj,title):


	mail=NewMail()
# specify server
	mail.settings.server='students.iiit.ac.in:25'
	mail.settings.login='username:password' or None


# specify address to send as
	mail.settings.sender=sender


#       mail.settings.lock_keys=True
	mail.settings.use_tls=True
#       return mail.settings.keys()
#send the message
	print "Mail to be sent"
	return mail.send(to=reciever, subject=title, mesg=subj)

# ----->>>    Temporary mail server is kept "students.iiit.ac.in" <<<<-------------------

#------ ADMIN LOGIN FUNCITON -------------
# FUNCTION GENERATE FOLLOWING SESSION VARIABLES
# session.login = 1
# session.admin_email = email of admin logged in

def admin_login():
    form = form_factory(
            SQLField('Username', 'string', requires = IS_NOT_EMPTY()),
            SQLField('Password', 'password', requires = IS_NOT_EMPTY()))

    if form.accepts(request.vars, session):
        username = request.vars.Username
        password = request.vars.Password
	#if valid username then check password with the server
        emailValue = db(db.Admin.adname == username).select(db.Admin.ademail_id)	
        if(emailValue):
            for row in emailValue:
                email = row.ademail_id
                value = match_password(email, password, 'iiit.ac.in')
	    if(value == '1'):							# login successful
                session.login = 1
		session.admin_email = email
		session.flash = 'Login Successful'
            else:								# login failure
		response.flash = 'Incorrect Username or Password'+str(value)
        else:
	    response.flash = 'Incorrect Username or Password'			# incorrect username
    return dict(form=form)

#----- STUDENT LOGIN FUNCTION -------
# FUNCTION GENERATES FOLLOWING SESSION VARIABLES 
# session.login=2
# session.student_email=email

def student_login(): 	
   # form is created in views/student_login.html 
    if(request.vars.submit):
        email = request.vars.username + '@' + request.vars.email
        passwd = request.vars.password
        value = match_password(email, passwd, request.vars.email)
        if(value == '1'):
            session.login = 2
            session.student_email = email
	    session.flash = 'Login Successful'
        else: 
	    response.flash = 'Incorrect Username or Password'
    return dict()

# >>>>    Temporary mail server is students.iiit.ac.in <<<<<<<<<
#--------- FACULTY LOGIN ---------
# FUNCTION GENERATES FOLLOWING SESSION VARIABLES
# session.login=3
# session.faculty_login_email = email_of_faculty_loggedin

def faculty_login():
    form = form_factory(
            SQLField('Username', 'string', label = 'Username  ', requires = IS_NOT_EMPTY()),
            SQLField('Password', 'password', label = 'Password  ', requires = IS_NOT_EMPTY()))

    if form.accepts(request.vars, session):
        username = request.vars.Username
        password = request.vars.Password
        value = match_password(username, password, 'mail.iiit.ac.in')
        if(value == '1'):
            session.login = 3
	    session.faculty_login_emailid = username
	    session.flash = 'Login Succesful'
        else:
	    response.flash = 'Incorrect Username or Password'
    return dict(form=form)

def logout1():
   	# updating all the session variables used to default => no user is logged in
        session.login = 0
        session.student_email = 0
	session.admin_email = 0
	session.faculty_login_emailid = 0
#	session.flash = "Successfully Logged out"
	redirect(URL(r = request, f = 'logout'))
	return dict()

# -------------- Applicant related queries  starts here ------------------------

import datetime
def TA_application():
   # checking whether applicant is logged in or not
    if session.login != 2 :		
       redirect(URL(r = request , f = 'index'))
       return dict()

    msg = ''							#  msg is for returning to the html file		
    record = []							#  record stores the info of the applicant if he has already applied 
    session.alreadyThereFlag = 0 					#  used in the corresponding html file to see if an applicant has already applied or not
    now = datetime.datetime.now()
    deadline_start = datetime.datetime(2010,12,27,0,0,0)
    deadline_end = datetime.datetime(2010,12,29,17,0,0)
    if now < deadline_start:
        session.flash = 'Wait till %s'%deadline_start.strftime('%d %B %Y %I:%M%p')
        redirect(URL(r=request,f='index'))
    elif now > deadline_end: # and auth.user.id != 149:
        session.flash = 'Deadline over at %s'%deadline_end.strftime('%d %B %Y %I:%M%p')
        redirect(URL(r=request,f='home_page'))


    if db(db.Applicant.apemail_id == session.student_email).select():   # if an applicant is already applied 
        session.alreadyThereFlag = 1 				     	
        applicantInfo = db((db.Applicant.apemail_id == session.student_email) & (db.Applicant.program_id == db.Program.id)).select()
	for rows in applicantInfo:
		 record.append(rows.Applicant.apname)
		 record.append(rows.Applicant.aprollno)
		 record.append(rows.Program.pname)
		 record.append(rows.Applicant.apcgpa)
		 record.append(rows.Applicant.phoneno)
		 if rows.Applicant.prev_exp == True :
		 	record.append('Yes')
		 else:
		    	record.append('No')
    	form = form_factory(						# creating a form for the applicant to select course
            SQLField('course', label = 'Course', requires = IS_IN_DB(db, 'Course.id', '%(cname)s ( %(cid)s )')),
            SQLField('grade', label = 'Grade In The Course', requires = IS_IN_SET(['A','A-','B','B-','C','NA'])))
    else:							# ------------ else if the applicant has applied for the first time ---------------	
	    form = form_factory(
        	    SQLField('name', 'string', label = 'Name', requires = IS_NOT_EMPTY()),
        	    SQLField('rollno', 'integer', label = 'Roll No',requires = IS_NOT_EMPTY()),
	            SQLField('program', label = 'Program Of Study', requires = IS_IN_DB(db,'Program.id','%(pname)s')),
	    #        SQLField('course', label = 'Course', requires = IS_IN_DB(db, 'Course.id', '%(cname)s ( %(cid)s )')),
	    #  	     SQLField('grade', label = 'Grade In The Course', requires = IS_IN_SET(['A','A-','B','B-','C','NA'])),
        	    SQLField('CGPA', 'double', requires = IS_FLOAT_IN_RANGE(0,10)),
	            SQLField('phone', 'integer', label = 'Phone No'),
	            SQLField('experience', label = 'Previous Experience', requires = IS_IN_SET(['YES','NO'])))

    if form.accepts(request.vars, session):  			# ----------------- if the form is submitted ----------------------------
        name = request.vars.name
        rollno = request.vars.rollno
        program = request.vars.program
        course = request.vars.course
        grade = request.vars.grade
        cgpa = request.vars.CGPA
        phone = request.vars.phone
        exp = request.vars.experience

	if request.vars.experience == 'YES':
	   exp = True
	else:
	   exp = False

        if(session.alreadyThereFlag == 1):			
	    r = db(db.Applicant.apemail_id == session.student_email).select()
	    for rows in applicantInfo:
	         appid = rows.Applicant.id
        else:							# ----------- else insert and get the .id of the applicant ----------	
            appid = db.Applicant.insert(apname = name, aprollno = rollno , apemail_id = session.student_email, \
		  apcgpa = cgpa, phoneno = phone, prev_exp = exp, program_id = program)
	    mesg = "Profile Successfully Updated !! "
    
        s = db((db.AppliedFor.appid == appid) & (db.AppliedFor.cid == course)).select()	# ---- if he/she has applied for the course -----------
        if(s):
            a = 1
	    session.flash = 'You have already applied for this course'
	    redirect(URL(r = request, f = 'TA_application'))
        else:
	    # else fill info in the database 
            db.AppliedFor.insert(appid = appid , cid = course, noflag = 0, timestamp = datetime.date.today(), grade = grade) 
	    if(session.alreadyThereFlag == 1):
		session.flash = 'Thank You for Application'
	    else :
		session.flash = mesg
	    redirect(URL(r = request, f = 'TA_application'))

    return dict(form = form, record = record)

def student_profile():
   	if ( session.login != 2 ):
	   redirect(URL(r=request, f='index'))
	   return dict()
	
	records = db((db.Applicant.apemail_id == session.student_email) & (db.Applicant.program_id == db.Program.id)).select()
	records_appliedfor = db((db.AppliedFor.appid == db.Applicant.id) & (db.AppliedFor.cid == db.Course.id) &\
	      (db.Applicant.apemail_id == session.student_email) & (db.Applicant.program_id == db.Program.id)).select()
	records_selectedfor = db((db.SelectedTA.appid == db.Applicant.id) & (db.SelectedTA.cid == db.Course.id) &\
	      (db.Applicant.apemail_id == session.student_email) & (db.Applicant.program_id == db.Program.id)).select()
	return dict(records = records , records_appliedfor=records_appliedfor,records_selectedfor=records_selectedfor)


#----------- FUNCTIONALITY FOR ADMIN -----------

def add_courses():
   if (session.login != 1) :
      redirect(URL(r = request, f = 'index'))
      return dict()

   #-------------------------  CREATING FORM FOR THE NEW COURSE ------------------------------------
   form = form_factory(
           SQLField('Cname', 'string', label = 'Course Name', requires = IS_NOT_EMPTY(error_message = T('fill this'))),
           SQLField('Cid', 'string', label = 'Course Id', requires = IS_NOT_EMPTY(error_message = T('fill this'))),
           SQLField('Cofferto', label = 'Course Offered To', requires = IS_IN_DB(db, 'Program.id', '%(pname)s')),
           SQLField('Profname', label = 'Name Of The Professor',requires = IS_NOT_EMPTY(error_message = T('fill this'))),
           SQLField('ProfEmail', 'string', label = 'Email Of The Professor', requires = [IS_NOT_EMPTY(error_message = T('fill this')), IS_EMAIL()]),
           SQLField('No_of_credits', 'integer', label = 'No Of Credits', requires = IS_NOT_EMPTY(error_message = T('fill this'))),
#          SQLField('NofullTA', label = 'No Of Full TAs Required'),
#	   SQLField('NohalfTA', label = 'No Of Half TAs Required'),
#	   SQLField('NoqrtTA', label = 'No Of Quarter TAs Required'),
	   SQLField('No_of_Hours', label = 'No. Of Hours Per Week'),
	   SQLField('coursetype', 'string', label = 'Type Of Course', requires = IS_IN_SET(['Full','Half'])),
	   SQLField('semester', label = 'Semester', requires = IS_IN_DB(db, 'Semester.id', '%(semname)s')))
    
   if form.accepts(request.vars, session):
      # STORING THE ENTERED VALUES IN VARIABLES 
       cname = request.vars.Cname
       cid = request.vars.Cid
       cofferto = request.vars.Cofferto
       profname = request.vars.Profname
       profemail = request.vars.ProfEmail
       cdts = request.vars.No_of_credits
#       ft = request.vars.NofullTA
#       ht = request.vars.NohalfTA
#       qt = request.vars.NoqrtTA
       ctype = request.vars.coursetype
       semid = request.vars.semester
       hours = request.vars.No_of_Hours

       r = db(db.Course.cid == cid).select() 
       if(r):			
	   # if course is already there in the database
           a = 1
           for i in r:
	      use_id = i.id 								# if yes then  use_id <= Course.id of that course
       else:										# else insert that course						
             use_id = db.Course.insert(cid = cid, cname = cname, cdts = cdts,\
		   no_of_qta = 0, no_of_hta = 0, no_of_fta = 0, coursetype = ctype, sem_id = semid, hours_per_week = hours)

       s = db(db.Faculty.femail_id == profemail).select()	
       if(s):										# if faculty is already present in the database
          for i in s:
	     newprof_id = i.id 								# if yes then newprof_if <= Faculty.id of that faculty			
       else:
            newprof_id = db.Faculty.insert(fname = profname, femail_id = profemail)		# else insert that faculty
      
       k = db((db.Teach.faculty_id == newprof_id) & (db.Teach.course_id == use_id)).select()
       if(k):										# if both of them are present in TEACH table do nothing		
           a = 1
       else:
	   # else insert	
 	   db.Teach.insert(faculty_id = newprof_id, course_id = use_id)
       	   response.flash = "Course Successfully added !!!"
       
       offer = db((db.OfferedTo.cid == use_id) & (db.OfferedTo.programid == cofferto)).select()	# insert in OfferedTo table
       if(offer):
           a = 1
       else:
	   db.OfferedTo.insert(cid = use_id, programid = cofferto)
           
   return dict(form=form)


def delete_courses():
   	if session.login != 1:						# -------- check if admin has logged in or not -------------------
	      redirect(URL(r = request, f = 'index'))
	      return dict()

	form = form_factory(						# -------- creating form for the delete course --------------			
	      SQLField('course', label = 'Select Course  ', requires = IS_IN_DB(db, 'Course.id', '%(cname)s  ( %(cid)s ) ' )),
	      SQLField('cofferto', label = 'Select Program ', requires = IS_IN_DB(db, 'Program.id', '%(pname)s')))
        return dict(form=form)
		 
def namewise_list():
# ALLOWS ADMIN TO SEE THE APPLICANT LIST NAMEWISE 
   	if (session.login != 1) :
	      redirect(URL(r = request, f = 'index'))
	      return dict()

	r = ''
# form for select the applicant name 
	form = form_factory(	
	      SQLField('applicantId', label = 'Select Applicant', requires = IS_IN_DB(db, 'Applicant.id',\
		    '%(apname)s (%(aprollno)s)')))
	if form.accepts(request.vars, session):
	      r = db((db.Applicant.id == db.AppliedFor.appid) & (db.Course.id == db.AppliedFor.cid) &\
		    (db.Applicant.id == request.vars.applicantId)).select()
	return dict(form = form, msg = r)

#------------------ ALLOWS ADMIN TO SEE THE LIST OF SELECTED APPLICANTS CATEGORY WISE eg: NAME, COURSE, ROLLNO etc.......-------------------
def selected_TA():
	   if session.login !=1 :
	      redirect(URL(r = request, f = 'index'))
	      return dict()
	   return dict()

#----------------- DISPLAYS THE LIST OF APPLICANTS FOR A SELECTED COURSE -----------------------------------------------
def admin_applicant_list():
   	if session.login!=1:
	      redirect(URL(r=request,f='index'))
	      return dict()

# session.admin_flag = 0 means form not accepted 
	session.admin_flag = '0'		
	records = ''
	#----- DICT FOR SORTING -------
	array = {'Overall CG':'apcgpa', 'Grade In That Course':'grade', 'Previous Experience':'prev_exp',\
	      'Programme Of Study':'pname'}

	form = form_factory(
			SQLField('course', label = "Select Course ", requires = IS_IN_DB(db, 'Course.id', '%(cname)s ( %(cid)s )')),
			SQLField('pr1', label = "Priority 1", requires = IS_IN_SET(['Overall CG',\
			      'Grade In That Course', 'Previous Experience','Programme Of Study'])),
			SQLField('pr2', label = "Priority 2", requires = IS_IN_SET(['Overall CG','Grade In That Course',\
			      'Previous Experience','Programme Of Study'])),
			SQLField('pr3', label = "Priority 3", requires = IS_IN_SET(['Overall CG', 'Grade In That Course', \
			      'Previous Experience', 'Programme Of Study'])))
	if form.accepts(request.vars,session):
		var1 = array[request.vars.pr1]
		var2 = array[request.vars.pr2]
		var3 = array[request.vars.pr3]
		var = var1 + '|~' + var2 + '|~' + var3
		# sorting the applicants on the priorities selected by the admin and storing in records 
		records = db((db.AppliedFor.cid == request.vars.course) & (db.Applicant.id == db.AppliedFor.appid) & \
		      (db.AppliedFor.cid == db.Course.id) & (db.Applicant.program_id == db.Program.id)).select(db.Applicant.apname, \
		      db.Applicant.aprollno, db.Applicant.apemail_id, db.Program.pname, db.AppliedFor.grade, db.Applicant.apcgpa, orderby=(var))
		# form accepted
		session.admin_flag = '1'  
		# redirecting to next form 
		redirect(URL(r = request, f = 'admin_applicant_list_2', args = [request.vars.course, var1, var2, var3]))
	return dict(form = form, records = records)

#--------------------- NEXT PART OF THE ABOVE QUERY -------------------------
def admin_applicant_list_2():
   	if (session.login != 1) :
	      redirect(URL(r = request, f = 'index'))
	      return dict()
	session.admin_varCid = request.args[0]
	session.admin_varPr1 = request.args[1]
	session.admin_varPr2 = request.args[2]
	session.admin_varPr3 = request.args[3]

	var = request.args[1] + ',' + request.args[2] + ',' + request.args[3]
	records = db((db.AppliedFor.cid == request.args[0]) & (db.Applicant.id == db.AppliedFor.appid) & (db.AppliedFor.cid == db.Course.id) & \
	      (db.Applicant.program_id == db.Program.id)).select(orderby = (var))
	return dict(records=records)

def admin_applicant_list_3():
   	if ( session.login != 1 ):
	      redirect(URL(r = request, f = 'index'))
	      return dict()
	return dict()
 
#---------- FUNCTION FOR MAKING THE SUBJECT TO BE SENDED TO THE TAs ---------------------------
def MakeStringForTA(course,sem, roll):
	admin = db(db.Admin.id > 0).select(db.Admin.ademail_id)[0]
	courseName = db(db.Course.cid == course).select()[0]
	string = "You Have been selected as " + session.admin_rollType[roll] + " TA for " + courseName.cname + '(' + course + ')' + \
	      " for " + sem + " Semester. Please send your acceptance by sending a email to " + admin.ademail_id + ", and Please report to the concerned faculty and submit the TA Report form in Academic office.\r\n\n\nTA Chair\r\nIIIT Hyderabad."
	return string

#---------- FUNCTION FOR MAKING THE SUBJECT TO BE SENDED TO THE FACULTY AS NOTIFICATION FOR THE SELECTED TA'S ----------------------------
def MakeStringForFaculty(course, courseId, list):
	string = "Respected Faculty,\r\n\tPlease note that following applicants are selected as a TA :\r\n" + list + " for your course "\
	      + course + "(" + courseId + ").\r\n\nThank You\r\nTA Chair\r\nIIIT-Hyderabad"
	return string

#--------- FUNCTION FOR SENDING MAIL BY THE ADMIN TO THE FACULTY AND TA'S --------------------
def admin_send_mail():
   	msg=''
   	if ( session.login != 1) :
      		redirect(URL(r = request,f='index'))
      		return dict()

	courseId = request.args[0]
	course = db(db.Course.id == courseId).select()[0]
	courseId = db( (db.Course.id == courseId) & (db.Course.sem_id == db.Semester.id) & \
	      (db.Course.id == db.Teach.course_id) & (db.Faculty.id == db.Teach.faculty_id )).select()[0]
	applicantList = session.admin_applicantList
	listForFacultyText = '\r\n'
	for roll in applicantList:
		record = db(db.Applicant.aprollno == roll).select()[0]
		listForFacultyText += 'Name: ' + record.apname + '\r\nTA Type: ' + session.admin_rollType[roll] + '\r\nRoll No.: ' +\
		      str(record.aprollno) + '\r\nPhone No.: ' + str(record.phoneno) + '\r\nEmail-id: ' + record.apemail_id + '\r\n'
		sender = db(db.Admin.id > 0).select()[0]
		sender = sender.ademail_id
		reciever = record.apemail_id
	 	text = MakeStringForTA(course.cid, courseId.Semester.semname, roll)
		title =  'TA-Ship Selection for ' + courseId.Course.cname
		sendmail(sender, reciever, text, title)
	
	courseIdSame = db( (db.Course.id == courseId.Course.id) & (db.Course.sem_id == db.Semester.id) &\
	      (db.Course.id == db.Teach.course_id) & (db.Faculty.id == db.Teach.faculty_id )).select()
	for emailId in courseIdSame:
		reciever = emailId.Faculty.femail_id
		text = MakeStringForFaculty(courseId.Course.cname, courseId.Course.cid, listForFacultyText)
		title = 'List of Selected TA' + "'s" + ' for ' + courseId.Course.cname + '(' + courseId.Course.cid + ')'
		sendmail(sender, reciever, text, title)
	returnValue1 = sendmail(sender, sender, text, title)
	if returnValue1 == 1:
	   msg = 'Mail Sent successfully'
	else:
	   msg = 'Mail Sending failed'
	return dict(msg=msg)

def admin_allocatedTA():
   	if( session.login != 1):
	   redirect(URL(r = request, f = 'index'))
	   return dict()

   	records = db(db.Course.id > 0).select()
	return dict(records=records)

#----------- ALLOWS ADMIN TO UPLOAD A FILE WHICH CONTAINS THE COURSE INFO ----------------------------
# ---------- AN ALTERNATE FOR THE ADD COURSES QUERY --------------------------------------------------
import os
def upload():
   	if( session.login != 1):
	   redirect(URL(r = request, f = 'index'))
	   return dict()

	form = crud.create(db.Upload)
	if form.accepts(request.vars, session):
		response.flash = 'file uploaded'
		r = db(db.Upload.id > 0).select()
		for i in r:
			filename = os.path.join(request.folder, 'uploads', i.file)
			f = open(filename)
			for lines in f.readlines():				   	
			   if len(lines) < 20:
			      break
			   lines = lines.strip('\n')
			   list = lines.split(',')
			   if( not( db(db.Course.cid == list[1].strip(' ')).select() ) ):
			      getCid = db.Course.insert(cname = list[0].strip(' '), cid = list[1].strip(' '),\
				    cdts = list[2].strip(' '), no_of_qta = 0, no_of_hta = 0, no_of_fta = 0, \
				    hours_per_week = 5, sem_id = 1, coursetype = list[3].strip(' '))
			   else:
			      getCid = db(db.Course.cid == list[1].strip(' ')).select()[0].id
			   if( not( db(db.Faculty.femail_id == list[5].strip(' ')).select() ) ):
			      getPid = db.Faculty.insert(fname = list[4].strip(' '), femail_id = list[5].strip(' '))
			   else:
			      getPid = db(db.Faculty.femail_id == list[5].strip(' ')).select()[0].id
			   if( not(db((db.Teach.course_id == getCid) & (db.Teach.faculty_id == getPid)).select()) ):
			      db.Teach.insert(course_id = getCid, faculty_id = getPid)
			#break
	return dict(form=form)
		
#----------- Admin Related queries ends here ------------------


#-------- Faculty related queries -------------------------
#-------- ALLOWS FACULTY TO SEE THE APPLICANTS LIST FOR THE SELECTED COURSE ------------------------------
def faculty_applicant_list():
	if (session.login!=3) :
		redirect(URL(r = request, f = 'index'))
		return dict()

	session.faculty_flag = 0
	records = ''
	array = {'Overall CG':'apcgpa', 'Grade In That Course':'grade', 'Previous Experience':'prev_exp', 'Programme Of Study':'pname'}
	courseTaught = db((db.Faculty.femail_id == session.faculty_login_emailid) & (db.Teach.faculty_id == db.Faculty.id)\
	      & (db.Teach.course_id == db.Course.id)).select()
	form = form_factory(
			SQLField('course', label = "Select Course ", requires =\
			      IS_IN_DB(db((db.Faculty.femail_id == session.faculty_login_emailid)\
			      & (db.Teach.faculty_id == db.Faculty.id) & \
			      (db.Teach.course_id == db.Course.id)), 'Course.id', '%(cname)s ( %(cid)s )')),
			SQLField('pr1', label = "Priority 1", requires = IS_IN_SET(['Overall CG','Grade In That Course', \
			      'Previous Experience', 'Programme Of Study'])),
			SQLField('pr2', label = "Priority 2", requires = IS_IN_SET(['Overall CG','Grade In That Course',\
			      'Previous Experience', 'Programme Of Study'])),
			SQLField('pr3', label = "Priority 3", requires = IS_IN_SET(['Overall CG','Grade In That Course', \
			      'Previous Experience', 'Programme Of Study'])))

	if form.accepts(request.vars,session):
		var1 = array[request.vars.pr1]
		var2 = array[request.vars.pr2]
		var3 = array[request.vars.pr3]
		var = var1 + '|' + var2 + '|' + var3
		records = db((db.AppliedFor.cid == request.vars.course) & (db.Applicant.id == db.AppliedFor.appid) & \
		      (db.AppliedFor.cid==db.Course.id) & (db.Applicant.program_id == db.Program.id)).select(db.Applicant.apname, \
		      db.Applicant.aprollno, db.Applicant.apemail_id, db.Program.pname, db.AppliedFor.grade, db.Applicant.apcgpa, orderby=(var))
		session.faculty_flag = '1'
		# request.vars.course = Course.id  (id of the course selected by the faculty)
		redirect(URL(r = request, f = 'faculty_applicant_list_2', args = [request.vars.course,var1,var2,var3]))
	return dict(form=form, records=records)

def faculty_applicant_list_2():
	if (session.login != 3) :
		redirect(URL(r = request, f = 'index'))
		return dict()

	session.faculty_varCid = request.args[0]
	session.faculty_varPr1 = request.args[1]
	session.faculty_varPr2 = request.args[2]
	session.faculty_varPr3 = request.args[3]
	var = '~' + request.args[1] + ',~' + request.args[2] + ',~' + request.args[3]
	records = db((db.AppliedFor.cid == request.args[0]) & (db.Applicant.id == db.AppliedFor.appid) & \
	      (db.AppliedFor.cid == db.Course.id) & (db.Applicant.program_id == db.Program.id)).select(orderby = (var))
	return dict(records=records)

def faculty_applicant_list_3():
	if (session.login != 3):
		redirect(URL(r = request, f = 'index'))
		return dict()
	return dict()

#--------- RETURNS A STRING WHICH IS THE SUBJECT OF THE MAIL BELOW ------------------------------
def MakeStringForAdmin(courseName, courseId, list, sem):
	string="I nominate \n" + list + "for " + courseName + "(" + courseId +") for " + sem + "."
	return string

#------- ALLOWS FACULTY TO SEND MAIL TO THE ADMIN FOR THE NOMINATIONS FOR THEIR COURSE --------------------------
def faculty_send_mail():
	msg=''
	if (session.login != 3) :
		redirect(URL(r = request, f = 'index'))
		return dict()

	courseId = request.args[0]
	course = db(db.Course.id == courseId).select()[0]
	courseId = db( (db.Course.id == courseId) & (db.Course.sem_id == db.Semester.id) &\
	      (db.Course.id == db.Teach.course_id) & (db.Faculty.id == db.Teach.faculty_id )).select()[0]
	applicantList = session.faculty_applicantList
	listForAdminText = '\r\n'
	for roll in applicantList:
		record = db(db.Applicant.aprollno == roll).select()[0]
		listForAdminText += 'Name: '+ record.apname + '\r\nTA Type: ' + session.faculty_rollType[roll] + '\r\nRoll No.: ' + \
		      str(record.aprollno) + '\r\nPhone No.: ' + str(record.phoneno) + '\r\nEmailid: ' + record.apemail_id + '\r\n\r\n'
		sender = db(db.Admin.id > 0).select()[0]
		sender = sender.ademail_id
		reciever = record.apemail_id
	
	reciever = courseId.Faculty.femail_id
	text = MakeStringForAdmin(courseId.Course.cname, courseId.Course.cid, listForAdminText, courseId.Semester.semname)
	title = 'TA-Ship Nominations for ' + courseId.Course.cname + '(' + courseId.Course.cid + ')'
	returnValue1 = sendmail(reciever, sender, text, title)
	returnValue1 = 1
	if (returnValue1 == 1) :
	   msg = 'Mail Sent successfully'
	else:
	   msg = 'Mail Sending failed'
	sendmail(reciever, reciever, text, title)
	return dict(msg=msg)
	
#----------- ALLOWS FACULTY TO SEE THE TAS ALLOCATED IN THEIR COURSES --------------------------------------
def faculty_allocatedTA():
   	if( session.login != 3 ):
	   redirect(URL(r = request, f = 'index'))
	   return dict()

   	records = db((db.Faculty.id == db.Teach.faculty_id) & (db.Teach.course_id == db.Course.id) & \
	      (db.Faculty.femail_id == session.faculty_login_emailid)).select()
	return dict(records=records)

def faculty_selectedTA():
   	if(session.login != 3):
		redirect(URL(r = request, f = 'index'))
		return dict()

	records = db((db.Faculty.id == db.Teach.faculty_id) & (db.Teach.course_id == db.Course.id) & \
	      (db.SelectedTA.appid == db.Applicant.id) & (db.SelectedTA.cid == db.Course.id) & \
	      (db.Faculty.femail_id == session.faculty_login_emailid) & (db.AppliedFor.appid == db.Applicant.id) &\
	      (db.AppliedFor.cid == db.Course.id)).select(orderby = 'cname')
	return dict(records=records)



#################################################################################################
# Above This is done by rangers #
##################################################################################################
def index():
# Below two lines are added by the rangers

    session.login = 0
    session.LOGGEDIN = 0
    redirect(URL(r=request,f='login'))
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """

    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login 
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()
