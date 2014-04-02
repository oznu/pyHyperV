import requests
from requests_ntlm import HttpNtlmAuth

class orchestrator(object):
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        
    def Execute(self, runbook_id, params):
        headers = {'Content-Type': 'application/atom+xml'}
        r = requests.post(self.host, data=self.Build(runbook_id, params), headers=headers, auth=HttpNtlmAuth(self.user,self.password))
        print r.text

    def Build(self, runbook_id, params):
        BASE = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
                 <entry xmlns:d="http://schemas.microsoft.com/ado/2007/08/dataservices" xmlns:m="http://schemas.microsoft.com/ado/2007/08/dataservices/metadata" xmlns="http://www.w3.org/2005/Atom">
                 <content type="application/xml">
                 <m:properties>
                 <d:RunbookId m:type="Edm.Guid">%s</d:RunbookId>
                 <d:Parameters>
                 <![CDATA[<Data>%s</Data>]]>
                 </d:Parameters>
                 </m:properties>
                 </content>
                 </entry>"""
        settings_array = []
        for setting_var in params:
            setting_val = '<Parameter><ID>{%s}</ID><Value>%s</Value></Parameter>' % (setting_var, params[setting_var])
            settings_array.append(setting_val)
        params = ('').join(settings_array)
        return BASE % (runbook_id, params)
