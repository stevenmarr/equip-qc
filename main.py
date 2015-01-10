#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import datetime
import pickle
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
import google.appengine.ext.blobstore

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("admin.html")
                
class admin(Handler):
    def get(self):
        self.render("admin.html")
        
class manage(Handler):
    def get(self, barcode):
        assets = db.GqlQuery("SELECT * FROM Equipment WHERE barcode = '%s'" %str(barcode))
        flag = 0
        for asset in assets:
            if asset.barcode == str(barcode):
                manufacturer = asset.manufacturer
                model = asset.model
                
                self.render("template.html", manufacturer = asset.manufacturer, model = asset.model, man_url = asset.manual_url)
                flag = 1
                break
        if flag == 0:
            self.render("template.html", manufacturer = "ID NOT FOUND")
        
class add_new_asset(Handler):
    manufacturer_model_dict = {}
    model_list = []
    
    def get(self):
        #Run this on the initial GET method from the HTTP Header
        if self.request.get("manufacturer") == "":
            #Build Data Base
            inventory = db.GqlQuery("SELECT * FROM Equipment WHERE manufacturer != ''")
            #Build model lists to store in each manufacturer DICT value
            for item in inventory:
                model_list = []
                model_db = db.GqlQuery("SELECT * FROM Equipment WHERE manufacturer = '%s'" %item.manufacturer)
                
                for model in model_db:
                    model_list.append(model.model)
                #Build 
                self.manufacturer_model_dict[item.manufacturer] = model_list
            
            
            manufacturer_list = self.manufacturer_model_dict.keys()
            manufacturer_list.sort()
            self.render("add_new_asset.html", manufacturer_list = manufacturer_list, model_list = "")
    def post(self):
        barcode = self.request.get("barcode")
        if barcode == "":
            #self.write("dict %s" %self.manufacturer_model_dict)
            manufacturer_list = []
            manufacturer = (self.request.get("manufacturer"))
            manufacturer_list.append(manufacturer)
            self.model_list=self.manufacturer_model_dict[manufacturer]
            self.render("add_new_asset.html", manufacturer_list=manufacturer_list,
                                                model_list = self.model_list)
            model_list = self.model_list
        else:
            barcode = self.request.get("barcode")
            manufacturer = self.request.get("manufacturer")
            model = self.request.get("model")
            asset_comments = self.request.get("asset_comments")
            asset_comments = asset_comments.replace('/n', '<br>')
            #self.write(" %s, %s, %s, %s" %(barcode, manufacturer, model, asset_comments))
            entry_type = 'asset'
            entry = Equipment(barcode = barcode, manufacturer = manufacturer , model = model, asset_comments = asset_comments, entry_type = entry_type)
            entry.put()
            #self.redirect('/admin')

class add_new_kit(Handler):
    #Get Manufacturer
    #Get Model
    #Outline QC Process
    #Link manual url
    #
    
    def get(self):
        self.render("add_new_kit.html", manual_url = "http://")
    def post(self):
        barcode = self.request.get("barcode")
        manufacturer = self.request.get("manufacturer")
        model = self.request.get("model")
        kit_contents = kit_contents.replace('/n', '<br>')
        qc_process = qc_process.replace('/n', '<br>')
        entry_type = 'kit'
        entry = Equipment(barcode = barcode, manual_url = manual_url, manufacturer = manufacturer,model = model, kit_contents = kit_contents, qc_process = qc_process, entry_type = entry_type)
        
        entry.put()

		
#class Model(polymodel.PolyModel):
class Model(db.Model):		
	
	def __init__(manu, model, desc):
		self.manu = manu
		self.model = model
		self.desc = desc
		
	def addURL(self, url, type="manual"):
		self.url = (url,type)
	def add	
	def addComments(self, user, comment, date):
		Model.comments.append[(user, date, comment)]
	def	addQCStep(self, stepNumber, description):
		Model.qcProcess.append((stepNumber, description))
	def updateModel():
		self.Model.put()
		#save db entry

class listModels(Handler):
	def get(self):
		self.render("list_models.html", models = Model)	
	
	
#class Asset(Model):



#class Kit(Model):



class add_new_item(Handler):
    #Get Manufacturer
    #Get Model
    #Outline QC Process
    #Link manual url
    def get(self):
        #Run this on the initial GET method from the HTTP Header
        if self.request.get("manufacturer") == "":
            #Build Data Base
            inventory = db.GqlQuery("SELECT * FROM Equipment WHERE manufacturer != ''")
            #Build manufacturer lists to poplulate HTML <select>
            manufacturer_list = []
            for manufacturers in inventory:
                manufacturer_list.append(manufacturers.manufacturer)
            
            manufacturer_list.sort()
            self.render("add_new_item.html", manufacturer_list = manufacturer_list)
    def post(self):
		manufacturer = self.request.get("manufacturer")
		if manufacturer == "":
			manufacturer = self.request.get("manufacturer_keyed")
			
        #manufacturer = self.request.get("manufacturer")
		model = self.request.get("model")
		qc_process = self.request.get("qc_process")
		qc_process = qc_process.replace('/n', '<br>')
		manual_url = self.request.get("manual_url")
		entry_type = 'item'
)
		entry = Equipment(manufacturer=manufacturer, model = model,
                                qc_process = qc_process, manual_url =manual_url,
                                entry_type = entry_type)
		entry.put()
        
class Equipment(db.Model):
	manURL = db.ListProperty(str)
    kit_id = db.StringProperty()
    barcode = db.StringProperty()
    manual_url = db.LinkProperty()
    manufacturer = db.StringProperty()
    model = db.StringProperty()
    kit_contents = db.TextProperty()
    qc_process = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add = True)
    unit_history = db.TextProperty()
    asset_comments = db.TextProperty()
    entry_type = db.TextProperty(required = True)

app = webapp2.WSGIApplication([
    ('/?', MainHandler),('/admin', admin),('/manage/([0-9]+)', manage),
    ('/new_kit', add_new_kit),('/new_item', add_new_item),
    ('/new_asset', add_new_asset),('/models', listModels)
], debug=True)
