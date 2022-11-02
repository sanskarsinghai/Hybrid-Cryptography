from flask import Flask, render_template, request, redirect,flash,session, send_file
from flask_sqlalchemy import SQLAlchemy
import hashlib

#import for encryption
import textfiletobinaryfile as tfb
import breakintothreeparts as b3t
import enc
import mergeenc as mge

#import for decryption
import divideenc as de
import desc
import merge as m
import os

#for file upload and download
from werkzeug.utils import secure_filename
from glob import glob
from io import BytesIO
from zipfile import ZipFile

#for data in logs
from datetime import datetime
import pytz
import math

#fro key regeneration
from arc4 import ARC4
from stegano import lsb

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

# em=""
# pa=""

class registration(db.Model):
    fname=db.Column(db.String(20), nullable=False)
    lname=db.Column(db.String(20), nullable=False)
    gender=db.Column(db.String(7), nullable=False)
    phone=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(50), primary_key=True)
    dob=db.Column(db.String(10),nullable=False)
    role=db.Column(db.String(10),nullable=False)
    status=db.Column(db.String(10),nullable=False)
    password=db.Column(db.String(20), nullable=False)
    
class LogT(db.Model):
    ObjectId = db.Column(db.String(150), primary_key=True)
    file_id  = db.Column(db.String(150), nullable=False)
    file_name = db.Column(db.String(150), nullable=False)
    operation = db.Column(db.String(20),nullable=False)
    date_time = db.Column(db.String(50),nullable=False)
    owner_no=db.Column(db.String(150),nullable=False)
    user_no=db.Column(db.Integer,nullable=False)

class documentT(db.Model):
    Uniqueid = db.Column(db.String(150),primary_key=True)
    doc_name = db.Column(db.String(150), nullable=False)
    ownerid = db.Column(db.String(150),nullable=False)
    recepientid = db.Column(db.String(150),nullable=False)
    Key_Regeneration_Token = db.Column(db.String(150),nullable=False)
    key=db.Column(db.String(200), nullable=False)

class contact(db.Model):
    file_id = db.Column(db.String(150),primary_key=True)
    request_id = db.Column(db.String(150),nullable=False)
    Key_Regeneration_Token = db.Column(db.String(150),nullable=False)
    response_status=db.Column(db.String(150),nullable=False)


@app.route("/admin/login",methods=["GET","POST"])
def adminlogin():
    # global em,pa
    if 'un' in session:
        flash("You are already login","success")
        return render_template('admin/index.html')

    if request.method=="POST":
        username=request.form['email']
        password=request.form['password']
        
        if username=="" or password=="":
            flash("Please Enter Email or Password","warning")
            return redirect("/admin/login")
        
        if username=='Admin' and password=='Admin':
            session['un']='Admin'
            return redirect("/admin/home")
        else:
            return redirect("/admin/login")

    return render_template("admin/login.html")

@app.route("/admin/")
@app.route("/admin/home")
def adminhome():
    if 'un' in session:
        return render_template("/admin/index.html")
    else:
        return redirect("/admin/login")

@app.route("/admin/logout",methods=["GET","POST"])
def adminlogout():
    # global em,pa
    if 'un' in session:
        session.pop('un')
        flash("Admin successfully logout","success")
        return redirect('/admin/login')

@app.route("/admin/usermanagement")
def users():
    if 'un' in session:
        allfeed=registration.query.filter_by(role='User').all()
        return render_template("admin/usermanagement.html",allfeed=allfeed)
    else:
        return redirect("/admin/")

@app.route("/admin/userprofile/<string:email>")
def pro(email):
    if 'un' in session:
        r=registration.query.filter_by(email=email).first()
        f=documentT.query.filter_by(ownerid=r.phone).all()
        c=contact.query.filter_by(request_id=r.phone).all()
        return render_template("admin/userall.html",lo=r,allfeed=f,c=c)

@app.route("/admin/status/<string:email>")
def status(email):
    if 'un' in session:
        s=registration.query.filter_by(email=email).first()
        if s.status=="Unblocked":
            s.status="Blocked"
        else:
            s.status="Unblocked"
        a=s.status
        db.session.add(s)
        db.session.commit()
        flash(email+" is "+a+" successfully","success")
        return redirect("/admin/usermanagement")

@app.route("/admin/keymanagement")
def keys():
    if 'un' in session:
        allfeed=documentT.query.filter_by().order_by(documentT.Uniqueid.desc()).all()
        return render_template("admin/keymanagement.html",allfeed=allfeed)
    else:
        return redirect("/admin/")

@app.route("/admin/requests")
def usersRequests():
    if 'un' in session:
        allfeed=contact.query.filter_by(response_status="Under Process").order_by(contact.request_id.desc()).all()
        return render_template("admin/RequestKey.html",allfeed=allfeed)
    else:
        return redirect("/admin/login")

@app.route("/admin/responserequest/<string:file_id>")
def responserequest(file_id):
    # if em !="" and pa !="":   
    if 'un' in session:
        c=contact.query.filter_by(file_id=file_id).first()
        
        f=documentT.query.filter_by(Uniqueid=file_id).first()

        if f is None:
            flash("Invalid file id","success")
            c.response_status="Invalid file id"

        elif f.ownerid!=c.request_id:
            flash("You are not authorized to get key","success")
            c.response_status="You are not authorized to get key"

        elif f.Key_Regeneration_Token!=c.Key_Regeneration_Token:
            flash("Invalid Key Regeneration Token","success")
            c.response_status="Invalid Key Regeneration Token"
        
        else:
            c.response_status="Approved"
            flash(file_id+" response is send successfully","success")

        db.session.add(c)
        db.session.commit()
        return redirect("/admin/requests")
    else:
        return redirect("/admin/login")  
        
@app.route("/login",methods=["GET","POST"])
def login():
    # global em,pa
    msg=None
    if 'email' in session:
        flash("You are already login","warning")
        return render_template('home/index.html')

    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        
        if email=="" or password=="":
            msg="Please Enter Email or Password"
            return render_template("login.html",msg=msg)
            
        
        p = hashlib.md5(password.encode())

        lo=registration.query.filter_by(email=email).first()

        if lo is None:
            msg="You may have not signed up!!"
        elif lo.status=="Blocked":
                msg=lo.email+" is blocked by our admin!!"
        elif lo.password!=p.hexdigest():
            msg="Invalid Password entered"
        else:
            session['email']=lo.email
            session['role']=lo.role
            session['phone']=lo.phone
            flash(lo.fname+"  logged in Successfully","success")
            return redirect("/home")
            
    return render_template("accounts/login.html",msg=msg)

@app.route("/signup",methods=["GET","POST"])
def signup():
    msg=""
    if 'email' in session:
        flash("You are already login","warning")
        return render_template('home/index.html')

    if request.method=="POST":
        fname=request.form['fname']
        lname=request.form['lname']
        gender=request.form['gender']
        phone=request.form['phone']
        email=request.form['email']
        dob=request.form['dob']
        password=request.form['password']
        conpassword=request.form['conpassword']

        e=registration.query.filter_by(email=email).first()
        p=registration.query.filter_by(phone=phone).first()
        if e is not None or p is not None :
            msg="Email or Phone number already register"
        elif password!=conpassword:
            msg="Password and Confirm password are not matched"

        elif len(phone)!=10:
            msg="Invalid phone number"

        else:
            p = hashlib.md5(password.encode())
            log=registration(fname=fname,lname=lname,gender=gender,phone=phone,email=email,dob=dob,password=p.hexdigest(),role="User",status="Unblocked")
            db.session.add(log)
            db.session.commit()
            flash(fname+"  register Successfully","success")
            return redirect("/login")
        
    return render_template("accounts/register.html",msg=msg)

@app.route("/logout")
def logout():
    if 'email' in session:
      session.pop('email')
      flash("Logout Successfully","success")
      return redirect("/login")

@app.route("/profile")
def profile():
    if 'email' in session:
        lo=registration.query.filter_by(email=session['email']).first()
        flash("If you change your profile data then this may effect the process of decryption of previously encrypted documents","danger")
        return render_template("home/profile.html",lo=lo,msg="no")
    else:
        return redirect("/")

@app.route("/passwrodupdatepage")
def passwrodupdatepage():
    if 'email' in session:
        lo=registration.query.filter_by(email=session['email']).first()
        flash("If you change your profile data then this may effect the process of decryption of previously encrypted documents","danger")
        return render_template("home/profile.html",lo=lo,msg="yes")
    else:
        return redirect("/")

@app.route("/profileupdate",methods=["GET","POST"])
def profileupdate():
    if 'email' in session:
        if request.method=='POST':
            fname=request.form['fname']
            lname=request.form['lname']
            gender=request.form['gender']
            dob=request.form['dob']

            re=registration.query.filter_by(email=session['email']).first()
              
            re.fname=fname
            re.lname=lname
            re.gender=gender
            re.dob=dob

            db.session.add(re)
            db.session.commit()
            flash("Your profile is successfully updated","success")

            return redirect('/profile')

    else:
        redirect("/")

@app.route("/passwordupdate",methods=["GET","POST"])
def passwordupdate():
    if 'email' in session:
        if request.method=='POST':
            cpass=request.form['cpassword']
            npass=request.form['npassword']
            copass=request.form['copassword']

            re=registration.query.filter_by(email=session['email']).first()

            if cpass!="":
                c=hashlib.md5(cpass.encode())
                if c.hexdigest()!=re.password:
                    flash("Invalid Current Password","warning")
                    return redirect("/passwrodupdatepage")
                else:
                    if npass=="":
                        flash("New password is empty string","warning")
                        return redirect("/passwrodupdatepage")
                    
                    elif npass!=copass:
                        flash("New and Confirm password does not matched","warning")
                        return redirect("/passwrodupdatepage")
                    n=hashlib.md5(npass.encode())
            
                    re.password=n.hexdigest()            
                    db.session.add(re)
                    db.session.commit()
                    flash("Your password is successfully updated","success")

                    return redirect('/logout')
            
            return redirect('/profile')

    else:
        redirect("/")

@app.route("/")
@app.route("/home")
def home():
    # if em !="" and pa !="":
    if 'email' in session:
        return render_template("home/index.html")
    else:
        return redirect("/login")

ALLOWED_EXTENSIONS = {'txt'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

ALLOWED_EXTENSIONSD = {'bin'}
def allowed_fileD(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONSD

ALLOWED_EXTENSIONSIM = {'png','jpeg','jpg'}
def allowed_fileim(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONSIM

@app.route("/encryption",methods=["GET","POST"])
def encryption():

    if 'email' in session:
        if request.method=="POST":

            if 'edoc' not in request.files:
                flash("No file attached in request","warning")
                return redirect(request.url)
       
            file = request.files['edoc']
            file2=request.files['simg']
            if file.filename == '' or file2.filename=='':
                flash("No file selected","warning")
                return redirect(request.url)
            ed=""
            ei=""

            if (file and allowed_file(file.filename)):
                ed = secure_filename(file.filename)
            else:
                flash("Invalid Document format","warning")
                return redirect(request.url)
            
            if (file2 and allowed_fileim(file2.filename)):
                ei = secure_filename(file2.filename)
            else:
                flash("Invalid Image format","warning")
                return redirect(request.url)

            ba=os.getcwd()

            loc=ba+"/templates/UploadF/"
            
            file.save(os.path.join(loc, ed))
            file2.save(os.path.join(loc,ei))
            
            dn=request.form['denumber']

            dnu=dn.split(",")

            dnam=file.filename
            imna=file2.filename

            print("Encryption process started: -")
            print()
            
            lo=registration.query.filter_by(phone=session['phone']).first()    
            l=list()
            l.append(lo.fname)
            l.append(lo.lname)
            l.append(lo.email)
            l.append(lo.phone)
            l.append(lo.dob)
            l.append(lo.gender)

            tfb.TxtToBin(dnam)
            b3t.BreakIn3Parts()
            k=enc.keygen(l)
            iv=enc.aesenc()
            di=enc.desenc()
            r=enc.rc4enc()
            le=enc.decauth(lo.phone,dnu)
            
            ist = pytz.timezone('Asia/Kolkata')
            a=datetime.now(ist)  
            s=a.strftime("%d-%m-%Y %I-%M-%S %p") 


            r=enc.stegnoimg(k[0],iv,di,r,le,imna,s)

            mge.MergeIn1(s)

            print("Encryption process completed")

            ftk=open(ba+"/templates/encFile/"+s+".txt","w")
            ftk.write("This is the validation token password of regenerating the key if key is lost for doc "+s+".bin\n Please don't share this file or token password.\nYour password token is: -\n"+k[1])
            ftk.close()

            ks=""
            for i in l:
                if type(i)!=str:
                    ks+=str(i)
                else:
                    ks+=i
            ks=ks.encode('utf-8')

            arc4=ARC4(ks)
            cipher = arc4.encrypt(r.encode('utf-8'))

            rk=hashlib.md5(k[1].encode())

            ui=str(lo.phone)+"_"+s
            docdt=documentT(Uniqueid=ui,doc_name=file.filename,ownerid=lo.phone,recepientid=dn,key=cipher,Key_Regeneration_Token=rk.hexdigest())
            db.session.add(docdt)
            db.session.commit()

            lui=s+"_"+ui
            loD=LogT(ObjectId=lui,file_id=ui,file_name=file.filename,operation="Encryption",date_time=s,owner_no=lo.phone,user_no=lo.phone)
            db.session.add(loD)
            db.session.commit()

            loc=ba+"/templates/encFile/"
            stream = BytesIO()
        
            with ZipFile(stream, 'w') as zf:
                for file in glob(os.path.join(loc, s+".*")):
                  zf.write(file, os.path.basename(file))
                  
            stream.seek(0)

            os.remove("templates/UploadF/"+dnam)
            os.remove("templates/UploadF/"+imna)
            os.remove("templates/encFile/"+s+".bin")
            os.remove("templates/encFile/"+s+".png")
            os.remove("templates/encFile/"+s+".txt")

            return send_file(stream,as_attachment=True,attachment_filename=s+' EncryptionDocs.zip')

        return render_template("home/encryption.html")
    else:
        return redirect("/")
    
@app.route("/decryption",methods=["GET","POST"])
def decryption():

    if 'email' in session:
        if request.method=="POST":

            if 'edoc' not in request.files:
                flash("No file attached in request","warning")
                return redirect(request.url)
       
            file = request.files['edoc']
            file2=request.files['simg']
            if file.filename == '' or file2.filename=='':
                flash("No file selected","warning")
                return redirect(request.url)
            ed=""
            ei=""

            if (file and allowed_fileD(file.filename)):
                ed = secure_filename(file.filename)
            else:
                flash("Invalid Document format","warning")
                return redirect(request.url)
            
            if (file2 and allowed_fileim(file2.filename)):
                ei = secure_filename(file2.filename)
            else:
                flash("Invalid Image format","warning")
                return redirect(request.url)

            ba=os.getcwd()

            loc=ba+"/templates/uploadFDec/"
        
            file.save(os.path.join(loc, ed))
            file2.save(os.path.join(loc,ei))
           
            print("\nDecryption process started: -")
            print()

            fn=file.filename[:len(file.filename)-4]
            fn=fn.split(" ")
            fns=fn[0]+"_"+fn[1]+"_"+fn[2]

            fnm=file.filename[:len(file.filename)-4]
            fnm=fnm.split(" ")
            fnsm=fnm[0]+"_"+fnm[1]+"_"+fnm[2]

            l=de.stegnoimg(str(session['phone']),fnsm)

            if 0 in l:
                flash("You are not authorized to decrypt this file","warning")
                return redirect(request.url)

            de.DiviIn3(l,fns)

            ow=desc.stegnoimg(str(session['phone']),fnsm)

            if ow == "You are no authorized to decypt this file":
                flash("You are not authorized to decrypt this file","warning")
                return redirect(request.url)
    
            lo=registration.query.filter_by(phone=ow).first()    
            l=list()
            l.append(lo.fname)
            l.append(lo.lname)
            l.append(lo.email)
            l.append(lo.phone)
            l.append(lo.dob)
            l.append(lo.gender)

            desc.keygen(l)
            me=desc.aesdec()
            if me!="OK":
                flash(me,"warning")
                return redirect(request.url)
            
            me=desc.desdec()
            if me!="OK":
                flash(me,"warning")
                return redirect(request.url)
            
            me=desc.rc4dec()
            if me!="OK":
                flash("Invalid key for decryption","warning")
                return redirect(request.url)

            ist = pytz.timezone('Asia/Kolkata')
            a=datetime.now(ist)  
            s=a.strftime("%d-%m-%Y %I-%M-%S %p") 

            m.MergeIn3(s)

            print("Decryption process completed")
            print(ow+"_"+file.filename[:len(file.filename)-4])
            do=documentT.query.filter_by(Uniqueid=ow+"_"+file.filename[:len(file.filename)-4]).first()    
        
            lui=s+"_"+do.Uniqueid
            loD=LogT(ObjectId=lui,file_id=do.Uniqueid,file_name=file.filename,operation="Decryption",date_time=s,owner_no=do.ownerid,user_no=session['phone'])
            db.session.add(loD)
            db.session.commit()

            loc=ba+"/templates/decFile/"
           
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in glob(os.path.join(loc, s+'.txt')):
                  zf.write(file, os.path.basename(file))
            stream.seek(0)

            os.remove("templates/uploadFDec/"+fns+".bin")
            os.remove("templates/uploadFDec/"+fnsm+".png")
            os.remove("templates/decFile/"+s+".txt")

            return send_file(stream,as_attachment=True,attachment_filename=s+' DecrytpionDocs.zip')

        return render_template("home/decryption.html")
    else:
        return redirect("/")

@app.route("/AboutUs",methods=['GET','POST'])
def about():
    # if em !="" and pa !="":
    if 'email' in session:
        return render_template("home/about.html")
    else:
        return redirect("/")

@app.route("/logdetails")
def logdetails():
    if 'email' in session:
        c = LogT.query.filter(LogT.file_id.startswith(str(session['phone'])) | LogT.user_no.startswith(str(session['phone']))).order_by(LogT.date_time.desc()).all()
        last = math.ceil(len(c)/3)
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        c = c[(page-1)*3:(page-1)*3+ 3]
        
        if last==1:
            prev = "#"
            next = "#"
            flash("Your have only these logs","info")
        elif page==1:
            prev = "#"
            next = "/logdetails?page="+ str(page+1)
            flash("Your are on latest logs","info")
            
        elif page==last:
            prev = "/logdetails?page="+ str(page-1)
            next = "#"
            flash("Your are on oldest logs","info")
        else:
            prev = "/logdetails?page="+ str(page-1)
            next = "/logdetails?page="+ str(page+1)
        
        return render_template('home/logtable.html',allfeed=c, prev=prev, next=next)
    else:
        return redirect("/login")
    
@app.route("/docdetails")
def docdetails():
    if 'email' in session:
        c = documentT.query.filter(documentT.Uniqueid.startswith(str(session['phone']))).order_by(documentT.Uniqueid.desc()).all()
        last = math.ceil(len(c)/3)
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        c = c[(page-1)*3:(page-1)*3+ 3]
        
        if last==1:
            prev = "#"
            next = "#"
            flash("Your have only these docs","info")
        elif page==1:
            prev = "#"
            next = "/docdetails?page="+ str(page+1)
            flash("Your are on latest docs","info")
            
        elif page==last:
            prev = "/docdetails?page="+ str(page-1)
            next = "#"
            flash("Your are on oldest docs","info")
        else:
            prev = "/docdetails?page="+ str(page-1)
            next = "/docdetails?page="+ str(page+1)
        
        return render_template('home/doctable.html',allfeed=c, prev=prev, next=next)
    else:
        return redirect("/login")

@app.route("/decdocdetails")
def decdocdetails():
    if 'email' in session:
        c = documentT.query.filter(documentT.recepientid.startswith('%'+str(session['phone'])+'%') ).order_by(documentT.Uniqueid.desc()).all()
        last = math.ceil(len(c)/3)
        page = request.args.get('page')
        if (not str(page).isnumeric()):
            page = 1
        page = int(page)
        c = c[(page-1)*3:(page-1)*3+ 3]
        
        if last==1:
            prev = "#"
            next = "#"
            flash("Your have only these docs","info")
        elif page==1:
            prev = "#"
            next = "/docdetails?page="+ str(page+1)
            flash("Your are on latest docs","info")
            
        elif page==last:
            prev = "/docdetails?page="+ str(page-1)
            next = "#"
            flash("Your are on oldest docs","info")
        else:
            prev = "/docdetails?page="+ str(page-1)
            next = "/docdetails?page="+ str(page+1)
        
        return render_template('home/decdoctable.html',allfeed=c, prev=prev, next=next)
    else:
        return redirect("/login")

@app.route("/contactus",methods=['GET','POST'])
def contactus():
    if 'email' in session:
        if request.method=="POST":
            f=request.form
            
            ch=contact.query.filter_by(file_id=f['fileid']).first()
            if ch is not None:
                flash("Request already send","info")
                return redirect(request.url)

            rk=hashlib.md5(f['retk'].encode())

            c=contact(file_id=f['fileid'],request_id=session['phone'],Key_Regeneration_Token=rk.hexdigest(),response_status="Under Process")
            db.session.add(c)
            db.session.commit()

            flash("Your request is send successfully","success")
            return redirect(request.url)
        return render_template("home/contact.html")
    else:
        return redirect("/login")

@app.route("/requestsresponse")
def RequestsResponse():
    if 'email' in session:
        allfeed=contact.query.filter(contact.request_id.startswith(session['phone']),(contact.response_status.startswith("Approved"))).order_by(contact.request_id.desc()).all()
        noa=contact.query.filter(contact.response_status.startswith("You") | contact.response_status.startswith("Invalid")).order_by(contact.request_id.desc()).all()
        return render_template("home/RequestResponse.html",allfeed=allfeed,noa=noa)
    else:
        return redirect("/login")

@app.route("/regeneratekey/<string:file_id>")
def regeneratekey(file_id):
    # if em !="" and pa !="":   
    if 'email' in session:
        c=contact.query.filter_by(file_id=file_id).first()
        if c is None:
            flash("You may already download the file","warning")
            return redirect("/requestsresponse")

        f=documentT.query.filter_by(Uniqueid=file_id).first()
        
        lo=registration.query.filter_by(phone=session['phone']).first()    
        l=list()
        l.append(lo.fname)
        l.append(lo.lname)
        l.append(lo.email)
        l.append(lo.phone)
        l.append(lo.dob)
        l.append(lo.gender)
        
        ks=""
        for i in l:
            if type(i)!=str:
                ks+=str(i)
            else:
                ks+=i
        ks=ks.encode('utf-8')

        arc4=ARC4(ks)
        s=arc4.decrypt(f.key)
        c=s.decode('utf-8')
        
        ba=os.getcwd()
        lo=ba+"/templates/KeyReg/img.jpg"

        secret = lsb.hide(lo,c)
        im=f.Uniqueid[11:]
    
        loc=ba+"/templates/KeyRegC/"+im+".png"
        secret.save(loc)

        ist = pytz.timezone('Asia/Kolkata')
        a=datetime.now(ist)  
        s=a.strftime("%d-%m-%Y %I-%M-%S %p") 

        lui=s+"_"+f.Uniqueid
        loD=LogT(ObjectId=lui,file_id=f.Uniqueid,file_name=f.doc_name,operation="Key Regeneration",date_time=s,owner_no=f.ownerid,user_no=session['phone'])
        db.session.add(loD)
        db.session.commit()

        c=contact.query.filter_by(file_id=file_id).first()
        db.session.delete(c)
        db.session.commit()
           
        loc=ba+"/templates/KeyRegC/"
        stream = BytesIO()
        with ZipFile(stream, 'w') as zf:
            for file in glob(os.path.join(loc, im+'.png')):
              zf.write(file, os.path.basename(file))
        stream.seek(0)

        os.remove(loc+im+".png")
        
        return send_file(stream,as_attachment=True,attachment_filename=im+' RegeneratedKEy.zip')
    else:
        return redirect("/login")  
     
@app.route("/deleteresponse/<string:file_id>")
def deleteresponse(file_id):
    # if em !="" and pa !="":   
    if 'email' in session:
        c=contact.query.filter_by(file_id=file_id).first()

        f=documentT.query.filter_by(Uniqueid=file_id).first()
        
        ist = pytz.timezone('Asia/Kolkata')
        a=datetime.now(ist)  
        s=a.strftime("%d-%m-%Y %I-%M-%S %p") 

        lui=s+"_"+c.file_id
        loD=LogT(ObjectId=lui,file_id=c.file_id,file_name="None",operation=c.response_status,date_time=s,owner_no="None",user_no=session['phone'])
        db.session.add(loD)
        db.session.commit()

        db.session.delete(c)
        db.session.commit()
        return redirect("/requestsresponse")
    else:
        return redirect("/login")  
     

if __name__=="__main__":
    app.run(debug=True,port=8080)