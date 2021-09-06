from flask import Flask, request, redirect, url_for, send_from_directory
import os
from os import openpty

from pandas.core.indexing import convert_to_index_sliceable
import fitz
import re
import pandas as pd
from collections import namedtuple
import convertir


UPLOAD_FOLDER = os.path.abspath("./Archivos PDF/")
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/", methods = ["GET", "POST"])
def upload():
    if request.method == "POST":
        f= request.files["ourfile"]
        filename = f.filename
        if filename == "":
            return "No se ha seleccionado ningún archivo"
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        convertir.conversor()

        return redirect(url_for("get_file", filename = filename))

    return """
<form method = "POST" enctype="multipart/form-data">
<input type = "file" name="ourfile">
<input type = "submit" value = "UPLOAD">
</form>
    """

@app.route("/Archivos PDF/<filename>")
def get_file(filename):

    return send_from_directory(app.config["UPLOAD_FOLDER"], path=filename+".xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)