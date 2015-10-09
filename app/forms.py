from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, StringField, HiddenField, PasswordField, SubmitField, SelectField
from wtforms.validators import *
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import EmailField

class AZP2FAForm(Form):
    wav_file = FileField('WAV file', validators=[FileRequired(),FileAllowed(['wav', 'WAV'], 'please select a .wav file')])
    transcript_file = FileField('Transcript file', validators=[FileRequired(), FileAllowed(['txt', 'TXT'], 'please select a .txt file')])
    language = SelectField(u'Language', choices=[('english', 'English')])
    options = SelectField(u'Options', choices=[('silence', 'add SILENCE tags between items'), ('noise', 'add NOISE tags between items')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Get TextGrid', id='get-textgrid')

class PairwiseCSVForm(Form):
    csv_file = FileField('csv file',
                         validators=[FileRequired(),
                                     FileAllowed(['csv', 'CSV'], 'please select a two-column .csv file')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Get Similarity Scores', id='pairwisecsv-submit')

class KNNCSVForm(Form):
    csv_file = FileField('csv file',
                         validators=[FileRequired(),
                                     FileAllowed(['csv', 'CSV'], 'please select a single-column .csv file')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Get K Nearest Neighbors', id='knncsv-submit')

class LoginForm(Form):
    provider = SelectField(u'Log in with...',
                    choices = [("google","Google"), ("gh","GitHub"), ("fb","FaceBook")],
                    validators = [Required()])
    username = StringField('Username', id='username', validators=[InputRequired("Forgetting something?")])
    password = PasswordField('Password', id='password', validators=[Required()])
    submit = SubmitField('Log in', id='login')

class RegisterForm(Form):
    #name = StringField('Name', id='name')
    username = StringField('Username', id='username', validators=[Required("Uh-oh! You forgot to choose a username.")])
    password = PasswordField('Password', id='password', validators=[Required("Is it safe?  Is it secret?")])
    email = EmailField('Email', id='email', validators=[Required("For a timely delivery of spam, of course..."), Email()])
    submit = SubmitField('Reporting for duty!', id='register')

class TraceForm(Form):
    name = StringField('Tracer ID', id='tracer', validators=[Required()])
    subject = StringField('Subject', id='subject')
    project_id = StringField('Project ID', id='project', validators=[Required()])
    data = HiddenField(id='trace-data')
    submit = SubmitField('Get traces', id='dump-traces')
