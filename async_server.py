from flask import Flask as FlaskApp
from os import access as file_exists
from os import getcwd as get_current_dir
from os import F_OK as file_exists_param
from os.path import join as join_path
from os.path import isdir as is_dir
from flask import request as req
from flask_cors import CORS as cors_for_flask
from threading import Thread as NewThread
from time import sleep
from requests import get as req_get


PORT = 5000
DEBUG = False
HOST = '127.0.0.1'
folder = get_current_dir()


app = FlaskApp(__name__, static_folder=folder, template_folder=folder)
cors_for_flask(app)
app.use_reloader = False
can_shutdown = False


def render(filename):
    temp_file = open(filename, 'r')
    read = temp_file.read()
    temp_file.close()
    return read


def error404():
    error_404_path = join_path(folder, '404')
    if file_exists(error_404_path + '.html', file_exists_param):
        return render(join_path(folder, '404.html')), 404
    elif file_exists(error_404_path + '.htm', file_exists_param):
        return render(join_path(folder, '404.htm')), 404
    else:
        return 'Error404', 404


@app.route('/')
def main_index():
    index_path = join_path(folder, 'index')
    if file_exists(index_path + '.html', file_exists_param):
        return render(join_path(folder, 'index.html'))
    elif file_exists(index_path + '.htm', file_exists_param):
        return render(join_path(folder, 'index.htm'))
    else:
        return error404()


@app.route('/<path:url>')
def main(url):
    if is_dir(join_path(folder, url)):
        index_path = join_path(folder, url, 'index')
        if file_exists(index_path + '.html', file_exists_param):
            print(join_path(folder, url, 'index.html'))
            return render(join_path(folder, url, 'index.html'))
        elif file_exists(index_path + '.htm', file_exists_param):
            return render(join_path(folder, url, 'index.htm'))
        else:
            return error404()
    elif url[-5:] == '.html' or url[-4:] == '.htm':
        joined = join_path(folder, url)
        if file_exists(joined, file_exists_param):
            return render(joined)
        else:
            return error404()
    else:
        joined = join_path(folder, url)
        if file_exists(joined, file_exists_param):
            return app.send_static_file(url)
        else:
            return error404()


@app.route('/shutdown_this_fucking_server')
def shutdown_this_fucking_server():
    if can_shutdown:
        func = req.environ.get('werkzeug.server.shutdown')
        if func:
            func()
            return 'True'
        else:
            return 'False'
    else:
        return 'False'


def shutdown():
    global can_shutdown
    can_shutdown = True
    req_get(f'http://{HOST}:{PORT}/shutdown_this_fucking_server')


def run_app():
    app.run(HOST, port=PORT, debug=DEBUG)


if __name__ == '__main__':
    NewThread(target=run_app).start()
    sleep(5)
    print('shutdown')
    shutdown()
