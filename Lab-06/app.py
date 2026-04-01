from flask import Flask, render_template, request
import math

app = Flask(__name__)

# ==================== TRANSPOSITION CIPHER - FIXED ====================
def transposition_encrypt(text, key):
    # Remove spaces
    text = text.replace(" ", "")
    
    # Validate key
    if key <= 1 or key >= len(text):
        key = max(2, min(key, len(text) - 1))
    
    # Create grid - write text in rows
    num_rows = math.ceil(len(text) / key)
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    
    # Fill grid row by row
    idx = 0
    for row in range(num_rows):
        for col in range(key):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    # Read column by column
    result = ''
    for col in range(key):
        for row in range(num_rows):
            result += grid[row][col]
    
    return result

def transposition_decrypt(text, key):
    # Validate key
    if key <= 1 or key >= len(text):
        key = max(2, min(key, len(text) - 1))
    
    num_rows = math.ceil(len(text) / key)
    num_empty = (num_rows * key) - len(text)
    
    # Create grid
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    
    # Fill grid column by column (encrypted text was read by column)
    idx = 0
    for col in range(key):
        for row in range(num_rows):
            # Skip empty boxes in last column
            if col == key - 1 and row >= num_rows - num_empty:
                continue
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    # Read row by row
    result = ''
    for row in range(num_rows):
        for col in range(key):
            result += grid[row][col]
    
    return result

# ==================== ROUTES ====================
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    encrypted_text = transposition_encrypt(text, key)
    return f'''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h2>✅ Encryption Result</h2>
            <p><strong>Original Text:</strong> {text}</p>
            <p><strong>Key:</strong> {key}</p>
            <p style="background: #e7f3e7; padding: 15px; border-left: 4px solid #4CAF50;">
                <strong>Encrypted Text:</strong> <span style="color: #d32f2f; font-size: 18px;">{encrypted_text}</span>
            </p>
            <br><a href="/transposition" style="color: #2196F3;">← Back to Transposition</a> | 
            <a href="/" style="color: #4CAF50;">Home</a>
        </div>
    </body>
    </html>
    '''

@app.route("/transposition/decrypt", methods=['POST'])
def decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    decrypted_text = transposition_decrypt(text, key)
    return f'''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h2>✅ Decryption Result</h2>
            <p><strong>Cipher Text:</strong> {text}</p>
            <p><strong>Key:</strong> {key}</p>
            <p style="background: #e7f3e7; padding: 15px; border-left: 4px solid #4CAF50;">
                <strong>Decrypted Text:</strong> <span style="color: #d32f2f; font-size: 18px;">{decrypted_text}</span>
            </p>
            <br><a href="/transposition" style="color: #2196F3;">← Back to Transposition</a> | 
            <a href="/" style="color: #4CAF50;">Home</a>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)