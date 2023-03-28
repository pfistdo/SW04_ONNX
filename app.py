from flask import Flask, send_file, request
import onnxruntime
import numpy as np
from nltk import word_tokenize
import nltk
nltk.download('punkt')

app = Flask(__name__, static_folder="web", static_url_path="/")
app.config['UPLOAD_FOLDER'] = "web/uploads"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000 # 16MB

def preprocess(text):
    tokens = word_tokenize(text)
    # split into lower-case word tokens, in numpy array with shape of (seq, 1)
    words = np.asarray([w.lower() for w in tokens]).reshape(-1, 1)
    # split words into chars, in numpy array with shape of (seq, 1, 1, 16)
    chars = [[c for c in t][:16] for t in tokens]
    chars = [cs+['']*(16-len(cs)) for cs in chars]
    chars = np.asarray(chars).reshape(-1, 1, 1, 16)
    return words, chars

@app.route("/")
def index():
    return send_file("web/index.html")

@app.route("/model/question", methods=["POST"])
def answer_question():
    if request.method == 'POST':
        # get context from request
        context = request.form.get("context")
        query = request.form.get("query")

        ort_session = onnxruntime.InferenceSession("bidaf.onnx")

        # input
        cw, cc = preprocess(context)
        qw, qc = preprocess(query)

        # run onnx bidaf model
        results = ort_session.run(None, {'context_word': cw, 'context_char': cc, 'query_word': qw, 'query_char': qc})

        # assuming answer contains the np arrays for start_pos/end_pos
        start = np.ndarray.item(results[0])
        end = np.ndarray.item(results[1])
        return cw[start:end+1].reshape(-1)[0]

        # @author: https://github.com/onnx/models/tree/main/text/machine_comprehension/bidirectional_attention_flow
  
if __name__ == "__main__":
    app.run()