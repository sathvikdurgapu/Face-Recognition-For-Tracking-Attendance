from flask import Flask,render_template,request,redirect,url_for,session
from flask_bootstrap import Bootstrap
import MySQLdb
import os
from math import sqrt
from sklearn import neighbors
from os import listdir
from os.path import isdir, join, isfile, splitext
import shutil
import pickle
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import face_recognition
from face_recognition import face_locations
from face_recognition.face_recognition_cli import image_files_in_folder
from datetime import datetime,timedelta
from pytz import timezone
import xlsxwriter
import pandas as pd
from glob import glob
from flask_mail import Mail, Message
from io import BytesIO
import base64
import lable_image