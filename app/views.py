from flask import render_template, jsonify
from flask import request
from app.utils import web
from app.utils import pdf
from app.utils import text
from app.utils import search_text
from app import flask_app
import os

reports = web.get_links()


@flask_app.route("/", methods=["GET"])
def home():
    return choose_report()


@flask_app.route("/choose_report", methods=["GET"])
def choose_report():
    return render_template('choose.html', reports=reports)


@flask_app.route('/download', methods=['POST'])
def download_report():
    year = request.form.get('year')
    link = reports[year]
    web.download_pdf(link=link, year=year)
    txt_exists = os.path.exists(f'app/static/data/txt/CBR_report{year}.txt')
    norm_exists = os.path.exists(f'app/static/data/norm/CBR_report{year}_norm.txt')
    freq_exists = os.path.exists(f'app/static/images/freq{year}.png')
    plot_exists = os.path.exists(f'app/static/images/dict{year}.png')
    return render_template('document.html', year=year,
                           txt_exists=txt_exists,
                           norm_exists=norm_exists,
                           freq_exists=freq_exists,
                           plot_exists=plot_exists)


@flask_app.route('/convert', methods=['POST'])
def convert_to_txt():
    year = request.data.decode('utf8')
    pdf.get_txt(year)
    return jsonify({"success": True})


@flask_app.route('/normalize', methods=['POST'])
def normalize():
    year = request.data.decode('utf8')
    text.normalize(year)
    return jsonify({"success": True})


@flask_app.route('/draw_plot_dict', methods=['POST'])
def draw_plot_dict():
    year = request.data.decode('utf8')
    return text.plot_dict_size(year)


@flask_app.route('/draw_freq', methods=['POST'])
def draw_freq():
    year = request.data.decode('utf8')
    return text.plot_freq_table(year)


@flask_app.route('/search', methods=['POST'])
def search():
    req = request.get_json()
    pattern = req['query']
    year = req['year']
    metric = req['metric']
    n_pad_words = int(req['n_pad'])
    exact_search = req['exact_search']
    result = search_text.file_search(pattern, year, metric, n_pad_words, exact_search)
    success = result is not None
    return_json = {"success": success}
    if success:
        left = ' '.join(result.split()[:n_pad_words])
        return_json['left'] = left
        middle = ' '.join(result.split()[n_pad_words:-n_pad_words])
        return_json['middle'] = middle
        right = ' '.join(result.split()[-n_pad_words:])
        return_json['right'] = right

    return jsonify(return_json)
