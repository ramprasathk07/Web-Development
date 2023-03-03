from flask import Blueprint,render_template,request,flash,jsonify,redirect,url_for
from flask_login import login_user,logout_user,current_user
from flask_login import login_required
from models import User,Posts,Comments,Like,Follow
from __init__ import db
from datetime import date,datetime
import json
from sqlalchemy import func, text

views = Blueprint('views', __name__)

@views.route('/create-com/<post_id>',methods=['POST'])
@login_required
def home1(post_id):
    com=request.form.get('text')
        
    
       
    if com:
        post=Posts.query.get_or_404(post_id)
        if post:
            comment=Comments(text=com,post_id=post_id,user_id=current_user.id)
            db.session.add(comment)
            db.session.commit()
            flash("comment added",category="success")
            return redirect(url_for('views.home12'))
        else:
            flash("post doesnot exist",category="error")
            return redirect(url_for('views.home12'))
    else:
        flash("no comment",category="error")
        return redirect(url_for('views.home'))

@views.route('/post',methods=['GET','POST'])
@login_required
def home12():
    posts=Posts.query.all()
    com=Comments.query.all()
    return render_template('post.html',posts=posts,comment=com,user=current_user)

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    posts=Posts.query.filter(Posts.by==current_user.username).all()
    u=current_user.id
    com=Comments.query.filter(Comments.post_id==u).all()
    return render_template('base.html',comments=com,posts=posts,user=current_user)

@views.route('add',methods=['GET','POST'])
@login_required
def add(): 
    if request.method=='POST':
        link=request.form.get('link')
        description=request.form.get('desc')
        title=request.form.get('title')
        
        data=Posts(link=link,title=title,desc=description,by=current_user.username,author=current_user.id)
        db.session.add(data)
        db.session.commit()
        flash("LIST added",category="success")
        return redirect(url_for('views.home'))
    return render_template("home.html",user=current_user)
    
@views.route('/search',methods=['POST'])
@login_required
def search():
    search=request.form.get('searched')
    if len(str(search))>1:
        posts=Posts.query.filter(Posts.by.like('%'+search+'%')).all()
        
        return render_template('search.html',posts=posts,searched=search,user=current_user)
        
    else:
        flash("no search",category="danger")
        return redirect(url_for('views.home'))

@views.route('/profile',methods=['GET','POST'])
@login_required
def pro():
    u=current_user.username
    posts=Posts.query.filter(Posts.by==u).all()
    x=Posts.query.filter(Posts.by==u).count()
    l=Follow.query.all()
    l1=[]
    l2=[]
    for i in l:
        l1.append(i.follower)
        l2.append(i.created_author)
    o=0
    for i in l2:
        if i==u:
            o+=1


    return render_template('profile.html',posts=posts,user=current_user,x=x,y=o)


@views.route('/<int:id>')
@login_required
def delete(id):
    user_to=Posts.query.get_or_404(id)
    if user_to.by != current_user.username:
        flash("not allowed",category="danger")
        return redirect(url_for('views.home'))
    else:
        try:
            db.session.delete(user_to)
            db.session.commit()
            flash("LIST deleted",category="success")
            return redirect(url_for('views.home'))
        except:
            flash("LIST not deleted",category="error")
            return redirect(url_for('views.home'))
    

@views.route('/profile/edit/<int:id>',methods=['GET','POST'])
@login_required
def more(id):
    id1=id
    post=Posts.query.get_or_404(id1) 
    if request.method=='POST':
        
        link=request.form.get('link')
        title=request.form.get('title')
        description=request.form.get('desc')
        if title:
            post.title=title
        elif link:
            post.link=link
        elif description:
            post.desc=description
                     
        db.session.commit()
        flash("LIST added",category="success")
        return redirect(url_for('views.home'))
    return render_template("more.html",user=current_user,post=post)
    
@views.route('/pro1/<int:id>',methods=['GET'])
@login_required
def pro1(id):
    id1=id
    user_to=Posts.query.get(id1)
    if user_to:
        u=user_to.by
        post=Posts.query.filter(Posts.by==u).all()
        x=Posts.query.filter(Posts.by==u).count()
        # print(x)
        l=Follow.query.all()
        l1=[]
        l2=[]
        for i in l:
            l1.append(i.follower)
            l2.append(i.created_author)
        o=0
        for i in l2:
            if i==u:
                o+=1
        
        return render_template('profile1.html',posts=post,user=user_to,x=x,y=o,l1=l1,l2=l2)
    else:
        flash("no Posts availabe",category="error")
        return redirect(url_for('views.home'))
    
@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comments.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.user_id and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home12'))



@views.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return redirect(url_for('views.home'))
    
@views.route("/follow/<id>", methods=['GET','POST'])
@login_required
def follow(id):
    l=Follow.query.all()
    l1=[]
    l2=[]
    print(l)
    for i in l:
        
        l1.append(i.follower)
        l2.append(i.created_author)

    
    print(l1)
    print(l2)
    post = Posts.query.filter_by(id=id).first()
    print(post.by)
    print(current_user.username )
    if ((current_user.username not in l1) or (post.by not in l2)):    
        data=Follow(created_author=post.by,author=post.author,post_id=id,follower=current_user.username)
        db.session.add(data)
        db.session.commit()
    s='views.pro1/'+str(id)
    return redirect(url_for('views.pro1',id=id,l1=l1,l2=l2))

@views.route("/unfollow/<id>", methods=['GET','POST'])
@login_required
def unfollow(id):
    c=current_user.username
    deli=Follow.query.filter_by(follower=c).first()
    # print(deli)
    db.session.delete(deli)
    db.session.commit()

    s='views.pro1/'+str(id)
    return redirect(url_for('views.pro1',id=id))