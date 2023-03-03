from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_user,logout_user,current_user
from flask_login import login_required
from .models import User,Note
from . import db
from datetime import date,datetime
import json
from sqlalchemy import func, text

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        id1=request.form.get('id')
        title1 = request.form.get('title')
        info = request.form.get('info')
        username= request.form.get('username')
        stat=request.form.get('status')
        deadl=request.form.get('deadline')
        date=request.form.get('date')
        if len(title1)<1:
            flash("title is too short",category="error")
        else:
            new_note=Note(id=id1,title=title1,content=info,user_id=current_user.id,user_name=username,status=stat,deadline=deadl)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added",category="success")
    notes=Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html",user=current_user)

@views.route('/add',methods=['GET','POST'])
@login_required
def add(): 
    if request.method=='POST':
        id1=request.form.get('id')
        title1 = request.form.get('title')
        info = request.form.get('info')
        username= request.form.get('username')
        stat=request.form.get('status')
        deadl=request.form.get('deadline')
        date=request.form.get('date')
        comm='NA'
        if len(title1)<1:
            flash("title is too short",category="error")
        else:
            new_note=Note(id=id1,title=title1,content=info,user_id=current_user.id,user_name=username,status=stat,deadline=deadl,com=comm)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added",category="success")
    return render_template("add.html",user=current_user)

@views.route('/about',methods=['GET','POST'])
@login_required
def about(): 
    return render_template("about.html",user=current_user)
    
@views.route('/summary',methods=['GET','POST'])
@login_required
def sum(): 
    com=0
    req=0
    rev=0
    inp=0
    cross=0
    notes=Note.query.filter_by(user=current_user).all()
    today=date.today()
    
    for l in notes:
        x=date(int(l.deadline[0:4]),int(l.deadline[5:7]),int(l.deadline[8:10]))
        
        if l.status=='completed':
            com+=1
            
        elif l.status=='request':
            req+=1
        elif l.status=='review':
            rev+=1
        else:
            inp+=1
        if x<today:
            cross=cross+1
        db.session.commit()
    data = {'Task' : 'Status', 'In Request' : req, 'In Progress' : inp, 'In Review' : rev, 'Completed' : com }
    return render_template("summary.html",user=current_user,comp=com,inp=inp,req=req,rev=rev,cross=cross,data=data)


@views.route('/<int:id>')
@login_required
def delete(id):
    user_to=Note.query.get_or_404(id)
    try:
        db.session.delete(user_to)
        db.session.commit()
        flash("LIST deleted",category="success")
        return render_template("home.html",user=current_user)
    except:
        flash("LIST not deleted",category="error")
        return render_template("home.html",user=current_user)

@views.route('/more/<int:id>',methods=['GET','POST'])
@login_required
def more(id):
    id1=id
    user_to=Note.query.get_or_404(id1) 
    if request.method=='POST':
        if len(request.form.get('comment'))>0:

            user_to.com=request.form.get('comment')
            user_to.date=datetime.now()
        if len(request.form.get('ip'))>0:
            user_to.title=request.form.get('ip')
            user_to.date=datetime.now()
    db.session.commit()
    return render_template("more.html",user=current_user,id=id1,date=date)




@views.route('/update/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    id1=id
    stats="request"
    user_to=Note.query.get_or_404(id1) 
    if user_to.status=="completed":
        stats="review"
    user_to.status=stats
    db.session.commit()
    
    return render_template("home.html",user=current_user)

@views.route('/update1/<int:id>',methods=['GET','POST'])
@login_required
def forw(id):
    id1=id
    
    user_to=Note.query.get_or_404(id1) 
    if user_to.status=="review":
        user_to.status="completed"
        
        user_to.timerem =datetime.today()
        now=datetime.now()
        user_to.time= now.strftime("%H:%M:%S")
        
        
    elif user_to.status=="request":
        user_to.status="in progress"
    elif user_to.status=="in progress":
        user_to.status="review"    
            
    db.session.commit()
    return render_template("home.html",user=current_user,t=user_to.timerem,time=user_to.time)


@views.route('/update2/<int:id>',methods=['GET','POST'])
@login_required
def back(id):
    id1=id
    user_to=Note.query.get_or_404(id1) 
    if user_to.status=="review":
        user_to.status="in progress"
    elif user_to.status=="in progress":
        user_to.status="request"
    elif user_to.status=="completed":
        user_to.status="review"    
                
    db.session.commit()
    return redirect("/")
