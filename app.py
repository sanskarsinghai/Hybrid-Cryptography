from flask import Flask, render_template, request, redirect,flash,session, send_file
from flask_sqlalchemy import SQLAlchemy
import hashlib

#import for encryption
from CryptoCode import textfiletobinaryfile as tfb
from CryptoCode import breakintothreeparts as b3t
from CryptoCode import enc
from CryptoCode import mergeenc as mge

#import for decryption
from CryptoCode import divideenc as de
from CryptoCode import desc
from CryptoCode import merge as m
import os

#for file upload and download
from werkzeug.utils import secure_filename
from glob import glob
from io import BytesIO
from zipfile import ZipFile

#for data in logs
from datetime import datetime

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
            flash(lo.fname+"  log in Successfully","success")
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
        return render_template("home/profile.html",lo=lo)
    else:
        return redirect("/")

@app.route("/profileupdate",methods=["GET","POST"])
def profileupdate():
    if 'email' in session:
        if request.method=='POST':
            fname=request.form['fname']
            lname=request.form['lname']
            gender=request.form['gender']
            phone=request.form['phone']
            cpass=request.form['cpassword']
            npass=request.form['npassword']
            copass=request.form['copassword']

            re=registration.query.filter_by(email=session['email']).first()
            
            if cpass!="":
                c=hashlib.md5(cpass.encode())
                if c.hexdigest()!=re.password:
                    flash("Invalid Current Password","warning")
                    return redirect("/profile")
                else:
                    if npass=="":
                        flash("New password is empty string","warning")
                        return redirect("/profile")
                    
                    elif npass!=copass:
                        flash("New and Confirm password does not matched","warning")
                        return redirect("/profile")
                    n=hashlib.md5(npass.encode())
                    re.password=n.hexdigest()            
            re.fname=fname
            re.lname=lname
            re.gender=gender
            re.phone=phone

            db.session.add(re)
            db.session.commit()
            flash("Your profile is successfully updated","success")

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

            loc=ba+"\\CryptoCode\\UploadF\\"
            
            file.save(os.path.join(loc, ed))
            file2.save(os.path.join(loc,ei))
            
            dn=request.form['denumber']

            dnu=dn.split(",")

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

            tfb.TxtToBin(file.filename[:len(file.filename)-4])
            b3t.BreakIn3Parts()
            k=enc.keygen(l)
            iv=enc.aesenc()
            di=enc.desenc()
            r=enc.rc4enc()
            le=enc.decauth(lo.phone,dnu)
            enc.stegnoimg(k,iv,di,r,le)

            d=datetime.today()
            s=d.strftime("%d-%m-%Y %I-%M-%S %p")

            mge.MergeIn1(s)

            print("Encryption process completed")
            

            ui=str(lo.phone)+"_"+s
            docdt=documentT(Uniqueid=ui,doc_name=file.filename,ownerid=lo.phone,recepientid=dn)
            db.session.add(docdt)
            db.session.commit()

            lui=s+"_"+ui
            loD=LogT(ObjectId=lui,file_id=ui,file_name=file.filename,operation="Encryption",date_time=s,owner_no=lo.phone,user_no=lo.phone)
            db.session.add(loD)
            db.session.commit()

            loc=ba+"\\CryptoCode\\encFile\\"
           
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in glob(os.path.join(loc, '*.*')):
                  zf.write(file, os.path.basename(file))
            stream.seek(0)

            os.remove("CryptoCode\\UploadF\\data.txt")
            os.remove("CryptoCode\\UploadF\\sbushiv.jpg")
            os.remove("CryptoCode\\encFile\\"+s+".bin")
            os.remove("CryptoCode\\encFile\\s1.png")

            return send_file(stream,as_attachment=True,attachment_filename='EncryptionDocs.zip')

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

            loc=ba+"\\CryptoCode\\UploadFDec\\"
        
            file.save(os.path.join(loc, ed))
            file2.save(os.path.join(loc,ei))
           
            print("\nDecryption process started: -")
            print()

            l=de.stegnoimg(str(session['phone']))

            if 0 in l:
                flash("You are not authorized to decrypt this file","warning")
                return redirect(request.url)

            fn=file.filename[:len(file.filename)-4]
            fn=fn.split(" ")
            fns=fn[0]+"_"+fn[1]+"_"+fn[2]

            de.DiviIn3(l,fns)

            ow=desc.stegnoimg(str(session['phone']))

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

            m.MergeIn3()

            print("Decryption process completed")
            print(ow+"_"+file.filename[:len(file.filename)-4])
            do=documentT.query.filter_by(Uniqueid=ow+"_"+file.filename[:len(file.filename)-4]).first()    
            d=datetime.today()
            s=d.strftime("%d-%m-%Y %I-%M-%S %p")

            lui=s+"_"+do.Uniqueid
            loD=LogT(ObjectId=lui,file_id=do.Uniqueid,file_name=file.filename,operation="Decryption",date_time=s,owner_no=do.ownerid,user_no=session['phone'])
            db.session.add(loD)
            db.session.commit()

            loc=ba+"\\CryptoCode\\decFile\\"
           
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in glob(os.path.join(loc, '*.*')):
                  zf.write(file, os.path.basename(file))
            stream.seek(0)

            os.remove("CryptoCode\\uploadFDec\\"+fns+".bin")
            os.remove("CryptoCode\\uploadFDec\\s1.png")
            os.remove("CryptoCode\\decFile\\origin.txt")

            return send_file(stream,as_attachment=True,attachment_filename='DecrytpionDocs.zip')

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

if __name__=="__main__":
    app.run(debug=True,port=8080)