import os
import ast
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ==============================
# SMART AST TOKENIZER
# ==============================
def get_ast_tokens(content):
    try:
        tree = ast.parse(content)
        tokens = []

        for node in ast.walk(tree):

            node_type = type(node).__name__

            # --- Add semantic context ---
            if isinstance(node, ast.Name):
                tokens.append(f"{node_type}_ID")

            elif isinstance(node, ast.Constant):
                tokens.append(f"{node_type}_CONST")

            elif isinstance(node, ast.Call):
                tokens.append(f"{node_type}_CALL")

            elif isinstance(node, ast.FunctionDef):
                tokens.append(f"{node_type}_FUNC")

            elif isinstance(node, ast.ClassDef):
                tokens.append(f"{node_type}_CLASS")

            else:
                tokens.append(node_type)

        return tokens

    except:
        return []


# ==============================
# NGRAM GENERATOR
# ==============================
def get_ngrams(tokens, n=4):   # Increased to 4-gram
    if len(tokens) < n:
        return []

    return [" ".join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]


# ==============================
# DOCUMENT BUILDER
# ==============================
def code_to_document(code):
    tokens = get_ast_tokens(code)
    ngrams = get_ngrams(tokens, n=4)
    return " ".join(ngrams)


# ==============================
# TFIDF SIMILARITY
# ==============================
def calculate_similarity(code1, code2):

    doc1 = code_to_document(code1)
    doc2 = code_to_document(code2)

    if not doc1 or not doc2:
        return 0.0

    vectorizer = TfidfVectorizer(
        min_df=1,
        ngram_range=(1,2),
        sublinear_tf=True
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return sim * 100
    except:
        return 0.0


# ==============================
# ROUTES
# ==============================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():

    if 'files[]' not in request.files:
        return jsonify({"error": "No files found"}), 400

    files = request.files.getlist('files[]')
    saved_paths = []

    for file in files:
        if file.filename == '':
            continue

        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        saved_paths.append(path)

    results = []

    PLAGIARISM_THRESHOLD = 70 

    for i in range(len(saved_paths)):
        for j in range(i+1, len(saved_paths)):

            with open(saved_paths[i], 'r', encoding="utf-8") as f1, \
                 open(saved_paths[j], 'r', encoding="utf-8") as f2:

                score = calculate_similarity(f1.read(), f2.read())

                results.append({
                    "file1": os.path.basename(saved_paths[i]),
                    "file2": os.path.basename(saved_paths[j]),
                    "score": round(score, 2),
                    "plagiarism": bool(score >= PLAGIARISM_THRESHOLD)
                })

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True, port=5000)