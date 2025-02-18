from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import EmailField, SubmitField, StringField, RadioField, SelectField
import os
from morse_decoder.main import Run
import threading

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
    choice = RadioField('', choices=[('play', 'Play'), ('analyze', 'Analyze')], validators=[DataRequired()])
    text = StringField(label="", render_kw={"placeholder": "Write your text here..."})
    recording_time = SelectField('',
                                 choices=[('5', '5 seconds'), ('10', '10 seconds'), ('15', '15 seconds'),
                                          ('20', '20 seconds'), ('25', '25 seconds'), ('30', '30 seconds')])
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
        # Hämta värdet från recording_time
        recording_time = int(form.recording_time.data) if form.choice.data == "analyze" else None
        choice = form.choice.data
        text = form.text.data

        # Skapa instans av Run
        run = Run(choice, text)
        morse_code = run.text_to_morse

        if run.choice == "play":
            threading.Thread(target=run.play).start()
            return render_template('morse_decoder.html',
                                   form=form,
                                   text=f'Text: {text}<br>Morse Code: {morse_code}',
                                   text_two="To Play write your text in the field 👇 To Analyze choose how many seconds "
                                            "to record 👇")
        elif run.choice == "analyze":
            print(type(recording_time))  # Här kommer inspelningstiden att loggas om den valts
            morse_to_text = run.analyze(recording_time)
            print(morse_to_text)
            return render_template('morse_decoder.html',
                                   form=form,
                                   text=f'Decoded Message:<br>{morse_to_text}',
                                   text_two="To Play write your text in the field 👇 To Analyze choose how many seconds "
                                            "to record 👇")

    return render_template('morse_decoder.html',
                           form=form,
                           text="Morse En- & Decoder",
                           text_two="To Play write your text in the field 👇 To Analyze choose how many seconds "
                                    "to record 👇")


if __name__ == '__main__':
    app.run(debug=True)