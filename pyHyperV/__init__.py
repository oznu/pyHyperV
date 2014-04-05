import requests, xmltodict
from requests_ntlm import HttpNtlmAuth

class orchestrator(object):
    def __init__(self, host, user, password):
        self.host = host
        self.session = requests.session()
        self.session.auth = HttpNtlmAuth(user,password)

    def intParseOutput(self, r):
        output, output['result'] = {}, {}
        doc = xmltodict.parse(r.text)
        output['status'] = r.status_code
        if r.status_code == 400: output['result']['message'] = doc['error']['message']['#text']
        if r.status_code == 401: output['result']['message'] = "Authorization Required"
        if r.status_code == 201 or r.status_code == 200:
            return True, doc, output
        else:
            return False, doc, output        
        
    def Execute(self, runbook_id, params, dictionary=False):
        headers = {'Content-Type': 'application/atom+xml'}
        data = self.Build(runbook_id, params, dictionary=dictionary)
        try: 
            if data['status'] == 400: return data
        except: pass
        r = self.session.post(self.host + "/Jobs", data=data, headers=headers)
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        properties = doc['entry']['content']['m:properties']
        output['result']['id'] =  properties['d:Id']['#text']
        output['result']['status'] = properties['d:Status']
        output['result']['CreationTime'] = properties['d:CreationTime']['#text']
        output['result']['LastModifiedTime'] = properties['d:LastModifiedTime']['#text']
        return output            

    def GetJobStatus(self, job_id):
        r = self.session.get(self.host + "/Jobs(guid'%s')" % job_id)
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        properties = doc['entry']['content']['m:properties']
        output['result']['id'] =  properties['d:Id']['#text']
        output['result']['status'] = properties['d:Status']
        output['result']['CreationTime'] = properties['d:CreationTime']['#text']
        output['result']['LastModifiedTime'] = properties['d:LastModifiedTime']['#text']
        return output               

    def GetJobInstance(self,job_id):
        r = self.session.get(self.host + "/Jobs(guid'%s')/Instances" % job_id)
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        return doc['feed']['entry']['content']['m:properties']['d:Id']['#text']

    def GetInstanceParameters(self, instance_id):
        r = self.session.get(self.host + "/RunbookInstances(guid'%s')/Parameters" % instance_id)
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        for e in doc['feed']['entry']:
            output['result'][str(e['content']['m:properties']['d:Name'])] = e['content']['m:properties']['d:Value']
        return output

    def GetRunbooks(self):
        r = self.session.get(self.host + "/Runbooks")
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        for e in doc['feed']['entry']:
            output['result'][str(e['title']['#text'])] = e['content']['m:properties']['d:Id']['#text']
        return output

    def GetRunbookID(self, runbook_name):
        dict = self.GetRunbooks()
        if dict['status'] != 200: return dict
        output, output['result'] = {}, {}
        if runbook_name not in dict['result']:
            output['status'] = 400
            output['message'] = "Runbook ID could not be found for %s" % runbook_name
            return output
        return dict['result'][runbook_name]

    def GetParameters(self, runbook_id):
        r = self.session.get(self.host + "/Runbooks(guid'%s')/Parameters" % runbook_id)
        success, doc, output = self.intParseOutput(r)
        if not success: return output
        for e in doc['feed']['entry']:
            output['result'][str(e['title']['#text'])] = e['content']['m:properties']['d:Id']['#text']
        return output

    def Build(self, runbook_id, params, dictionary=False):
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
        if dictionary == False:
            for setting_var in params:
                setting_val = '<Parameter><ID>{%s}</ID><Value>%s</Value></Parameter>' % (setting_var, params[setting_var])
                settings_array.append(setting_val)
        if dictionary == True:
            dict = self.GetParameters(runbook_id)
            if dict['status'] != 200: return dict
            for setting_var in params:
                try:
                    setting_val = '<Parameter><ID>{%s}</ID><Value>%s</Value></Parameter>' % (dict['result'][setting_var], params[setting_var])
                    settings_array.append(setting_val)
                except:
                    output, output['status'],output['message'] = {}, 400, "Object '%s' does not exist in runbook {%s}" % (setting_var, runbook_id)
                    return output
        params = ('').join(settings_array)
        return BASE % (runbook_id, params)
