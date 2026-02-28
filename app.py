import os
import ast
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==============================
# SMART AST TOKENIZER (Fixed: DFS Traversal)
# ==============================
class ASTTokenExtractor(ast.NodeVisitor):
    """
    Traverses the AST in Depth-First Search (DFS) order.
    Guarantees tokens match the actual execution flow.
    """
    def __init__(self):
        self.tokens = []

    def generic_visit(self, node):
        node_type = type(node).__name__
        
        # Normalize identifiers to focus on structure
        if isinstance(node, ast.Name): 
            self.tokens.append(f"{node_type}_ID")
        elif isinstance(node, ast.Constant): 
            self.tokens.append(f"{node_type}_CONST")
        elif isinstance(node, ast.FunctionDef): 
            self.tokens.append(f"{node_type}_FUNC")
        elif isinstance(node, ast.Call): 
            self.tokens.append(f"{node_type}_CALL")
        elif isinstance(node, ast.ClassDef): 
            self.tokens.append(f"{node_type}_CLASS")
        else: 
            self.tokens.append(node_type)
            
        # Continue traversing down the tree to children nodes
        ast.NodeVisitor.generic_visit(self, node)

def get_ast_tokens(content):
    try:
        tree = ast.parse(content)
        extractor = ASTTokenExtractor()
        extractor.visit(tree)
        return extractor.tokens
    except SyntaxError:
        return []

# ==============================
# DOCUMENT BUILDER (Fixed: No more Double N-gramming)
# ==============================
def code_to_document(code):
    """
    Converts AST tokens into a flat, space-separated string.
    Leaves the sliding window math to Sklearn.
    """
    tokens = get_ast_tokens(code)
    return " ".join(tokens)

# ==============================
# MAIN ROUTE
# ==============================
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'submissions' not in request.files:
            return "No files uploaded", 400

        files = request.files.getlist('submissions')
        file_data = []

        # 1. Pre-process all files in the batch
        for file in files:
            if file.filename == '':
                continue
            
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            
            with open(path, 'r', encoding="utf-8", errors="ignore") as f:
                content = f.read()
                doc = code_to_document(content)
                if doc:
                    file_data.append({"name": filename, "doc": doc})

        if len(file_data) < 2:
            return render_template('index.html', file_count=len(file_data), results=[], error="At least 2 valid Python files are required.")

        # 2. Global Batch Vectorization
        documents = [f['doc'] for f in file_data]
        filenames = [f['name'] for f in file_data]

        # Fixed: TF-IDF now correctly handles the 4-gram sliding window
        vectorizer = TfidfVectorizer(ngram_range=(4, 4), sublinear_tf=True)
        
        try:
            tfidf_matrix = vectorizer.fit_transform(documents)
            sim_matrix = cosine_similarity(tfidf_matrix)

            results = []
            for i in range(len(filenames)):
                for j in range(i + 1, len(filenames)):
                    score = round(sim_matrix[i][j] * 100, 2)
                    
                    if score > 0:
                        results.append({
                            "file1": filenames[i],
                            "file2": filenames[j],
                            "score": score
                        })

            results.sort(key=lambda x: x['score'], reverse=True)
            return render_template('index.html', file_count=len(file_data), results=results)

        except ValueError:
            # Catch error if files are too small to generate a 4-gram
            return render_template('index.html', file_count=len(file_data), results=[], error="Files are too short for structural analysis.")
        except Exception as e:
            return f"Error during analysis: {str(e)}", 500

    return render_template('index.html', file_count=0, results=[])

if __name__ == '__main__':
    app.run(debug=True, port=5000)