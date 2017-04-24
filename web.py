# -*- coding: utf-8 -*-
#
# Copyright (C) 2016-2017 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Author:
#     Maria Peña Hernan


import http.server
import http.client
import json

class OpenFDAClient():

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_events(self, limite):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit='+limite)
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_events_searchDrugs(self, incognita):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+incognita+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_events_searchCompanies(self, incognita):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=companynumb:'+incognita+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events


class OpenFDAParser():

    def get_drugs(self, limite):

        CLIENT = OpenFDAClient()
        events = CLIENT.get_events(limite)
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_companies_search(self, incognita):

        CLIENT = OpenFDAClient()
        events= CLIENT.get_events_searchDrugs(incognita)
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies

    def get_companies(self, limite):

        CLIENT = OpenFDAClient()
        events = CLIENT.get_events(limite)
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies

    def get_drugs_search(self, incognita):

        CLIENT = OpenFDAClient()
        events= CLIENT.get_events_searchCompanies(incognita)
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_patient_sex(self, limite):

        CLIENT = OpenFDAClient()
        events = CLIENT.get_events(limite)
        patient_sex = []
        results = events['results']
        for event in results:
            patient_sex += [event['patient']['patientsex']]
        return patient_sex


class OpenFDAHTML():

    def get_main_page(self):

        html = """
        <html>
            <head>
                <title>OpenFDA</title>
                <h1>OpenFDA</h1>
            </head>
            <body>
                <form method="get" action="listDrugs">
                    <input type = "submit" value="Drug List: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>
                <form method="get" action="searchDrug">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search: Send to OpenFDA"></input>
                </form>
                <form method="get" action="listCompanies">
                    <input type = "submit" value="Company List: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
                </form>
                <form method="get" action="searchCompany">
                    <input type = "text" name="company"></input>
                    <input type = "submit" value="Company Search: Send to OpenFDA"></input>
                </form>
                <form method='get' action='listGender'>
                    <input type = "submit" value="Patient Sex: Send to OpenFDA"></input>
                    Limit:
                    <input type = "text" name="limit"></input>
            </body>
        </html>
        """
        return html

    def get_page_receive_drugs(self, drugs):

        s = ''
        for drug in drugs:
            s += '<li>' +drug+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Products</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_receive_companies(self, companies):

        s = ''
        for comp in companies:
            s += '<li>' +comp+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Companies</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_search_drug(self, companies):

        s = ''
        for company in companies:
            s += '<li>' +company+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Medicinal Companies</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_search_company(self, drugs):

        s = ''
        for drug in drugs:
            s += '<li>' +drug+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Companynumb</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_for_patient_sex(self, patient_sex):

        s = ''
        for patient in patient_sex:
            s += '<li>' +patient+ '</li>'

        html = '''
        <html>
        <head> </head>
        <body>
            <h1>Patient Sex</h1>
            <ol>
                %s
            </ol>
        </body>
        </html>
        ''' %(s)

        return html

    def get_page_for_error(self):

        html = '''
        <html>
            <head></head>
                Implement 404, Page Not Found
            <body></body>
        </html>
        '''
        return html

    def get_page_fot_secret(self):

        html = '''
        <html>
            <head></head>
                You need an autentification
            <body></body>
        </html>
        '''
        return html



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        CLIENT = OpenFDAClient()
        PARSER = OpenFDAParser()
        HTML = OpenFDAHTML

        main_page = False
        is_eventDrug= False
        is_eventCompany = False
        is_searchDrug = False
        is_searchCompany = False
        is_patientsex = False
        is_found = False
        is_secret = False
        is_redirect = False


        if self.path == '/':
            main_page = True
            is_found = True
        elif '/listDrugs' in self.path:
            is_eventDrug = True
            is_found = True
        elif '/listCompanies' in self.path:
            is_eventCompany = True
            is_found = True
        elif 'searchDrug' in self.path:
            is_searchDrug = True
            is_found = True
        elif 'searchCompany' in self.path:
            is_searchCompany = True
            is_found = True
        elif 'listGender' in self.path:
            is_patientsex = True
            is_found = True
        elif 'secret' in self.path:
            is_secret = True
            is_found = True
        elif 'redirect' in self.path:
            is_redirect = True
            is_found = True

        if is_secret:
            self.send_response(401)
            self.send_header ('WWW-Authenticate', 'Basic realm="Login required"')
        elif is_redirect:
            self.send_response(302)
            self.send_header('Location','/')
        elif is_found:
            self.send_response(200)
            self.send_header('Content-type','text/html')


        else:
            self.send_response(404)
            self.send_header('Content-type','text/html')

        self.end_headers()


        if main_page:
            html = HTML.get_main_page(self)
            self.wfile.write(bytes(html, "utf8"))
        elif is_eventDrug:
            limite = self.path.split('=')[1]
            drugs = PARSER.get_drugs(limite)
            html2 = HTML.get_page_receive_drugs(self, drugs)
            self.wfile.write(bytes(html2, "utf8"))
        elif is_searchDrug:
            incognita = self.path.split('=')[1]
            companies = PARSER.get_companies_search(incognita)
            html3 = HTML.get_page_search_drug(self, companies)
            self.wfile.write(bytes(html3, "utf8"))
        elif is_eventCompany:
            limite = self.path.split('=')[1]
            companies = PARSER.get_companies(limite)
            html4 = HTML.get_page_receive_companies(self, companies)
            self.wfile.write(bytes(html4, 'utf8'))
        elif is_searchCompany:
            incognita = self.path.split('=')[1]
            drugs = PARSER.get_drugs_search(incognita)
            html5 = HTML.get_page_search_company(self, drugs)
            self.wfile.write(bytes(html5,'utf8'))
        elif is_patientsex:
            limite = self.path.split('=')[1]
            patientsex = PARSER.get_patient_sex(limite)
            html6 = HTML.get_page_for_patient_sex(self, patientsex)
            self.wfile.write(bytes(html6, 'utf8'))
        elif is_found == False:
            html7 = HTML.get_page_for_error(self)
            self.wfile.write(bytes(html7, 'utf8'))
        return
