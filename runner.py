import os
from flask import Flask, jsonify
from flask_apscheduler import APScheduler
from sharepoint import SharePoint
from limesurvey import Limesurvey
from dotenv import dotenv_values
from datetime import datetime


app = Flask(__name__)
config = dotenv_values(".env")


scheduler = APScheduler(
    app=app
)
limesurvey = Limesurvey(
    url=config.get('LiMESURVEY_URL'),
    username=config.get('LiMESURVEY_USERNAME'),
    password=config.get('LiMESURVEY_PASSWORD'),
)
sharepoint = SharePoint(
    url=config.get('SHAREPOINT_URL'),
    username=config.get('SHAREPOINT_USERNAME'),
    password=config.get('SHAREPOINT_PASSWORD'),
    site=config.get('SHAREPOINT_SITE'),
    doc=config.get('SHAREPOINT_DOC'),
    dir=config.get('SHAREPOINT_DIR'),
)


@scheduler.task('interval', minutes=3)
def process_runner():
    dir = 'files'
    print('start')

    # 1
    path = os.path.join(os.path.dirname(__file__), dir)

    for filename in os.listdir(path):
        os.remove(path + '/' + filename)

    print('2')

    # 2
    surveys = limesurvey.get_survey_list()

    files = []
    for survey in surveys:
        limesurvey.save_survey_xlsx(survey['sid'], './files')
        files.append(f'{survey["sid"]}.xlsx')

    print('3')
    # 3
    now = datetime.now()

    for filename in os.listdir(path):
        name = f'{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_sid_{filename}'
        sharepoint.upload_file('./files', filename, 'Archive', name)

    print('4')
    # 4
    sharepoints_files = sharepoint.files_list('')
    for file in files:
        if file not in sharepoints_files:
            sharepoint.upload_file('./files', file, '', file)
        else:
            sharepoint.delete_file(file, '')
            sharepoint.upload_file('./files', file, '', file)

    print('done')



if __name__ == '__main__':
    scheduler.start()
    app.run('0.0.0.0', port=5000)
