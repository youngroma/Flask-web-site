import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from config import app, db, ALLOWED_EXTENSIONS
from models import Item


# Проверка допустимых файлов
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return 'No file part'
#         file = request.files['file']
#         if file.filename == '':
#             return 'No selected file'
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#             # Создание нового Item с загруженной фотографией
#             new_item = Item(title='Sample Title', price=100, photo=os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             db.session.add(new_item)
#             db.session.commit()
#
#             return redirect(url_for('uploaded_file', item_id=new_item.id))
#
#
#

#
# if __name__ == '__main__':
#     app.run(debug=True)
