import os
from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from control import app, db


# 建立一個User類別，該類別繼承了db.Model，這個類別可以提供我們未來與資料庫進行溝通傳遞
class Users(db.Model):
    _id = db.Column('id', db.Integer, primary_key=True) # column：欄位
    name = db.Column('name', db.String(100))
    #email = db.Column(db.String(100))
    def __init__(self, name#, email
                            ):
        self.name =name
        #self.email = email
    def __repr__(self):
        return f'使用者名稱為 {self.name}'
    
    

    
def add(name):
    # 1
    new_user = Users(name)
    # 2
    db.session.add(new_user)
    # 3
    db.session.commit()