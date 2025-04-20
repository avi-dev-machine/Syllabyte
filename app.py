from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from models import db, SearchHistory, User
from chains.notes_chain import generate_notes
from chains.formula_chain import generate_formulas
# from chains.mindmap_chain import generate_mindmap
from chains.flash_card_mindmap import generate_study_material
from chains.general_summary import general_summary
from chains.general_mindmap import get_general_mindmap
from auth import auth
import json
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///history.db"
db.init_app(app)
app.register_blueprint(auth)

with app.app_context():
    db.create_all()

@app.route("/")
def landing():
    """Landing page route - first page users see"""
    if "user_id" in session:
        return redirect("/home")
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route - accessible from landing page"""
    if "user_id" in session:
        return redirect("/home")
    # ...rest of your login logic...

@app.route("/home")
def home():
    """Home page after login"""
    if "user_id" not in session:
        return redirect("/login")
    return render_template("home.html")

@app.route("/try")
def try_page():
    """Try page requires authentication"""
    if "user_id" not in session:
        return redirect("/login")
    return render_template("try.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect("/login")

    notes = formulas = mindmap = ""
    if request.method == "POST":
        topic = request.form["topic"]
        notes = generate_notes(topic)
        formulas = generate_formulas(topic)
        mcqs = generate_mcqs(topic)
        mindmap, flashcards = generate_study_material(topic)

        # Store in database
        entry = SearchHistory(
            user_id=session["user_id"],
            topic=topic,
            notes=notes,
            formulas=formulas,
            mindmap=json.dumps(mindmap),
            mcq=json.dumps(mcqs)
        )
        db.session.add(entry)
        db.session.commit()

    history = SearchHistory.query.filter_by(user_id=session["user_id"]).order_by(SearchHistory.timestamp.desc()).all()
    return render_template("index.html", notes=notes, formulas=formulas, history=history)

@app.route("/get_history_content/<int:history_id>")
def get_history_content(history_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        entry = SearchHistory.query.get_or_404(history_id)
        if entry.user_id != session["user_id"]:
            return jsonify({"error": "Unauthorized"}), 401
        
        return jsonify({
            "id": entry.id,
            "topic": entry.topic,
            "notes": entry.notes,
            "formulas": entry.formulas,
            "timestamp": entry.timestamp.strftime('%Y-%m-%d %H:%M')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/generate_study_material", methods=["POST"])
def generate_study_material_route():
    topic=request.form.get("topic")
    if topic:
        try:
            mind_map,flashcards = generate_study_material(topic)
            # print(mind_map)
            # print(flashcards)
            for dic in mind_map:
                dic['content'] = dic['content'].replace('\\\\','\\')
                dic['content'] = dic['content'].replace('\\*','*')
            for dic in flashcards:
                dic['front'] = dic['front'].replace('\\\\','\\')
                dic['front'] = dic['front'].replace('\\*','*')
                dic['back'] = dic['back'].replace('\\\\','\\')
                dic['back'] = dic['back'].replace('\\*','*')
            
            return render_template('minmap.html', mind_map=mind_map, flashcards=flashcards, topic=topic)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', error="Try again after some time.")
    else:
        return render_template('index.html', error="Please provide a topic.")
    

from chains.mcq_chain import generate_mcqs  # Add this import

@app.route("/generate_mcq", methods=["POST"])
def generate_mcq():
    topic = request.form.get("topic")
    if topic:
        try:
            mcqs = generate_mcqs(topic)
            return jsonify(mcqs)
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Failed to generate questions"})
    return jsonify({"error": "No topic provided"})

@app.route("/mcq")
def mcq_page():
    topic = request.args.get('topic')
    if not topic:
        return redirect('/')
        
    try:
        mcqs = generate_mcqs(topic)
        if not mcqs or not isinstance(mcqs, list) or len(mcqs) == 0:
            raise Exception("Invalid MCQ format received")
        
        correct_answers = [q.get('correct', '') for q in mcqs]
        
        return render_template('mcq.html', 
                               topic=topic, 
                               questions=mcqs,
                               correct_answers=correct_answers)
    except Exception as e:
        print(f"Error in MCQ generation: {e}")
        flash("Failed to generate questions. Please try again.", "error")
        return redirect('/')
    

@app.route("/generate_general_mindmap", methods=["POST"])
def general_mindmap():
    topic=request.form.get("topic")
    if topic:
        try:
            mind_map= get_general_mindmap(topic)
            # print(mind_map)
            # print(flashcards)
            for dic in mind_map:
                dic['content'] = dic['content'].replace('\\\\','\\')
                dic['content'] = dic['content'].replace('\\*','*')
           
            
            return render_template('general_mindmap.html', mind_map=mind_map, topic=topic)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('home.html', error="Try again after some time.")
    else:
        return render_template('home.html', error="Please provide a topic.")
    

@app.route("/generate_general_summary", methods=["GET","POST"])
def generate_general_summary_route():
    topic = request.form.get("topic")
    if topic:
        try:
            summary = general_summary(topic)
            return render_template('general_summary.html', summary=summary, topic=topic)
        except Exception as e:
            print(f"Error: {e}")
            return render_template('home.html', error="Try again after some time.")
    else:
        return render_template('general_summary.html', error="Please provide a topic.")

    
    


import os
from werkzeug.utils import secure_filename
from utils.pdf_parser import DocumentParser

# Add these configurations to your app
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET'])
def upload_page():
    if "user_id" not in session:
        return redirect("/login")
    return render_template('upload.html')

@app.route('/upload_document', methods=['POST'])
def upload_document():
    if 'user_id' not in session:
        return redirect('/login')

    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('upload_page'))

    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('upload_page'))

    if file and allowed_file(file.filename):
        try:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Parse the document
            parser = DocumentParser()
            content = parser.parse_document(file_path)

            if content:
                # Generate study materials from the content
                # notes = generate_notes(content)
                # mindmap = get_general_mindmap(content)
                mindmap,flashcards = generate_study_material(content)

                # Save to history
                entry = SearchHistory(
                    user_id=session["user_id"],
                    # topic=filename,  # Using filename as topic
                    # notes=notes,
                    formulas="",
                    mindmap=json.dumps(mindmap)
                )
                # db.session.add(entry)
                # db.session.commit()

                # Clean up the uploaded file
                os.remove(file_path)

                # return render_template(
                #     'upload.html',
                #     notes=notes,
                #     mindmap=mindmap
                # )
                return render_template(
                    'minmap.html',
                    mind_map=mindmap,
                    flashcards=flashcards,
                    
                )

            else:
                flash('Failed to parse document', 'error')
                return redirect(url_for('upload_page'))

        except Exception as e:
            print(f"Error processing document: {e}")
            flash('Error processing document', 'error')
            return redirect(url_for('upload_page'))

    flash('Invalid file type', 'error')
    return redirect(url_for('upload_page'))
if __name__ == "__main__":
    app.run(debug=True, port=5000)