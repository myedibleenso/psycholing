from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_file, send_from_directory, Response, Markup
from werkzeug import secure_filename
import os
import logging
import json
from markdown import markdown
from app import app
from wordvectors import *
from forms import PairwiseCSVForm, KNNCSVForm
from config import basedir
from wordvectors import WordVector, WordVectorCollection, ScoredPair, w2v_collection

UPLOADS_DIR = os.path.join(basedir, app.config['UPLOAD_FOLDER'])

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Welcome')

@app.route('/pairwise-comparison', methods =['POST'])
def pairwise_csv():
    fname = request.files["csv_file"].filename
    if fname.lower().endswith(".csv"):
        scored_rows = []
        for r in request.files["csv_file"]:
            # get the word pair in columns 1 & 2
            row = r.strip().split(",")
            # the query will use lowercased words
            w1 = row[0].lower()
            w2 = row[-1].lower()
            # query the db for the words
            wv1 = w2v_collection.retrieve_wordvector(w1)
            wv2 = w2v_collection.retrieve_wordvector(w2)
            # if either word was missing from the db,
            # a score cannot be calculated :(
            if not wv1 or not wv2:
                score = "UNKNOWN"
            else:
                score = str(wv1.cosine_similarity(wv2))
                scored_rows.append((w1, w2, score))
            print "cos({0}, {1}) = {2}".format(w1,w2,score)

        scored_data = "\n".join(",".join(list(row)) for row in scored_rows)
        outname = '{0}-{1}-scores.csv'.format(fname[:-4], 'w2v')
        return Response(scored_data,
                        mimetype="csv/plain",
                        headers={"Content-Disposition": "attachment;filename={0}".format(outname)})

    else:
        flash(Markup(markdown("#### No `.csv` file was found")))
        return render_template('pairwise-comparison-csv.html')

@app.route('/knn', methods =['POST'])
def knn_csv():
    K = WordVectorCollection.K
    fname = request.files["csv_file"].filename
    if fname.lower().endswith(".csv"):
        # create header
        header = ",".join(["WORD"] + ["NN{0},NN{0}_SIM".format(i) for i in range(1, K+1)])
        neighbor_rows = [header]
        for r in request.files["csv_file"]:
            # we should only have a single column
            row = r.strip().split(",")
            if len(row) != 1:
                flash(Markup(markdown("#### Not a single-column `.csv` file")))
                return render_template('knn-csv.html')
            # the query will use the lowercased word
            w = row[0].lower()
            # find the nearest K neighbors
            # TODO: rename this method
            neighbors = w2v_collection.compare_all(w)
            if neighbors:
                neighbors = "{0},{1}".format(w,",".join("{0},{1}".format(w,s) for (w,s) in neighbors))
                neighbor_rows.append(neighbors)
            else:
                #flash(Markup(markdown("#### `{0}` not found".format(w))), 'error')
                neighbor_rows.append(w)
        # return the scored file
        outname = '{0}-{1}-knn.csv'.format(fname[:-4], 'w2v')
        return Response("\n".join(neighbor_rows),
                        mimetype="csv/plain",
                        headers={"Content-Disposition": "attachment;filename={0}".format(outname)})

    else:
        flash(Markup(markdown("#### No `.csv` file was found")))
        return render_template('knn-csv.html')

@app.route('/<path:filename>')
def basic_template(filename):
    template = '{0}.html'.format(filename)
    #print "attempting to load {0}".format(template)
    return render_template(template)

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
