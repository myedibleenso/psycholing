from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, send_from_directory, Response, Markup
from werkzeug import secure_filename
import os
import logging
import json
from app import app
from wordvectors import *
from forms import AZP2FAForm, CSVForm
from config import basedir
from wordvectors import WordVector, ScoredPair, w2v_collection

UPLOADS_DIR = os.path.join(basedir, app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Welcome')

@app.route('/azp2fa', methods = ['GET', 'POST'])
def azp2fa():
    form = AZP2FAForm()
    if request.method == 'POST' and form.validate():
            form = request.form

    return render_template('azp2fa.html',
                           title='azp2fa', form=form)

@app.route('/csv', methods =['POST'])
def csv():
    scored_rows = []
    for r in request.files["csv_file"]:
        row = r.strip().split(",")
        w1 = w2v_collection.retrieve_wordvector(row[0])
        w2 = w2v_collection.retrieve_wordvector(row[-1])
        scored_rows.append((w1.word, w2.word, str(w1.cosine_similarity(w2))))
    #flash("Generated {0} similarity scores for {1}".format(len(scored_rows), request.files["csv_file"]))
    scored_data = "\n".join(",".join(row) for row in scored_rows)
    #return render_template('csv.html',
    #                       title='word vector similarity', score_data)
    return Response(scored_data,
                       mimetype="csv/plain",
                       headers={"Content-Disposition":
                                    "attachment;filename={0}".format('w2v-scores.csv')})

@app.route('/<path:filename>')
def basic_template(filename):
    return render_template('{0}.html'.format(filename),
                            title=filename.title())

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.route('/resources/<path:filename>')
def serve_file(filename):
    return send_from_directory(directory=UPLOADS_DIR,
                               filename=filename)

@app.route('/downloads/<string:filename>')
def download_file(filename):
    app.logger.info("sending {0}".format(filename))
    return send_from_directory(directory=UPLOADS_DIR,
                               filename=filename, as_attachment=True)

@app.route('/notes/<string:filename>')
def notes(filename):
    return app.send_static_file("notes/{0}/".format(filename))

if __name__ == '__main__':
    app.debug = True
    app.run()
