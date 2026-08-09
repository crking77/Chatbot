from models import Faq_User, User
from flask import render_template, request, redirect, url_for, jsonify, session
import bcrypt
from flask_login import  login_required, login_user
def register_routes(app,db):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(
                username = username
            ).first()
            if user and bcrypt.checkpw (password.encode("utf-8"), user.password.encode("utf-8")):
                login_user(user, remember=False)
                return redirect(
                    url_for("index")
                )
                session.permanent = True
            return "Sai tài khoản hoặc mật khẩu"
        return render_template("login.html")







    @app.route("/", methods =["GET"])
    @login_required
    def index():
        return render_template("index.html")
    @app.route("/add_faq", methods =["POST"])
    @login_required
    def add_faq():
        question = request.form.get("question")
        answer = request.form.get("answer")
        print(f"Received question: {question}, answer: {answer}")
        if not question or not answer:
            return jsonify({"error": "Question and answer are required"}), 400  
        else:
            from services.faq_service import add_faq as add_faq_service
            faq = add_faq_service(question, answer)
            print(faq.id)
            print(faq.ask)
            print(faq.answer)
            return render_template("index.html")
    @app.route("/view_faq", methods =["GET"])
    @login_required
    def view_faq():
        faqs = Faq_User.query.all()
        return render_template("listFaq.html", faqs=faqs)
    @app.route("/view_faq/delete/<int:id>", methods =["GET"])
    @login_required
    def delete(id):
        faq = db.session.get(Faq_User, id)
        if faq:
            db.session.delete(faq)
            db.session.commit()
            return redirect(url_for("view_faq"))
    @app.route("/view_faq/edit/<int:id>", methods =["GET", "POST"])
    @login_required
    def edit(id):
        faq = db.session.get(Faq_User, id)
        if faq is None:
            return jsonify({"error": "FAQ not found"}), 404
        if request.method == "POST":
            question = request.form.get("question")
            answer = request.form.get("answer")
            if not question or not answer:
                return jsonify({"error": "Question and answer are required"}), 400
            faq.ask = question
            faq.answer = answer
            db.session.commit()
            return redirect(url_for("view_faq"))
        return render_template("editFaq.html", faq=faq)
        
    @app.route("/embeddings", methods =["GET"])
    @login_required
    def embeddings():
        from services.embedding_service import embedding_faqs
        embedding_faqs()
        return render_template("embedding_success.html")
    @app.route("/test_embeddings_result", methods =["GET"])
    @login_required
    def test_embeddings_result():
        from services.embedding_service import query_embedding_result
        question = request.args.get("question")
        if not question:
            return jsonify({"error": "Question is required"}), 400
        response_text = query_embedding_result(question)
        return jsonify({"response": response_text}), 200    
    @app.route("/privacy")
    def privacy():
        return """
        <h1>Chính sách quyền riêng tư</h1>
        <p>Chatbot này chỉ dùng để trả lời tin nhắn cho Fanpage [tên page].
        Dữ liệu tin nhắn được xử lý để phản hồi tự động, không chia sẻ cho bên thứ ba.</p>
        """