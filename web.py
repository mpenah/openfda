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


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_events(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_drugs(self):

        events = self.get_events()
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_events_searchDrugs(self):

        incognita = self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+incognita+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_companies_search(self):

        events= self.get_events_searchDrugs()
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies

    def get_companies(self):

        events = self.get_events()
        companies = []
        results = events['results']
        for event in results:
            companies += [event['companynumb']]
        return companies

    def get_events_searchCompanies(self):

        incognita = self.path.split('=')[1]
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search=companynumb:'+incognita+'&limit=10')
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode('utf8')
        events= json.loads(data)
        return events

    def get_drugs_search(self):

        events= self.get_events_searchCompanies()
        drugs = []
        results = events['results']
        for event in results:
            drugs += [event['patient']['drug'][0]['medicinalproduct']]
        return drugs

    def get_main_page(self):

        html = """
        <html>
            <head>
            </head>
            <body>
                <form method="get" action="listDrugs">
                    <input type = "submit" value="Drug List: Send to OpenFDA"></input>
                </form>
                <form method="get" action="searchDrug">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Drug Search: Send to OpenFDA"></input>
                </form>
                <form method="get" action="listCompanies">
                    <input type = "submit" value="Company List: Send to OpenFDA"></input>
                </form>
                <form method="get" action="searchCompany">
                    <input type = "text" name="company"></input>
                    <input type = "submit" value="Company Search: Send to OpenFDA"></input>
                </form>
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
            <ul>
                %s
            </ul>
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
            <ul>
                %s
            </ul>
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
            <ul>
                %s
            </ul>
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
            <ul>
                %s
            </ul>
        </body>
        </html>
        ''' %(s)

        return html

    def do_GET(self):

        main_page = False
        is_eventDrug= False
        is_eventCompany = False
        is_searchDrug = False
        is_searchCompany = False

        if self.path == '/':
            main_page = True
        elif self.path =='/listDrugs':
            is_eventDrug = True
        elif self.path =='/listCompanies':
            is_eventCompany = True
        elif 'searchDrug' in self.path:
            is_searchDrug = True
        elif 'searchCompany' in self.path:
            is_searchCompany = True

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        if main_page:
            html = self.get_main_page()
            self.wfile.write(bytes(html, "utf8"))
        elif is_eventDrug:
            drugs = self.get_drugs()
            html2 = self.get_page_receive_drugs(drugs)
            self.wfile.write(bytes(html2, "utf8"))
        elif is_searchDrug:
            companies = self.get_companies_search()
            html3 = self.get_page_search_drug(companies)
            self.wfile.write(bytes(html3, "utf8"))
        elif is_eventCompany:
            companies = self.get_companies()
            html4 = self.get_page_receive_companies(companies)
            self.wfile.write(bytes(html4, 'utf8'))
        elif is_searchCompany:
            drugs = self.get_drugs_search()
            html5 = self.get_page_search_company(drugs)
            self.wfile.write(bytes(html5,'utf8'))
        return
