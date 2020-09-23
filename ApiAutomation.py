import json
import requests
import os
from database import DataBase as db
from pathlib import Path


class ApiAutomation:

    def __init__(self):
        self.absolutePath = Path('ApiAutomation.py')

    def getNewCampaigns(self):
        # campaignsFileName = 'campaigns.json'
        # urlApi = "https://marioguimaraes.com.br/automation/api/campaigns"
        urlApi = "http://localhost/laravel-tips/adminlte/api/campaigns"
        response = requests.get(url=urlApi)

        if response.status_code >= 200 and response.status_code <= 209:
            campaignsWeb = response.json()

            # if os.path.isfile(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName)):
            #     with open(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName), 'r') as json_file:
            #         campaignsLocal = json.load(json_file)

            #     for campaignWeb in campaignsWeb['campaigns']:
            #         for segmentationWeb in campaignWeb['segmentations']:
            #             for groupWeb in segmentationWeb['groups']:
            #                 groupWeb['numbers_group'] = []
            #                 groupWeb['new_numbers'] = []
            #                 groupWeb['numbers_left'] = []

            # else:
            for campaignWeb in campaignsWeb['campaigns']:
                if not db().existsCampaign(campaignWeb['id']):
                    db().campaignStore(campaignWeb['id'],
                                        campaignWeb['name'],
                                        campaignWeb['start'],
                                        campaignWeb['end'],
                                        campaignWeb['start_monitoring'],
                                        campaignWeb['stop_monitoring'],
                                        campaignWeb['description'])

                for segmentationWeb in campaignWeb['segmentations']:
                    if not db().existsSegmentation(segmentationWeb['id']):
                        db().segmentationStore(segmentationWeb['id'],
                                                segmentationWeb['campaigns_id'],
                                                segmentationWeb['name'],
                                                segmentationWeb['description'])

                    for groupWeb in segmentationWeb['groups']:
                        if not db().existsGroup(groupWeb['id']):
                            db().groupStore(groupWeb['id'],
                                            groupWeb['segmentations_id'],
                                            groupWeb['name'],
                                            groupWeb['full_image_path'],
                                            groupWeb['description'],
                                            groupWeb['edit_data'],
                                            groupWeb['send_message'],
                                            groupWeb['seats'],
                                            groupWeb['occuped_seats'],
                                            groupWeb['people_left'],
                                            groupWeb['url'])

                        for groupInitialMembersWeb in groupWeb['initial_members']:
                            if not db().existsGroupInitialMembers(groupInitialMembersWeb['id']):
                                db().groupInitialMembersStore(groupInitialMembersWeb['id'],
                                                                groupInitialMembersWeb['wa_groups_id'],
                                                                groupInitialMembersWeb['contact_name'],
                                                                groupInitialMembersWeb['administrator'])

            # campaignsLocal = campaignsWeb

            # # atualizar campaigns.json
            # with open(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName), 'w') as json_file:
            #     json.dump(campaignsLocal, json_file, indent=4)
        else:
            # Erros
            print('Status Code', response.status_code)
            print('Reason', response.reason)
            print('Texto', response.text)

    # Obtem os dados de uma campanha específica

    def getCampaign(self):
        campaignsFileName = 'campaigns.json'
        # urlApi = "https://marioguimaraes.com.br/automation/api/campaigns"
        urlApi = "http://localhost/laravel-tips/adminlte/api/campaigns"
        response = requests.get(url=urlApi)

        if response.status_code >= 200 and response.status_code <= 209:
            campaignsWeb = response.json()

            if os.path.isfile(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName)):
                with open(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName), 'r') as json_file:
                    campaignsLocal = json.load(json_file)

                for campaignWeb in campaignsWeb['campaigns']:
                    for segmentationWeb in campaignWeb['segmentations']:
                        for groupWeb in segmentationWeb['groups']:
                            groupWeb['numbers_group'] = []
                            groupWeb['new_numbers'] = []
                            groupWeb['numbers_left'] = []
            else:
                for campaignWeb in campaignsWeb['campaigns']:
                    for segmentationWeb in campaignWeb['segmentations']:
                        for groupWeb in segmentationWeb['groups']:
                            groupWeb['numbers_group'] = []
                            groupWeb['new_numbers'] = []
                            groupWeb['numbers_left'] = []
                campaignsLocal = campaignsWeb

            # atualizar campaigns.json
            with open(os.path.join(os.path.dirname(__file__), 'data', campaignsFileName), 'w') as json_file:
                json.dump(campaignsLocal, json_file, indent=4)
        else:
            # Erros
            print('Status Code', response.status_code)
            print('Reason', response.reason)
            print('Texto', response.text)

    def updateGroup(self):
        # url = "https://marioguimaraes.com.br/automation/api/wagroups/1"
        urlApi = "http://localhost/laravel-tips/adminlte/public/api/wagroups/{}"

        with open(os.path.join(os.path.dirname(__file__), 'data', 'groups.json'), 'r') as json_file:
            self.groups = json.load(json_file)
        for grp in self.groups:
            group_data = {
                "occuped_seats": grp['occuped_seats']
            }
            url = urlApi.format(grp['id'])
            response = requests.put(url=url, json=group_data)

            if response.status_code >= 200 and response.status_code <= 209:
                # Sucesso
                print('Status Code', response.status_code)
                print('Reason', response.reason)
                print('Texto', response.text)
                print('JSON', response.json())
            else:
                # Erros
                print('Status Code', response.status_code)
                print('Reason', response.reason)
                print('Texto', response.text)


ApiAutomation().getNewCampaigns()
