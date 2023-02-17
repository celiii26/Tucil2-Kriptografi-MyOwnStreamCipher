# gui web dengan Flask untuk my own stream cipher
from flask import *
from utils import *
import os
import streamCipher
from pathlib import Path

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        action = request.form.get('action')
        input = request.form.get('input')
        output = request.form.get('output')
        text = request.form['text']
        key = request.form['key']

        if action == "Encrypt" and input == "string":
            hasil = streamCipher.enkrip(text, key)
            if output == "hex":
                return '<h3>Hasil encrypt : %s</h3>' % hasil
            elif output == "base64":
                return '<h3>Hasil encrypt : %s</h3>' % streamCipher.hex_to_base64(hasil)
            else:
                return redirect(request.url)
        elif action == "Decrypt" and input == "hex":
            hasil = streamCipher.dekrip(text, key)
            if output == "string":
                return '<h3>Hasil decrypt : %s</h3>' % hasil
            elif output == "base64":
                return '<h3>Hasil decrypt : %s</h3>' % streamCipher.str_to_base64(hasil)
            else:
                return '<h3>Hasil decrypt : %s</h3>' % streamCipher.str_to_hex(hasil)
        elif action == "Decrypt" and input == "base64":
            text = streamCipher.base64_to_hex(text)
            hasil = streamCipher.dekrip(text, key)
            if output == "string":
                return '<h3>Hasil decrypt : %s</h3>' % hasil
            elif output == "base64":
                return '<h3>Hasil decrypt : %s</h3>' % streamCipher.str_to_base64(hasil)
            else:
                return '<h3>Hasil decrypt : %s</h3>' % streamCipher.str_to_hex(hasil)

    else:
        return '''
        <h1> My Own Stream Cipher </h1>
        <p> by Shely - 18220036 </p>
        <p><a href="/file">Enkripsi & Dekripsi dengan File</a></p>

        <p> Catatan : hasil enkripsi tidak bisa dalam bentuk string </p>

        <form action="" method = "POST">

        <label for="action">Choose action :</label>
        <select name="action" id="action">
        <option value="Encrypt">Encrypt</option>
        <option value="Decrypt">Decrypt</option>
        </select>

        <label for="input">Input format :</label>
        <select name="input" id="input">
        <option value="string">string</option>
        <option value="hex">hex</option>
        <option value="base64">base64</option>
        </select>

        <label for="output">Output format :</label>
        <select name="output" id="output">
        <option value="string">string</option>
        <option value="hex">hex</option>
        <option value="base64">base64</option>
        </select>

        <h4> Masukan Text </h4>
        <p><textarea name="text" rows="4" cols="50"></textarea></p>

        <h4> Masukan Key </h4>
        <p><textarea name="key" rows="4" cols="50"></textarea></p>
        <p><input type="submit" value="Submit"></p>

        </form>

        '''

@app.route('/file', methods=['GET', 'POST'])
def file():
    if request.method == 'POST':
        action = request.form.get('action')
        input = request.form.get('input')
        output = request.form.get('output')
        key = request.form['key']
        path = request.form['path']

        extension = Path(path).suffix
        #write_byte_file("enkrip%s" % extension, enkrip)
        #return ("enkrip%s" % extension)
    
        if action == "Encrypt" and input == "string":
            hasil = streamCipher.enkripFile(path, key)
            if output == "hex":
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            elif output == "base64":
                hasil = streamCipher.hex_to_base64(hasil)
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            else:
                return redirect(request.url)
        elif action == "Decrypt" and input == "hex":
            hasil = streamCipher.dekripFile(path, key)
            if output == "string":
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            elif output == "base64":
                hasil = streamCipher.str_to_base64(hasil)
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            else:
                hasil = streamCipher.str_to_hex(hasil)
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
        elif action == "Decrypt" and input == "base64":
            file = streamCipher.open_byte_file(path)
            text = file.decode("ISO-8859-1")
            text = streamCipher.base64_to_hex(text)
            hasil = streamCipher.dekrip(text, key)
            if output == "string":
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            elif output == "base64":
                hasil = streamCipher.str_to_base64(hasil)
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
            else:
                hasil = streamCipher.str_to_hex(hasil)
                streamCipher.write_byte_file("hasil%s" % extension, hasil)
        return redirect('/showfile/hasil%s' % extension)

    else:
        return '''
        <h1> My Own Stream Cipher </h1>
        <p> by Shely - 18220036 </p>
        <p><a href="/">Enkripsi & Dekripsi dengan input ketikkan</a></p>

        <p> Catatan : hasil enkripsi tidak bisa dalam bentuk string </p>

        <form action="" method = "POST">

        <label for="action">Choose action :</label>
        <select name="action" id="action">
        <option value="Encrypt">Encrypt</option>
        <option value="Decrypt">Decrypt</option>
        </select>

        <label for="input">Input format :</label>
        <select name="input" id="input">
        <option value="string">string</option>
        <option value="hex">hex</option>
        <option value="base64">base64</option>
        </select>

        <label for="output">Output format :</label>
        <select name="output" id="output">
        <option value="string">string</option>
        <option value="hex">hex</option>
        <option value="base64">base64</option>
        </select>

        <h4> Masukan Path File </h4>
        <p><textarea name="path" rows="4" cols="50"></textarea></p>

        <h4> Masukan Key </h4>
        <p><textarea name="key" rows="4" cols="50"></textarea></p>
        <p><input type="submit" value="Submit"></p>

        </form>
        '''

# route untuk nge-direct download file yg udah di proses
@app.route('/showfile/<path:filename>')
def showfile(filename):
    uploads = os.path.join(current_app.root_path, "")
    return send_from_directory(directory=uploads, path=filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)