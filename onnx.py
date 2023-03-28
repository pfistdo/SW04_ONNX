import onnxruntime
import numpy as np
from nltk import word_tokenize

ort_session = onnxruntime.InferenceSession("bidaf.onnx")

def preprocess(text):
   tokens = word_tokenize(text)
   # split into lower-case word tokens, in numpy array with shape of (seq, 1)
   words = np.asarray([w.lower() for w in tokens]).reshape(-1, 1)
   # split words into chars, in numpy array with shape of (seq, 1, 1, 16)
   chars = [[c for c in t][:16] for t in tokens]
   chars = [cs+['']*(16-len(cs)) for cs in chars]
   chars = np.asarray(chars).reshape(-1, 1, 1, 16)
   return words, chars

# input
context = 'A quick brown fox jumps over the lazy dog.'
query = 'What color is the fox?'
cw, cc = preprocess(context)
qw, qc = preprocess(query)

# run onnx bidaf model
results = ort_session.run(None, {'context_word': cw, 'context_char': cc, 'query_word': qw, 'query_char': qc})

# assuming answer contains the np arrays for start_pos/end_pos
start = np.ndarray.item(results[0])
end = np.ndarray.item(results[1])
print([w.encode() for w in cw[start:end+1].reshape(-1)])
print(cw[start:end+1].reshape(-1))

# @author: https://github.com/onnx/models/tree/main/text/machine_comprehension/bidirectional_attention_flow