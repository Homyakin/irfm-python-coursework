from flask import render_template
from flask import request
from app.utils import web
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
