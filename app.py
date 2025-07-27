from flask import(
    render_template,
    redirect,
    session,
    url_for,
    request,
    flash
)
from config import app,db
from models import User,Post
from datetime import datetime
from sqlalchemy import or_

@app.route("/register",methods = ["GET", "POST"])
def register():
    
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        # vérification de l'existence des données
        existing_user_email = User.query.filter_by(email= email).first()
        existing_user_username = User.query.filter_by(username= username).first()

        if existing_user_email:
            flash("L'adresse email existe déja","error")
            return redirect(url_for("register"))
        
        if existing_user_username:
            flash("Ce nom d'utilisateur est déja pris","error")
            return redirect(url_for('register'))
        
        #création d'un nouvel utilisteur
        new_user = User(username = username, email= email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        flash(f"Compte cré avec succès {new_user.username}! Vous pouvez désormais vous connecter", "success")
            
    return render_template("register.html")



@app.route("/",methods = ["GET","POST"])
def home():
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        stay_log_in = 'stay' in request.form
        
        user = User.query.filter_by(email = email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f"Bienvenue {user.username}","success")
            print(session)
            session.permanent = stay_log_in
            return redirect(url_for('about'))
        
        else:
            flash("Identifiants incorrects","error")
            return redirect(request.url)
        
    
    else:
        if 'user_id' in session:
           return redirect(url_for('about'))
       
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop("user_id",None)
    session.pop("username",None)
    flash("Déconnecté avec succès","success")
    return redirect(url_for('home'))


@app.route('/about/')
def about():
    if 'user_id' not in session:
       return redirect(url_for('home'))
  
    #user = User.query.get(session['user_id']) 
    user = db.session.get(User,session["user_id"])
    return render_template("about.html",posts = user.posts)


@app.route('/add_post',methods = ["GET", "POST"])
def add_post():
    
    if 'user_id' in session:
       
        if request.method == "GET":
            return render_template("add_post.html")
        else:
            title = request.form['title']
            content = request.form['content']
            user_id = session['user_id']
            new_post = Post(title=title, content = content, user_id = user_id)
            
            db.session.add(new_post)
            db.session.commit()
            
            flash("Nouveau post créé","success")
            return redirect(url_for('about'))
  
    return redirect(url_for('home'))

@app.route("/edit_post/<int:post_id>",methods = ["GET","POST"])
def edit_post(post_id):
    
    if 'user_id' in session:
        post = db.session.get(Post, post_id)
        #post = Post.query.get(post_id)
        
        if   post is None:
            flash("Ce poste n'exhiste pas","error")
            return redirect(url_for('about'))   
        
        elif post.user_id != session['user_id'] :
            flash("Vous n'avez pas droit à cette action","error")
            return redirect(url_for('about'))
        
      
        if request.method == "GET":
            return render_template('edit_post.html',post = post)
        
        else:
            post.title = request.form["title"]
            post.content = request.form['content']
            db.session.commit()
            flash("Modifications appliquées avec succès","success")
            return redirect(url_for('about'))


    return redirect(url_for("home"))

@app.route("/delete_post/<int:post_id>",methods = ["GET","POST"])
def delete_post(post_id):
    if request.method == "POST":
        if 'user_id' in session:
            #post = Post.query.get(post_id)
            post = db.session.get(Post,post_id)
            if post is None:
                flash("Ce post n'existe pas","error")
                return redirect(url_for('about'))
            
            elif post.user_id != session['user_id']:
                flash("Vous n'avez pas de droit sur ce fichier","error")
                return redirect(url_for('about'))
            
            db.session.delete(post)
            db.session.commit()
            
            flash("Post supprimé avec succès","success")
            return redirect(url_for('about'))
    
    return redirect(url_for('home'))


@app.route("/search",methods =["GET"])
def search():
    
    search_query = request.args.get("query", "").strip()
    posts = []
    
    if search_query:
        posts = Post.query.filter(
            or_(
            Post.title.ilike(f"%{search_query}%"),
            Post.content.ilike(f"%{search_query}%")
            )
            ).all()

    return render_template("search.html",posts=posts,query = search_query)


if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5000,debug=True)