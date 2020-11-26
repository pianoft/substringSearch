import subprocess


def run(commands):
    subprocess.run([commands], shell=True)
    return


run('pip3 install pipenv;pip3 install bs4 flask flask_sqlalchemy sqlalchemy_imageattach numpy;cd application;python3 server.py')

run('pipenv shell')
