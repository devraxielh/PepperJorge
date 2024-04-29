from flask import Flask, request, render_template
from ultralytics import YOLO
import shutil
import os
app = Flask(__name__)
@app.route('/')
def upload_form():
    return render_template('upload_form.html')
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No se seleccionó ningún archivo'
    image = request.files['image']
    if image.filename == '':
        return 'No se seleccionó ningún archivo'
    if image:
        image.save(os.path.join("static", image.filename))
        model = YOLO("yolov8m.pt")
        infer = YOLO('./weights/best.pt')
        Salida = infer.predict(os.path.join("static", image.filename),save=True)
        result = Salida[0].save_dir
        archivo_a_copiar = result+'/'+image.filename
        carpeta_destino = os.path.join("static")
        shutil.copy(archivo_a_copiar, carpeta_destino)
        return render_template('imagen.html', img=os.path.join("static", image.filename))

if __name__ == '__main__':
    app.run(debug=True)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER