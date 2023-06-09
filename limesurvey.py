from citric import Client


class Limesurvey:

    def __init__(self, url, username, password):
        self.__url = url
        self.__username = username
        self.__password = password

        self.client = Client(
            url,
            username,
            password,
        )
    
    def get_survey_list(self):
        return [survey for survey in self.client.list_surveys()]
    
    def save_survey_xlsx(self, sid, path='.'):
        self.client.save_responses(survey_id=sid, file_format="xls", filename=f'{path}/{sid}.xlsx')