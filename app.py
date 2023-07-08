from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
import os


root_dir = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(root_dir, 'orders.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Canopy20181122713'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'canopysystem@outlook.com'
app.config['MAIL_PASSWORD'] = 'Canopy20181122713'
app.config['MAIL_DEFAULT_SENDER'] = 'canopysystem@outlook.com'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Define the database model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    plan = db.Column(db.String(20), nullable=False)

# Define the checkout form
class CheckoutForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    plan = SelectField('Plan', choices=[('basic', 'Basic'), ('pro', 'Pro'), ('premium', 'Premium')], validators=[DataRequired()])
    
def send_email(subject, body, recipients):
    message = Message(subject, body=body, recipients=recipients, sender=app.config['MAIL_DEFAULT_SENDER'])
    mail.send(message)



@app.route('/')
@app.route('/home')
def landing_page():
    return render_template('index.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()

    if request.method == 'POST' and form.validate_on_submit():
        # Retrieve form data
        name = form.name.data
        email = form.email.data
        phone_number = form.phone_number.data
        address = form.address.data
        plan = form.plan.data

        # Save the form data to the database
        order = Order(name=name, email=email, phone_number=phone_number, address=address, plan=plan)
        db.session.add(order)
        db.session.commit()

        # Send emails to CEO and CTO
        ceo_email = 'andromeda6761@gmail.com'
        cto_email = 'akormichaeljohn@gmail.com'
        ceo_body = f"Name: {name}\nEmail: {email}\nPhone: {phone_number}\nAddress: {address}\nPackage: {plan}"
        cto_body = ceo_body
        send_email(f'New User Ordered Canopy Sensor', ceo_body, [ceo_email])
        send_email(f'New User Ordered Canopy Sensor', cto_body, [cto_email])
        


        # Send confirmation email to the user
        user_body = f"Dear {name},\nThank you for placing your order with Canopy! We appreciate your interest in our Canopy sensor, and we are excited to have you as a valued customer.\nOrder Details:\n- Name: {name}\n- Email: {email}\n- Phone Number: {phone_number}\n- Address: {address}\n- Plan: {plan}\nPlease note that our Canopy sensors are currently in high demand, and we are working diligently to meet the demand. As soon as the stock is available, we will notify you to complete the purchase process and make the payment with your credit card.\nWe understand the importance of keeping you informed, and we assure you that we will provide regular updates on the availability of the Canopy sensors. We appreciate your patience and understanding.\nIf you have any questions or need further assistance, please don't hesitate to reach out to our customer support team at {ceo_email}.\nThank you once again for choosing Canopy. We look forward to serving you soon!\nBest regards,\nThe Canopy Team\nNote: This is an automated email. Please do not reply to this email. If you have any inquiries, please contact us directly at {ceo_email}."
        send_email(f'Your Canopy Sensor Order Confirmation', user_body, [email])

        print(email)

        flash('Your order has been placed. You will receive a confirmation email shortly.')
        return redirect(url_for('success'))

    return render_template('checkout.html', form=form)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')