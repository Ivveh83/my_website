import os
import secrets
import threading
import smtplib
import subprocess
import soundfile as sf
import numpy as np
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor, CKEditorField
from morse_decoder.main import Run
from wtforms import EmailField, SubmitField, StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length

# Miljövariabler
sending_email = os.environ.get("SENDING_EMAIL")
password = os.environ.get("SENDING_EMAIL_PASSWORD")
my_email = os.environ.get("MY_EMAIL")
flask_key = os.environ.get("FLASK_KEY")
UPLOAD_FOLDER = "morse_decoder/audio"

app = Flask(__name__)
ckeditor = CKEditor(app)
bootstrap = Bootstrap5(app)
app.config["SECRET_KEY"] = flask_key

# ----- CSRF-token generator -----
def generate_csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(16)
    return session["_csrf_token"]

app.jinja_env.globals["csrf_token"] = generate_csrf_token
# --------------------------------

# WTForms för kontakt (endast för kontaktformuläret)
from flask_wtf import FlaskForm
class PostForm(FlaskForm):
    phone = StringField(label="", render_kw={"placeholder": "Phone Number (optional)"})
    email = EmailField(label="", render_kw={"placeholder": "Email (required)"}, validators=[DataRequired(), Length(max=50)])
    body = CKEditorField(label="", validators=[DataRequired()])
    submit = SubmitField('Submit Mail')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = PostForm()
    if form.validate_on_submit():
        email = form.email.data
        phone = form.phone.data or "Missing"
        message = form.body.data

        # Skicka e-post
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=sending_email, password=password)
            connection.sendmail(
                from_addr=sending_email,
                to_addrs=my_email,
                msg=f"Subject: New message from My Website\n\n"
                    f"Email: {email}\nPhone: {phone}\nMessage: {message}".encode("latin1")
            )
        return render_template("contact.html", form=PostForm(), text="Message successfully delivered, I'll get back to you ASAP!")

    return render_template("contact.html", form=form, text="Don't be a Stranger ...")

# Morse decoder: ingen WTForms – manuell CSRF-validering
@app.route("/morse_decoder", methods=["GET", "POST"])
def morse_decoder():
    errors = {}
    # Grundvärden för values
    values = {
        "choice": "",
        "text": "",
        "recording_time": "5"
    }
    if request.method == "POST":
        # Hantera CSRF-token från AJAX/FETCH eller form
        form_token = request.form.get("csrf_token") or request.values.get("csrf_token")
        session_token = session.get("_csrf_token")
        if not form_token or form_token != session_token:
            flash("Ogiltig CSRF-token – försök igen.", "warning")
            return render_template(
                "morse_decoder.html",
                text="CSRF-token saknas/ogiltig – ladda om sidan och försök igen.",
                values=values,
                errors=errors
            )

        # Data från FormData (JS) eller vanliga POST-fält
        choice = request.form.get("choice") or request.values.get("choice")
        text = request.form.get("text")
        recording_time = request.form.get("recording_time")

        run = Run(choice, text or "")

        if choice == "play":
            morse_code = run.text_to_morse
            threading.Thread(target=run.play).start()
            return render_template(
                "morse_decoder.html",
                text=f"Text: {text}<br>Morse Code: {morse_code}",
                values=values,
                errors=errors
            )

        elif choice == "analyze":
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            if "audio" in request.files:
                audio_file = request.files["audio"]
                if audio_file.filename:
                    # Spara temporär WebM
                    temp_path = os.path.join(UPLOAD_FOLDER, "temp_audio.webm")
                    file_path = os.path.join(UPLOAD_FOLDER, "audio_recording.wav")
                    audio_file.save(temp_path)

                    # Konvertera till WAV med ffmpeg
                    subprocess.run([
                        "ffmpeg", "-y", "-i", temp_path,
                        "-acodec", "pcm_s16le",
                        "-ar", "44100",
                        "-ac", "1",
                        file_path
                    ], check=True)

                    os.remove(temp_path)

                    audio_data, sample_rate = sf.read(file_path, dtype="float32")
                    audio_array = (audio_data * 32767).astype(np.int16)
                    sf.write(file_path, audio_array, sample_rate, format="WAV", subtype="PCM_16")

                    morse_to_text = run.analyze()
                    print("Morse to text: " + morse_to_text)
                    return f"Decoded Message:<br>{morse_to_text}"
            # Om ingen/ogiltig fil
            return render_template(
                "morse_decoder.html",
                text="Ingen ljudfil uppladdad eller fel på filen.",
                values=values,
                errors=errors
            )

    # GET-besök
    return render_template(
        "morse_decoder.html",
        text="Morse En- & Decoder",
        values=values,
        errors=errors
    )

if __name__ == "__main__":
    app.run(debug=True)