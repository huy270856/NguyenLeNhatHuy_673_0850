from flask import Flask, render_template, request
import math

app = Flask(__name__)

# ==================== TRANSPOSITION CIPHER ====================
def transposition_encrypt(text, key):
    text = text.replace(" ", "")
    if key <= 1 or key >= len(text):
        key = max(2, min(key, len(text) - 1))
    
    num_rows = math.ceil(len(text) / key)
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    
    idx = 0
    for row in range(num_rows):
        for col in range(key):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    result = ''
    for col in range(key):
        for row in range(num_rows):
            result += grid[row][col]
    
    return result

def transposition_decrypt(text, key):
    if key <= 1 or key >= len(text):
        key = max(2, min(key, len(text) - 1))
    
    num_rows = math.ceil(len(text) / key)
    num_empty = (num_rows * key) - len(text)
    
    grid = [['' for _ in range(key)] for _ in range(num_rows)]
    
    idx = 0
    for col in range(key):
        for row in range(num_rows):
            if col == key - 1 and row >= num_rows - num_empty:
                continue
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1
    
    result = ''
    for row in range(num_rows):
        for col in range(key):
            result += grid[row][col]
    
    return result

# ==================== ECC (Elliptic Curve Cryptography) ====================
# Simple ECC implementation for demonstration
class SimpleECC:
    def __init__(self):
        # Using small prime for demonstration (secp256k1 uses much larger)
        self.p = 997  # Prime number
        self.a = 1    # Curve parameter
        self.b = 1    # Curve parameter
        self.G = (2, 3)  # Generator point
    
    def mod_inverse(self, a, m):
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        _, x, _ = extended_gcd(a % m, m)
        return (x % m + m) % m
    
    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2 and y1 != y2:
            return None
        
        if x1 == x2 and y1 == y2:
            # Point doubling
            lam = (3 * x1 * x1 + self.a) * self.mod_inverse(2 * y1, self.p) % self.p
        else:
            # Point addition
            lam = (y2 - y1) * self.mod_inverse(x2 - x1, self.p) % self.p
        
        x3 = (lam * lam - x1 - x2) % self.p
        y3 = (lam * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    def scalar_multiply(self, k, P):
        result = None
        current = P
        
        while k > 0:
            if k & 1:
                result = self.point_add(result, current)
            current = self.point_add(current, current)
            k >>= 1
        
        return result
    
    def encrypt(self, text, public_key):
        # Simple XOR-based encryption using ECC point
        encrypted = []
        for i, char in enumerate(text):
            ecc_value = (public_key[0] + public_key[1] + i) % 256
            encrypted_char = ord(char) ^ ecc_value
            encrypted.append(encrypted_char)
        
        return ','.join(map(str, encrypted))
    
    def decrypt(self, encrypted_text, public_key):
        # Decrypt using same ECC point
        numbers = list(map(int, encrypted_text.split(',')))
        decrypted = []
        
        for i, num in enumerate(numbers):
            ecc_value = (public_key[0] + public_key[1] + i) % 256
            decrypted_char = num ^ ecc_value
            decrypted.append(chr(decrypted_char))
        
        return ''.join(decrypted)

ecc = SimpleECC()

# ==================== ROUTES ====================
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/transposition")
def transposition():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt_route():
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
def transposition_decrypt_route():
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

# ==================== ECC ROUTES ====================
@app.route("/ecc")
def ecc_page():
    return render_template('ecc.html')

@app.route("/ecc/encrypt", methods=['POST'])
def ecc_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    
    # Generate public key using ECC scalar multiplication
    public_key = ecc.scalar_multiply(key, ecc.G)
    
    encrypted_text = ecc.encrypt(text, public_key)
    
    return f'''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h2>✅ ECC Encryption Result</h2>
            <p><strong>Original Text:</strong> {text}</p>
            <p><strong>Private Key:</strong> {key}</p>
            <p><strong>Public Key:</strong> {public_key}</p>
            <p style="background: #e7f3e7; padding: 15px; border-left: 4px solid #FF9800;">
                <strong>Encrypted Text:</strong> <span style="color: #d32f2f; font-size: 16px;">{encrypted_text}</span>
            </p>
            <br><a href="/ecc" style="color: #FF9800;">← Back to ECC</a> | 
            <a href="/" style="color: #4CAF50;">Home</a>
        </div>
    </body>
    </html>
    '''

@app.route("/ecc/decrypt", methods=['POST'])
def ecc_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    
    # Generate public key using ECC scalar multiplication
    public_key = ecc.scalar_multiply(key, ecc.G)
    
    decrypted_text = ecc.decrypt(text, public_key)
    
    return f'''
    <html>
    <body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px;">
            <h2>✅ ECC Decryption Result</h2>
            <p><strong>Cipher Text:</strong> {text}</p>
            <p><strong>Private Key:</strong> {key}</p>
            <p><strong>Public Key:</strong> {public_key}</p>
            <p style="background: #e7f3e7; padding: 15px; border-left: 4px solid #FF9800;">
                <strong>Decrypted Text:</strong> <span style="color: #d32f2f; font-size: 18px;">{decrypted_text}</span>
            </p>
            <br><a href="/ecc" style="color: #FF9800;">← Back to ECC</a> | 
            <a href="/" style="color: #4CAF50;">Home</a>
        </div>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)