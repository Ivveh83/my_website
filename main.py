from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, length
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import EmailField, SubmitField, StringField, RadioField
import os

sending_email = os.environ.get("SENDING_EMAIL")
password = os.environ.get("SENDING_EMAIL_PASSWORD")
my_email = os.environ.get('MY_EMAIL')

flask_key = os.environ.get('FLASK_KEY')


app = Flask(__name__)
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)

app.config['SECRET_KEY'] = flask_key

class PostForm(FlaskForm):
    phone = StringField(label="", render_kw={"placeholder": "Phone Number (optional)"})
    email = EmailField(label="", render_kw={"placeholder": "Email (required)"}, validators=[DataRequired(), Length(max=50)])
    body = CKEditorField(label="", validators=[DataRequired()])
    submit = SubmitField('Submit Mail')

class MorseForm(FlaskForm):
    choice = RadioField('Play or Analyze Morse:', choices=[('play', 'Play'), ('analyze', 'Analyze')], validators=[DataRequired()])
    text = StringField(label="", render_kw={"placeholder": "What do you want to send in Morse Code?"})
    submit = SubmitField('Submit')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = PostForm()  # Skapa formuläret

    if form.validate_on_submit():  # Om POST + validering lyckas
        email = form.email.data
        phone = form.phone.data or "Missing"
        message = form.body.data  # Rätt fältnamn!

        # Skicka e-post
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=sending_email, password=password)
            connection.sendmail(
                from_addr=sending_email,
                to_addrs=my_email,
                msg=f"Subject: New message from My Website\n\n"
                    f"Email: {email}\nPhone: {phone}\nMessage: {message}".encode('latin1')
            )

        return render_template('contact.html', form=PostForm(), text="Message successfully delivered, I'll get back to you ASAP!")

    # Om GET eller fel vid POST, visa formuläret igen
    return render_template('contact.html', form=form, text="Don't be a Stranger ...")



@app.route('/morse_decoder', methods=['GET', 'POST'])
def morse_decoder():

    form = MorseForm()
    if form.validate_on_submit():
        choice = form.choice.data
        text = form.text.data
        print(choice)
        print(text)
        return render_template('morse_decoder.html',
                               form=form,
                               text="Morse decoder",
                               text_two="This is a two-way Morse Decoder")


    return render_template('morse_decoder.html',
                           form=form,
                           text="Morse Decoder",
                           text_two="This is a two-way Morse Decoder")



if __name__ == '__main__':
    app.run(debug=True)