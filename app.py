from flask import Flask, send_file, render_template_string
from pywebio.platform.flask import webio_view
from pywebio.output import *
from pywebio.input import *
from pywebio.session import *
from pywebio.pin import *
import smtplib
from email.mime.text import MIMEText



# --- EMAIL CONFIGURATION ---
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_ADDRESS = 'aissaouileith31@gmail.com'            # Remplacez par votre email Gmail
EMAIL_PASSWORD = 'bvhvwphobebknbxs'               # Votre mot de passe d'application Gmail (16 caractères, PAS d'espaces)


def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def show_booking_form():
    with use_scope('input_area', clear=True):
        def validate_form(data):
            if data['action'] == 'cancel':
                return None
            # Validation du formulaire
            if not data['name']:
                return ('name', 'Name is required')
            if not data['phone']:
                return ('phone', 'Phone number is required')
            if not data['date']:
                return ('date', 'Preferred date is required')
            if not data['sexe']:
                return ('sexe','sexe is required')
            if not data['email']:
                return('email','e-mail is required')
            return None

        booking = input_group("Booking Form", [
            input("Full Name", name="name"),
            input("Phone Number", name="phone", type=NUMBER, placeholder="+213 7xx xxx xxx"),
            input("Preferred Date", name="date", type=DATE),
            radio('sexe',options =['Man','Women'],name='sexe'),
            input('e-mail' ,name="email"),
            textarea("Describe your concern", name="message",
                     placeholder="e.g. tooth pain, cleaning, braces..."),
            actions("", buttons=[
                {'label': 'Submit', 'value': 'submit', 'color': 'success'},
                {'label': 'Cancel', 'value': 'cancel', 'color': 'danger'},
            ], name='action')
        ], validate=validate_form)

        if booking['action'] == 'submit':
            # Compose email
            subject = f"New Booking from {booking['name']}"
            body = f"""
                Name: {booking['name']}
                Phone: {booking['phone']}
                Date: {booking['date']}
                email: {booking['email']}
                sexe: {booking['sexe']}

                Message:
                {booking['message']}
                """
            # Send email
            send_email(subject, body, EMAIL_ADDRESS)
            toast(f"✅ Thank you, {booking['name']}! We’ll contact you at {booking['phone']} to confirm your appointment.",
                  position='top', color='success')
            clear('input_area')
        else:
            clear('input_area')


    

def give_feed_back():
    with use_scope('input_area', clear=True):
        def validate_form(data):
            # Skip validation if user clicked cancel
            if data['action'] == 'cancel':
                return None
            # Validate if submit clicked
            if not data['name']:
                return ('name', 'Name is required')
            if not data['feedback']:
                return ('feedback', 'Feedback is required')
        
        feedback = input_group("Feedback Form", [
            input("Your Name", name="name", placeholder="Enter your name"),
            textarea("Your Feedback", name="feedback", placeholder="Write your feedback here...", rows=6),
            actions("", buttons=[
                {'label': 'Submit', 'value': 'submit', 'color': 'success'},
                {'label': 'Cancel', 'value': 'cancel', 'color': 'danger'},
            ], name='action')
        ], validate=validate_form)

        if feedback['action'] == 'submit':
            toast(f"Thank you, {feedback['name']}! 🙏\n your feedback is submeted ",position='top', color='success')
            clear('input_area')
        elif feedback['action'] == 'cancel':
            clear('input_area')


    


def contact_us():
    clear()
    put_html("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
            padding: 2em;
            color: #333;
        }
        .contact-container {
            max-width: 800px;
            margin: auto;
            background-color: white;
            padding: 2em;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }
        h1 {
            color: #0072CE;
            font-size: 2.5em;
        }
        p {
            font-size: 1.1em;
        }
        .info {
            margin-bottom: 1.5em;
        }
    </style>

    <div class="contact-container">
        <h1>Contact Us</h1>
        <p class="info">
            We'd love to hear from you! Whether you have questions, need to book an appointment, or just want to say hello — reach out any time.
        </p>
        <p>
            📍 <strong>Clinic brush dental</strong><br>
            Coop el rahmane lot n 16 hai khemisti bir el djir - ORAN<br>
            Phone: <a href="tel:📞 07 93083638">0793083638/05 40013051</a><br>
            Email: <a href="mailto:brush_dental@brightsmile.com">brush_dental@gimail.com</a><br>
            Open: 6j/7j - 9h/17h 
        </p>
    </div>
    """)
    put_button('back',onclick=lambda:App())




def about_us():
    clear()
    put_html("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
            color: #333;
            padding: 2em;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background-color: white;
            padding: 2em;
            border-radius: 8px;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }
        h1 {
            color: #0072CE;
            font-size: 2.5em;
        }
        h2 {
            color: #444;
        }
        .highlight {
            color: #0072CE;
            font-weight: bold;
        }
        .team-member {
            margin-top: 2em;
        }
        .team-member img {
            width: 120px;
            border-radius: 50%;
            margin-right: 1em;
        }
        .team-info {
            display: flex;
            align-items: center;
        }
        .team-text {
            max-width: 600px;
        }
    </style>

    <div class="container">
        <h1>About Us</h1>
        <p>
            At <span class="highlight">Brush dentel clinic</span>, we believe everyone deserves a smile they can be proud of. 
            Our mission is to provide expert, gentle, and personalized dental care that leaves you feeling confident and comfortable.
        </p>

        <h2>Why Choose Us?</h2>
        <ul>
            <li>✔️ Experienced and compassionate dental professionals</li>
            <li>✔️ State-of-the-art technology for pain-free treatment</li>
            <li>✔️ A calming, patient-first environment</li>
            <li>✔️ Tailored treatment plans for every age and smile</li>
        </ul>

        <h2>Meet Our Team</h2>

        <div class="team-member">
            <div class="team-info">
                <img src="https://via.placeholder.com/120" alt="photo">
                <div class="team-text">
                    <strong>Dr.benmahammed fatiha,</strong><br>
                    Founder & Chief Dentist<br>
                    With over 15 years of experience, Dr. Smith is passionate about painless care and helping patients feel at ease.
                </div>
            </div>
        </div>


        <h2>Our Vision</h2>
        <p>
            We’re more than just a dental office — we’re your partners in long-term oral health. Whether it’s your child’s first visit 
            or a complete smile transformation, we’re here every step of the way.
        </p>
    </div>
    """)
    put_button('back',onclick=lambda:App())





def App():
    # Clear screen
    clear()


    put_html("<script>document.title = 'brush_detal';</script>")
    put_html("""
        <div style="padding: 0 20px;">
    """) 
    put_buttons(["about us" , "contact us" , "give feedback"], onclick=[lambda:about_us(),lambda:contact_us(),lambda:give_feed_back()])


    # Header Section
    put_html("""
    <div style="
        background-color: #0a3d62;
        text-align: center;
        color: white;
        font-size: 36px;
        font-weight: bold;
        border-radius: 10px;
        margin-bottom: 20px;
        font-family: 'Segoe UI', sans-serif;
    ">
        🦷 BRUSH dental
        <div style="font-size:16px; font-weight:normal; color:#dff9fb;">Clinic dentel</div>
    </div>
    """)

    # Hero Section
    put_html("""
    <div style="
        display: flex;
        background-color: #f5f6fa;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        overflow: hidden;
        font-family: 'Segoe UI', sans-serif;
    ">
        <div style="flex: 1; padding: 30px;">
            <h2 style="color:#0a3d62;">Smile Like You Mean It</h2>
            <p style="font-size:16px;">Step into a world of premium dental care — discreet, gentle, and tailored to perfection. Your radiant smile begins with a private consultation.</p>
        </div>
        <div style="flex: 1;">
            <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMSEhUTEhMVFRUXGBUVFhUXFRUVFxgVGBcWGBUVGBUYHSggGBolHRUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGxAQGi0lICUrLS0tLS0tLS0tLS0tLS0tLSstLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIARMAtwMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAEAQIDBQYABwj/xAA6EAABAwEGAggEBAcBAQEAAAABAAIRAwQFEiExQVFhBhMicYGRobEywdHwB0JS4RQVI2JygpIzovH/xAAaAQACAwEBAAAAAAAAAAAAAAADBAABAgUG/8QALREAAwACAQMDAwMDBQAAAAAAAAECAxEhBBIxIkFRExQyBXGBYZHwFTOxwdH/2gAMAwEAAhEDEQA/APWglhIE5ZNCLlxXBQhlPxHdFlJ/uHzXhd13f/EWoz8Le0e4aD3Xun4ltP8ABuj9TPdeO9HT1Yqu3Li30/cIL4psMluUi+rlrB/qD4kzl45LPW62SctPuFLb7WXQZ/LHgc/SUK2yE56qpWvJdPfgFdUMjn45qSz1A0wdDHlP09lO2xGfhkbhXVh6LOqZt2zHdutOkjKhsEu2pBDefmNlqbRYHsa2vSkOacWWUjVFXF0TBIB1G58PmtxRuxrGYYnZCb29oKlpaYRc14C0UWVRuM+/dWYWVuOl/DWh9Af+dUGrT5PHxs8oPmtU3RNQ9oWtaZxTU5ItGRq5KkVliLkq5QoaQmkJ6RQoYQuTiEihCVKkShYNHQuSrlCFR0ssnW2Wq3eA7/kh3yXg9myFUcHnwlfRz2SCDoRHmvn2+bP1NeozYl3uSg3+QaOZKSo/PktFdVjxAELPWinmDsfRajoziDg14J4HKCPPIqsnjgvH+RobuuOYJjyWpsNmawZBMoOGEKdpSu2N6QXZnBpkKxNcEKmY5TseiTWkDqdsnqWcOcx27HYmnmQWn0JVlRcYVc6oGjE4wN1ZWd0gHYgHzTOFi2VD1yVcjgRpSJxSKiDVyVIrLOSJUhChQhXLiuUKHpQoqU6Hb1CkCwaHLly5Qgq8Y/E+wGnaBUAyMzwkGRrloW+a9nWT6T0qYfTq1GNfrhDgC3GQWiZBH6BpzQsvC2GxcvXyePWGm1zsOoOYOvgfZai7LlfTI1LeBExyncIm3XZSeAKbWU6kiowANbDnCXU3mAIdGR2dyJV90frYmYdHNyc05EEZEEbEEIFXtbQwsfbWmF2dsNG3JSSU9xjYnkFn7yr2kS7HTot2ntHx29UHQTZo2J3XQJWDpdJXsqBrqhqE/paGjvWmqUKlos7wwkOIEQYMTmJ2yWvBXkrbR0gbVrhrnFzWnsUWhz3PcDm5zWglwGsacV6TZagLQcxI3BB4aHuWF6LXE9jxLAHAYZAHwg6krfvoiANtE1h+UK5vhiGq3iEhrN4hQGxN4JpsDeCPsBoINZvEJOvb+oIY2BnBN/l7OCmyaCTXb+oJDaGfqCGN3M4JP5czgq2TQQbUz9QSG2M/UEObuZwTDdzOCvuJoJNup/qC5CG7WcFyruZNFxXtDTAG+hTAFAGkgcQUQFCCpVwSOfGqhY4hUHTCxCpZnNO0/T5q1rXgxuuLwY4+wVZb79s5aWvdAORxNc33CFdS01sJE0mno82uu0Nq1BRruwVhlTqzGOM2g7F2muvfrrLvhtRuOG1C3CX6B8ZAO4ECAHcBB2KwPS6yMcS5hBgxI3A0cPvYcUNcvSB4r0mVSC2G02vc4/8AoCcBc46B2JzCdsc/lELqN+Bmsnsz1q12V5BgO4GATHksnetw43BzsbiNs9OA4eGa3V01sTMiYygGZHEEbEEQRsUW6oUSMG0qTBXn0+1o83u7ou7FLaDmjFizaRJ4S7b7zWvu2x1GEQyBv2m/VWxqH+0eEpzCYmfQIn268tg/uH4SJrsaQHy2DjInLNsAtI8yPAqdz4hQ2GrJIKgt9oioI2GnnKZiNcCebLrkNa6UsIJloaTEwVL1hatPGgU9QychNhMs9oDxltkQpHIbhoPGaaGrkpSLIcQhNITkhUKGFclXKEILTVcGy1mMzETAHMpLFUeDNQtz0a0ZDx3U5pOGeoOsJlJ1MbyeC0mtaZhp74DQue2RrC6mUyvUwjv9FSW2XVKVtmfvuzUyI7bjOZxuMeErH35drXNPV1aoIyw5ukRrmVtKzv6kHIPBOmeNph3n8lDabDTcCKuEgZgkZju3nuWqwT8C+Pq2/LPJOpcJpvmRx14bdypbbZM4ieRzB71r7zsmCoTJgk6md9EHWu8zjbEDM55xyG6XeGpexyepi51vk3fQm96RoOrVarabiP6rHPhjXMlvWNNQkjE0Au7RkydSZ19N4cA4QQcwQQQRxHJeY9H6ANOdczI5HTLxKnu+yVrGSbK4miTJs5OTSdTTnL/U+B2TfZ6doQ+4X1HFvR6GS3gUx9We5UFLpJIGJhnfUGf8SutPSNrYDaVR7nGA0YW+bpyCGskv3Gqilzrg0Vnfhk8pUFYGZ4/ZQ1lteMCRBIBIEkA7iYE7o+zvDgRuEwlo5mTIsj4K+s8jVviETQtLnDUJ7HgOLSmVbNGmi0BSa5QylVLKh55oytaZB5Ae6qHOIeJOXPj3oxuYd97BRok2/BbjMSuKGs1sZkwuGKBkUUQlKlpnailUpjUhSlIVRpjSkTikUITXe+WwdkxrRjdoh30nAuNFwAI3zzQFkZWpBz6va0zbJzJjTYKJbejNUpW2XpcgLXaY9j45JLRbGxkQfHPyVJbLZMjY5HuKPEaEc+bfglt7sRDm/E3Xu3KjrnEq91ZzowzjGUDOToRG4RrDlLsju0Q6DwlFfApHqb0Ul82IFpyUN0NjIq9trWkd/JVFayVKThLSA4S06yFSaKqKT37Ed1WUMq2hg0GBzeQdiy9FY02SoLspkOe92r45ZNkD3PmrG00tCNFcLSKztVWwG8WBuHLPWeXD0ULaoZUpmJJMR35FFWynjYRuM2nnw8VQ3BazUtWEzNMOyGskQEnkwv6yfydTp+pl9LU+6RunkAtjj6Ronh2F6GzkSprUwkBwTpykya8G6OCJoPxtQdmq9ZTIOoS2N8KmuDafO/kit9GNdEtJ8MeeGfhA/dWVRgeIKrK9A02vB0LT+3uVE98FVPa9lJ0lqAdW7QkEA9xB+aJuHpEQQyqZbs7cd6GviwurWWW5upnFG5bEOj38FjqNqLTquhiwzmxdr9i4zuGmez65hIs70TvXGwNJkDIHgeBWiK4+XE8dOWdnHaudoQrlxK5DNAZrmk6nSgdvES46ADbvzH2FLaK+QEgDgor2oF9ORk5ubTz4eKohby4Z6jI8QeCZmFrg5WTNXc1T/YW8KxlwiQDEb+CqalfcGRw3RVetJJ4qW72sbitFSMNOCCcpqH4Bz4+SIuBWvU9bHVz1Awj/ANXR1h/TkIYOBjVBUZYcQ+E6jvz80JZbO60ViaDnueTLzh7Ge7iSAFpLVc76bBigk64ZifFR6nh+Spm8yblcLx/n/IO14ynMctY5c1qrVZWVWCBsC3LTgsVZqga4B3wyJ7pzXoFIZBBy8NND/ReuaTMlbLvLSSB3hJZKmxWottnkSBmPUKkq0WHtSESL7kL5sH064IatjaRLcis/ZaeC14cgXBxyicwJ027HHdaF1UaBUV8kNrWerke0WOGQGYy+atozDW2l7ouqlMjf6qSjV7JB2U9na1zZaJ5akKqvqSx0CCB81pc8A69K2JZLe1jjOmcqut15uqGKLHPAOoyH/WnqpKWQGrjzz8giWUarvykf5fRR18Iix7WqrX7eSNt51aTWEgSTBEzA5xl6oi13hUqEiMLRlGpJ3PIcER/LQG4qsGNG7Sh+rjxVT8vyTKtPUt6DbuqYG9+XmsT01uoUagewdipPg8aj5+a31CmMIniCs30/eBZ2A6vqyOQa05+oTPSW1lWvclL0Ga6N3saL4PwnJw5bEcwc16jdFuFamHbjJ3fxXiDnQZW46AXzFXq3HJ4j/YafRM/qHTq5dryhjos7l9rPQHpFI5q5efOwZKraq1lcGV3OqUSYbVP5Ts2pw/y07lX1bWHk1GsAMlrwSZBG+WoK32FD1bupOnFTaZ1yAPmEWerXujn5P0xv8b/v/wCmFrYIklwJ0DTmTwAK0lG5KTmMo1ZLKfaIxfFVd8RJESGiGj9kSzo/Z2vFQNILTiHaJEjMZHnCINia4yHHmZyUvqU0u0vp/wBPqW/qaYZZG0qbQ2m1rWjYCFM5zXCDmEHSu1v6j5qStZmNEDU5CSfFCl97HnPajPX7deHtNzHstNdlsFWm1w3GY4EahNbY275jIRJT6dnazJjQ3eAIz4lMNdy0xWMXZbqfDCsQG6zN82AYy+mcj8TeDuIHAq8IVTanyVvFGnwTqIWSdMBo2eFV9Kh/Qxfoex/k6PmrwgEZHMiRwI5FVN9APoVW5/A7zAn5IlJnO7HjpbLK7ux1lQRAZIjiYhE0bUyoJyncIG4HipZG8XtYP+Yk+cqSlSptcWNzdElSZ7uQ30q1KXj/AL2HEsHBd/EMHBAWigHNkE6T4ckD2WDGXZASfBU50Brul6aKTpNfr3Wp1JjoZTwtI/uIDjPmEZctRzxMy0auOnhxXnNKzVLTbKtRmKXvxEDMZn83cIXpvRq469GT1zSHAAtc0keSnfKWmwdYMnftJtfsXtjrsJAmTz0nuWP/ABGrmaTHag1D4dla91yjWQDrkHjy7Syf4kXccFOtM4TgJ4tdpPMEeqY6Vz9ZF2r7dNGDqFSXRbDTqNIMQQQh3uQxqQZXYyNaB409n0RY7QKlNjxo5oPmFyz34fW3rLIAdWEjwOY91y8tljstyegx13SmHOvDmojeRVYCVNToOd8LSe4FctdzOi3KDRbS6W8WuA74MKGjeBLQRoQCiKFzVSRMN4SZ9l1K6G06hbVeQ1xlhAAbJ1biOhnQc0RY6aBPLKZC63P4qpt97OFSnBLoLiYO0e2Wq2rbmowWlgcCC04s5BEHu8FJYLspUJFJgbIAMSchoJJ5lOdKlifdXLF89PIu1GdodJQ0dqZ/fNMqdLRJgH7GnmtPabBSqGX02OPEtBPmof5LZ4I6mnBEHsj31Hgm1nx+8i/ZXyZA9JnOBAaTAkxtnm48Bt4qJ97DqjUE9gtJ7iYM8hOfcVX9ILiqWG0CvQzYNuLT8VNx9jyB1CMrPZUwvp/BWYWkHY5hzSOITUUtrS4YF7CjbmtcwEzTqyWf2OAzHIZyPLZNvGphJE5OHnOSp7tul9pszC0nHTAe3XMkZg+SKrUxWotxFwcwgz+YHnx7lb7W2vgBmjcbYdQrihRZRpAl0BjeZiS48Nyn2D+gXgmXfE9xky46DPQAD2UNlrso0uscQ4kfEYnk2Nh9FlbZbqp6wgyXknIgxIgAdwhb0vBp5Enpvk21lvXGcTjhYMgRAxGDJP8Ab9Csz0ktb6FTrZD7HWwhxzmm45Egj8p1132VNWrv6sMJ7AAAHdseSvL2tDG3a+k6C51NwAnPEGlwPhAKzePaNPVLk2d1XHRoMaKTWhpAcCDIcCJDsW8yjnEBZrofeb/4Gg2pOJrYAIJdhBhpJJJ0A3KNr3mBrl35Lz2TitI7GLmdlmy2ZwdNJ4Lzr8Tr6msLM09lgDqgnV5zaD3DPxWss9rFUlrarARGQILonPJRWnoVY7UX1ajHNfUM4w9wIIyBA0zjRdHobeP1Wt/By+tWO77Z4+TyB1RDVKq3V9/hbaGSbPUFZuzT2X/Q+iyFfo9a2Owus9UH/Bx9QIK6/wB1GRcMS+hUPlG8/Dm2ltJ8ckqvvw16PPs9nLqzcLnmQ06gbTzXLjdRSrI2jqYk1CTNG67mupvpgYXjRw14tKXo4CGOa4ZycXfuirYcBFQdzu47qmu2o6lanh57FQjDwDoOXkPRL6SYblov2nQcDCmq0g4FrgCDqCJCGtDoe3+73RYWzIALC9n/AJVSB+h4xt7gZDh5pwtNZvx0cXOm8H/5fB9Sjkx9Vo1IHioUQUrwpkwSWn9LwWH118EUhalspkQe0OET7qAPZ+QFvc4j00WlLMu5XuPvKiHAgictDoVk7dc+EA0aYEPxFoIBMxnmeQWir1TpJJ5oKrOqPjpyJ5WnXchOh1gdSpgPyMDLfTdGXtc9ETUwantAEgTsYHNAUbW5jp8xxWmoVG1GTq0jP5rF1Sru+QuOpyT2mCvzosy0VWim/qjT+N0FzXSM+xIGKd+RVBbegdrBPVvZVbydgd4tdkP+ivQKtkwGo8uOZPkTIySUwQ0OJS9dXc16fAZ/p2PMu7J5PN7H0ZtWMMNJ+uZcIaOeLSO6Vv7r6NUKTe0xtR5+JzwHTyAOgRVjtDn1SDo1oMc3HfuA9VYFwVZOqvIteEEwdHGHjz+4rBGmXIZKg6WWwhhECOJAKuH2oDUrD9ML2DiIcA1sk8zoPdK1Q7MmOr9ZiLmnQzlrPgtJcnTR7S1lpnCMi8DMDmN+9V9loNqthsNJM/7bKkvWzvpSHDMaFEx5HPgFmwza9R7ndt50aw/o1GvgCQDmJ0kahGEL5+uy830ntq0jBGTgNSOC9UuDpZja3rMwdH6R/kE1jl5N68i96j9jWELkgcCJC5UQbVYHy06bqnq2XGHsfqxzS07wILSrumFUX3auqe10SHDAe/ZUyFkBiaMWoPsm1rSdkyyV8TASISVAiyloBkp7IalVx1JUKmLUmFbAPkgcpKL0pppOrhQofUbumMoypKb08PyUIB2izDdVN0XxVpWkUavw1yW02AfAWtBxTwOnqrS1SXhWdGzMOF7mNL2zhcQC5siDB1EjJJ5clVfavY6PT4oiO9rbZPXYHZESs/eT3de0YSWBpM/lDsgPTF6K3qWmCVAagKBTTGYTQNZnhtSp3geTQp61bIoYN7RPFVXSO39XSMHM5D5nyQ3XAVTyUnSLpCGyAV5/brzc8yUXeX6nTyB1JVG+cUbnM8gtY5Xkzkp+EXlgvEsiJzhaS3WinWY5hPayg8N8z4rDfxOgGg9+KsKNslsGZ5eE+krbkwqALZRdTdyP2clo7ovMNDQTkdefPXVA3wMTAe858OCALwGDPwMy07jmESbaapGKhNNM946KVi+zidiQO7ZcvPLr/EJ1Kk2kwUqcDNzxUeSdzDcguXS+3rJ61rkQ+tMel+x6zUJ0aD3oO8rsFRsOOHMGdc+5WNWsG96gawvOJ2mw4pTQbY6x0gG5ZzxTq1McApyFFVREBrlgFRg2UcIh7UyFoE0Ma0plWqIT3zohLQFpIHVfAzrURSdKrzknNrkKzCTfkPtDRAO49t0XZ6nZVXQeXaqd7sGY09kpnjnuR0elyLXY/wCAe8akFD0bUmWy1AqFjZGS51b2dWda5DalpAGZWOvm2daZPwjP6BN6RW57HtYJ7Rjwgys5fVqyFMHXXuGv3zUSbJtSV142qZfqBk0cT+r74wqamYLicznn9+KW22qSOGIADkNfknOGZ8/qmpWkK09sYTH3v9wiKNSI8z6oQPkztqiKGZJ4QPktMyiztdaKYB1ERPdn7qstD4Ezqut9UkQoKtTsgKSiUxjHyuRL7IWAAiCQ13g4At9CFy7XTy1jRycr3bPd7DforVOqpxVqAjEGkHA0nVx0AWoo0SM3GTwGgQNwXPRsVIUqTGtGriBm525J38VYde3iFzZT8jl0lwPTXhJ1reI80mMcR5rYFsheFEwZolzZTMMKymNfTVfaWq1ahbbQkSFaZilxwU72qLAjqVOVILOtGEiKzNhPtzP6bjwh3gCCfSVK2gQp205BB0IIPccisWtrQbH6WmUVpu6cwURY6ZpscfiMGGZAmInM96prNfU0xn2gIOe43QNovl065TJH3ouRvTO4pbQzpBeNJ9M1MGEjJpcIceII23XmlttJe5ztyQB4bK86SXn1tXCwZDY7ncnxVA9oaPnxM7ImNa5YPI98IAFOX92adXccJ5oujS46nXkPsQoLS3OO4eJn9kffIDXBA3IAbn2+wiaZgd+fkhXGXngOyO7T5qSrUgHkPeD8wrMo6pX+f7K26L3C+3WhtJkwJdUds1gOveTkB9CgOj9wV7Y+KTeyNXn4R9Tnovd+ityUbDR6tkT8VSoficQNSdgNhsiTAOrRkelPRWzG0YnVzTaGMbhlozA2Ltow5RxXJl6XSyvaKtarVaMbpDWgvcGgBrZnTIDZcmFky+29AO2Pc9Uove6cYAzyySlikrOTGuWV4M15G9UEmFSSulWZ0MwpA8BOcULVpSdVaKb0SvtoHNRm3g6iPVR/whSiwkq+Ae7Yjw05tInccfBPpFcLrafiPgFVWtrqFUEOik52cguwmIDdcmkxB2PEO7MbLlPfJdgJlR0KvZf9CDFQEhzmGMw17TDmEjIOHAoaveAcCQ4aFV/UJvT0eU2OtjLjNRpJJwtOQGwAIKgtXWtJGbhx0McENY6r8Qc0HPPIRK0FrxvaJb35QfvRcu3pnYhbkoX0J7zl3fUqC00BIA0b78fCFbGzkSSIG2nnwCrqrw44RmB8RGncPqrlkpAuDLll5DRBTJLu8+wVha6ktyyEkeDZHuSgHiB4j0z+aJIKgaytkknSD6mPvuR92WPrXQdyO4E5z4D2QNI9jvy8/wD99FIx7j2Wo+KO60hfLXbGz1F992axsbTp4HQBoQBlxjOfAoG1dMnVTDGFw4fAzx1J8Vj7NZGtzeZPBFttk9mm0u/xErsxhxwt0cv1P3Levbqj/ic1o/SwR/8ARlchrLcVsr5tplo4n9svVcr+6wzxtGvoW/ZnuzcwE1zYUAqYTGyLY6Vy0M0uSMJYSuYuhWZGQlbRSP2Tg9QhIGpyYHJZULFJQVsoB7SCAQciCjCo3hRFNGQZcQZW6zU8CXAOyIl0HtGHHM9+sk5rpPfdrs5qh1nYKBJY10y6HCBmDrrtkvSLRRlYL8UbRFBrD+oH3+XurdqE3rZUQ6pLZh7J0gpsJLWQeZ08kQOlpMBzAAcxuY4rD3h+xRN3yTJOWUCfklMuCE9nQxdRbWjV229KTxLsU7CPL8yAqVey8gANGW2bt9NtEwUHRiiCcmjfPIkeEqerZoDKY3Oft9UDSQfbZHaKUNYP7MR/2zVbaBkB3n0VzeThJ4QGjwn6qreyXR981qGZtA7KJMNAk8uf7LY3N0AtTs3ltIHPPtOjuGnip+gN0B9Q1XDstgjvHw/XwC9NqODcydM++Nk908tepHM6vP2tR/czNg/D+zMg1C+qeZhv/IWisl20aQHV0mN/1z8zmqK7+nllqZOJpn+4Zf8AQyWho2pjwCxwcOIIKFdU36mMypXgmLkijc5KsmiyIBCYCRoUrXJRSJ0RDBA63PbrB7x9ELaOkIYDLMREnC05mBJgKe32Jz4a3/ZxyAHzKfd9zspaNHzPeptme1DLvvXrabKhpPYXNnAYJE7GN9EYLT/a7xgKTstyaIUVesY4hX3MrsRzrcB+U+YTP5s39LvRCVHBCPcqdMvsRauvho/K7zCjF9U/zBzfCfZVZcoKtLEfZRWU8ZpqVVrxLXAjl95LyP8AFC24nkDQZ+cgeg9Vv6kMblkANfcryHppbMWJx3Ppt6ALGWt6QTDGm2Y60iXYRm45jdaro5dzGiS3PdxzPht4rIWYy+efpwC2V3DKR4wY89FjP3dqCdP29zLJ8YpiDsOAHtr6ydkEHS9z9miB8z8/FLVryYZmTw080Laa0DCPE8T9EqkxttEFqfiLW+J9/f2SWChjd35D7+9UlOkXEgb5LSXPZxTgnX1CYxw6ekK5sqxz3M1N13URRa1lQgakNgZ75q2u2xlk/EZjNxn3VJZxVAmlUBHci2Wmu7LG3uiF1JSS0jzd5O+nTPJ78p1bPXqsfTOFr3YXYSAWzLYdociEt333g7VOo+m7kcvovVLwvLAOrc0OMcAV5v0qs1NwllMNdOZAhJ1Xq0drHLcKv6Ftd34gWhph5bUb3AHzXLCWeg7FA9pXK9ItVR9Q2GzkgOfLRw38eCNxbDRMdVnLxTgIVGxZlK98BQOOUod1YqEJXndD16iVz4QdeoqIR1KihJSPKjLlksfK4PhRF6iqVwFCbIOklsLaBjchvgdQvHellpxODB3+sfJa3p70ihzaLDiIzIG3CVkKNkL3dZUyGwRcXT1kvfsYvMpjS8kN2WIRidk0eqs7FWc9+FrQRzAMBQw6q7AwZegHErR3fYm0mwNdzuSnM6jt7EhOcjh9+yGtZakQ3CByQBsmEkuMkK7r1IEqqe8FyS+2k3/qNt60h91VWmYGitKT81nLnf2n96vKLs0aJUrgW6m6q+S4o1HNMtMeysWW+fjZ4hUbKympWhFTEnLLqrZ2VQHcMlVWq4mOyJR132mQQe9OqVoSWVetnc6at4kVt33LSo5gSeJzK5SWi075xySLAbZ6ZZzL3Ip51XLkQoDtTzAChBXLlCEVYoOoVy5ZZZA8qMlcuUKArRVPFUnSy0vpWWpUpuLX5Q7U5kcVy5ajyjFeDA3XTDiXOzJzJJJJPEk6p14vOkrly7U/ic9l3d1INpswiJAJ5kjVHLly5kkz/l/BFadFT7+K5ctoW9wW6T/Ud97q9o6rlyzPgP1H5/wEEpocVy5aAFjdryTnwUtrecJzSrkrl/I6nS/7ZV2p5zzSLlyygzP/2Q==" 
                 style="width: 100%; height: 100%; object-fit: cover;">
        </div>
    </div>
    """)


    put_html("""
        <div style="
            display: flex;
            background-color: #f5f6fa;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 30px;
            overflow: hidden;
            font-family: 'Segoe UI', sans-serif;
        ">
            <div style="flex: 1;">
                <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUSEhMWFRUXFxcZFxgVGBYXFhcYFxUXFxcYGBgYHSggGBolHRoWITEhJSktLi4uGB8zODMtNygtLisBCgoKDg0OGxAQGy0lICYtLS0tLS0tLS0tLTUtLS0tLS0vLS0tLS0tLS0tLS8tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIARMAtwMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAFBgMEAAIHAQj/xAA/EAACAQIEAwcCAggFBAMBAAABAhEAAwQSITEFQVEGEyJhcYGRMqFCsQcUI1JiwdHwFZKisuEzcoLxJMLic//EABoBAAMBAQEBAAAAAAAAAAAAAAIDBAEABQb/xAAuEQACAgEEAgEDAgUFAAAAAAAAAQIRAxIhMUEEE1EiMmFx8IGRobHBFCNCUtH/2gAMAwEAAhEDEQA/AFDAY4roNqZcJg0IDuRtNKRhRNaLxBtp06VGo6xl0NuLxJyZQazC7AUIt3SQKJ8MugHU/NNgtGxnI0cItZYYb1c4hxdoyDSo8CZUmhuIUm4aV5U9EAorc91YiasFsuor3D2prb9XOavJU99mOG7gnETlApit3ZpU4XZgUZt3Kdg82UdnuKlFMJPfUc6xbwNDbluahNwrtVkfNvlGesOA16DQRMYalF49aL/WxukgdAWrKgw9+RrvUwarVJNWBR7WVlZWnGVlZNaG6K443rKgbFqN62XEqeYrjiWsrKyuOPlLHjSqNokGr10zXiYbnUkHpW4TLWGvHQem1dJwtuytn9mobMsAKMzEkc41mkPhmGlgAJJIAH2rsvA+F28JbUn/AKhEkn8M9B9potSkwo7G/BezJ7te9OUnUqN/fpRLEdlcOw0DKeqn8wdKrHibk75VG55n+/n0onheJIF8TH1MUUowntJWdUlwL+J7NNa8QbMvpBHma1weBk03WMSj/SZ/vzoLi8M1q7pqjyR/CdyK8/yvFUPrhwFGXTJVsBa3tivTcBGtVbmMVdzUS0phF13qhfuVrbx6vtrUGLbSjbT4NR739EMJcBFLwueKKM4RdK2CadnMKbbVEMVrXiXRtWNaBqyOWgKLX64Iqu2ONQXMOahyVTrk+zKReOLkb1GcTQ1yZrFmups4lvXJNU7hYbVYyazWO1bqceDasgXiN4CASKypUujpWULys7ScCtpUorVFqVFpcmANf6PsMGxYYxFtWfXkR9J+afRis7FmMD8I6eZ89R80kdglkYiNXa2QB0AIPydfimTEXCMiLuW1+J/mfkUEsmlUOxxsLKBrcbREGka+XuSdBVa27XDmIgcgdY/5q3iyAlu31M/5AP5moprtbsfGCqwxhrsQV5R70TvjvLcruNQPPpSk/FktEAmTziAB6k6CmHhOLRwXtt6gaj/3VScZxp/xJ8kGtwFfxrNIWh74FnPiJo7xRFW6xA3g+Wok1Xa90rw8sHGTXwcjfBYRba1BjsSK9diRVK9hztWwlXIRmFtF2mmbC4WFE0L4Th8u9HEaBVWJp9AsoYrwmo8JiyTV25ZmvEwgFasLbOsmFyRVdxrU2WtGSrYR0gkTWpqtdSKId2ah/VSTrXNnFFLnKpkWaufqorZUApUpmlM2hzrK3xFyDWVNKUrNo4JYw8iajuLrRPC25Sh+IOtPt2LQQ7OcSNi6DJCtAaDHPTWugWbgYnEDVDqnqYAHrvXKBqadOyWPzIMM55ll8zvv1kekUOWGpDcT3obu0GMFrITEhT9RhRJOpP8AKh3CuJNdMmMpEggEDfz1NHeJ4ZbhUsozACJAMGJ2NUVspbuIsSzH4gT/AGKFrssh9pW4hwUPcDRIEETMAiDOnOmTgb5YBII+BFCr+OOzKEQ75oYkaiAP6UEweKPftbslu7XLObkWE5RrJ018qoi6qSAcdSaZ06/gkcQw6eW21K/H8H+rgODKExry0nlyofxztRicPiAVh7QRc6EdVnMD0mrOF7aJiLbM1uLYENr4g+6iCCDsTPKDNPzeNHLF7boj0yg1+SPCLccTbAcdQf60Rw+Dhh3ly2GMeEuMwnlFI/FO3l0KVQAEkgQOXQA8/Olr/FbubeS05yZLGfw6bcvjlScXgQ7ClKjuNq0kwjqT0kH2PnUxtxXG8Hxnu1BbUZGUiSIzHUabg+vvT72M40Lq5WdixkZD9J10KzJED+Kmy8NR+0DVY0JUhIqFxFeWgal1NOjaPSk1IlqpUWtyao6BNSBUZuCocXegUJ/XoJ1pMsm+wSiGHeqt5qpf4iOtenEgjSkylYVEGKva17Xi2s/OsodLCRyjA3AtuDQbFtLGsGJ0qJzVPIlIksrTr2A4abl8HKCoHinYDmZ6ilPhOGLsBrE6kdK7BhcGuDwa5RDvkznc6tO/pRRjbt8I1EPaXj1tLqW0WRr3jTooUTMRqdqC41LrsrW7gQ/hYjMII6SJ3pa405CYlyRmM+EzqpJIM8iZHrFRYbjDpdsFiMjIAQDPhygzE6MpHxNdlxOtS5LcMtmvgcsNhryTmAZz+MfVquUjMSWyneOtb2bKYey2ZVQDWFAHkB8RWt3jLqpAykxpymkzGY29fYi42gnQbUrHkDcbKWL7Q3Dfukn8bET0P4fQdNoqa9jcmHS0p08Tn/zMx7LlFBLuEMuxHP8AMf8AFXEsZlynXafPmark04oZnS0RaW//AIUO9Okj+50/Op3xIUEvIiJgamR/6qNrWsnRQRP5/NRYrM2ipp6SaYslHnODJLfHyQENlSkzIJD/APkeY5xEUQw3acWyIAH8XiVo5gZSIHtQn/DLp/C0ekVInBb/AO4SPOu96+TPVL4Ow9h+03fqVZwyKAPEwLhhqZgTsRqYnzp4AiuA9jsNfw+JRwGTxBWPIodCD5V3O7iJVTtI/nFTZK+5Gyi+y33lQ3b1D7mJjnVPEcRA51NKbZyib8SxZpfv4rWpbvEAzx7UXtcHS4ozV0UFwL7X6lwV13OUSaLv2aB0BIFEuFcISyNNTzJooxsFsH4S3dTcVlMmVayi9b+TNR8yWqI4bDKQc2bbTLB18weUTtVCxpRjhIuM6i1OYERl3B9dh71s76ATHfsd2ct20F+8lyQwyKwULczRlIG8a86Z+PYgO3clgCyqU9VnQe2vtVbFWbtjDIGOa4FZjAEBjt6xrSpi8TcOLtkMJtW0FydpyjOfn+VNS1ao/Csox43Kmhe7ZXh3Y5Z84PIqykj4PxQW7dy28PcH1qq/YT/SpO0Um7cEyGOlHey/ZgX8PbNyYBIgHVtTAB6eflT1FKKDjcdVrqr/ACHruGR7Nu9bYZWA8M+IHmAOYrXB4Ifux/3Aflzojh8Op8FsAW0hZXn/AAqeQ8+dE7GDUasBA3nYf3yjU/ep1ijdgvLKqB2Kwdk2wDa9WQL/AFmkfi2GFvM1onL+IGcy7b8yOc0+8R7RW7RC9075tM2wHL6dDHzS1xTDKZZEYBlYZWJ0kRoTypraBWpirax4JXQeKdT5GJ+8V0HgPB7YQMVEnWudYXBD9at27gIUDY6HQ6Dz9a6bex/dW9CFEaQhdvZVqTNVpFGO63LGJwanlXuGww2gUv2O0N4sIGa2zFQXt5DI3GjEj3FEuK8TeymcISZAAAOpNBFKMg27Rb43Ya3aNxV0BUQBqSzBQB6k0UxXFMtu2jHxKsH15/GgoBwTiWLuJcu31hFtl1HhCBl1QNPimQDO3nVp2GIQC8Vt4nk34LnkxGkx+L5qv0uUbiRylTpmtzi8mJqni8VpM0L4hZe02W4pVuh/keY8xVN8V51NoNLQxXiB866BwDGygjX+VcvVpIroHZO14cwPtXSVVR3Q2pcqlxDFkDw1DjrjKNKH2rj3G2gda6U9qBUey1bxrxtPpWVZsWQBWUqpfJ2x86W3o5wTEgXbeYnJnUsASARIn7UvWhJotgrOoqySFJHc+G4xMTZW8SPCXFwMQNNZPp0rm3FGP/yLtvWdPUFwTB/e5Qa84WzEm2WItkHP0CqCZodjle1hywkm80aajKpmY9YHzTsSjob7bX9CnxZzWVVwAVMvl6xAPLxDTXUTJ+9dat2O6wqW10JAQeWYZnI840965l2RwhvYy0GG7DTaQJYk+wJrrbJmv2V/CFdyPUgL9qHI9I/ycvsm645o3s4cW7YAGpICjqx29uvlNK3EWbE3mtozG3bYqFUx3jj/AKl24donQLB+1NHGsXkF1+ViySP/AOlwH8lj5oF+jvD5bJY/U5JJ8zrSJz6Ewj2y3gOBgHxgegiKKYnhiOuWBU19oNVsTxa3aXM7QPc/AFdCa7CcX0cz7Y8NbD3bbEyMwCmDzP0k8qfOCvntj03oH2rvDGYa4FADKO8Rd2OTxanlMUO7N8RZrYVXjSgycWOxq0xusYO2bwBYsw8UdPOBuaJ8RwiPaYuuYKM0RJ0GsedLXC77AlDbCvvmLxn81aPsYohebELlVVV2Y5Ya4CqJrmc5dwIiJklh61uNO+AZ/qZ3qHBXzhiMzWiFJ2kwBM0lWe0FxHKYq2VI5IIBHUqdD6ii2Ixa4a01tD43aTGw10Ecp6VtfSzibeVh8aEHqp3WrvG+1PsQ8sI5Hatf1CuFxS4iyEa2Ws65WzEsh/e8X0xz5Gl1+CXRcZAJjZuTAiQR/elLGKXE4O8qi44Vf+mwJgiZ11geeldU/R72hGJm1fy97urDQOAfECOTfn80eaGuOpcoyS5nH7QFwXsw9xjnlQKcsJgWsAAaimUWANhVPHRIFeZli0rbFqVkTMCNTVRLoWrzWxFBMReVWApUpNchLctXsaZ2isq1bRSs15Wcm7HzfYeKv4O8cwociUUwSwRV8thMR54Namy4lR3jBPED9KjO8R6qKBcbvs7StthbVcoDNA05wANzPzRPGYs2UW1aYMxzqzCfC0gOFPXYT5Us45SBL6sdgdhPPU9PzFMSaSR6mDB6sTyy74Gr9HWAh7uKJSAO7WNWLES0TyCiJ569KecGv/yfS0g+TJpN7GJls2VghnW9cbNHiVmCWyPYN8+dNV66Ve+4GyAD/KIqfNL6iKKuwR23xuTAXG537v2LAD/StCuG9oe4w6jwKY5kk/AFBf0kcUm5Yw4PhtiW/wC6AB/9vmmDsvwyzdRWZRIGh6UidUmyjHwzfhXEr95wGOhEiFAAB99/KifHeA96igMd5PUjpNWbos4aIGpIUdZYwI6UQbGWwILCfWda2GnUbK6A3BezVu2JKqWClQY1AO/LU+tcy7x8Hi7lkyVRyPY+IR7EV0TH8RxGHuCSHtu0LsHEnQEc/Wlftpw3vLly+PqVEZo6FSB/tp8fqelipNwWpDNw/E271sQw853FTYnidvDWXuBwzkQg5lj5eW59K5Nh7sbGPSpxf5k/NFHDpfIuXkalQQuXGYyxk9eZPU+dW8HiShFDLWNXrVl2BEg066Jw/wARdLlgm4JyQ3nEw0exmPKq/CLvcOJdVZSPo1LAiVYR1X8qGi/KOh2ZGX5Uis4BjQ9pQqzcQacsy7ss7/xDbnRqe9lXiPd43wzvWExy3LS3B+IT0rS6oakjsjxY3LeVj9JB0nY+vt96be/gVJnVTcWBkwvFJxZ7etGDBpZv2W73U0yW8eG0oXj4majyJdHRdBCxahd6ytrAlQfIVlCsZh88d1O1FeHYbMyJOUsQJ6efr/OKrcLSRJorwexnxKLBIWXIH8IJ/OK9KtUqExVuifiHEbj3DkK27aArJAPhEknXmT050CxuJkEASTuSo0XkJ6nf2FNWPwyoha7kkeIqWTVz9Kc/P/LS7w22b+Kt2wMiZi7mQZCeIn409TVX5odnyanS4/f9x54BZy3EV2llspby/uBANPWc3+Xzpjxa+G6Y5p/WlTsxabvWuv4S7SF/dB2HsPyp0uAERyJtn50FebmX1G4+Dh3blmS9JElpgk7ZTrp7inTsHxLNhhG4od+k3hmZUYDZrmvScv8AOk7s5xh8K+mqndT/AHvWzx6sSS5GQyacjvhnSmxFw4gPcSQv0kmLaz+Nzy6DSmT/AA0GHe7aUGD+zXMfYn16UH7OcXtXoZWExtzHrTA+DkSGgeRqeD+UUzfwyriODWXc3UUyqqoLak5WLFjPWQPagli4jvjS/wBKoq+yQD+bfNF+L8WtYTDu2aWghB1Y6D7muXjixzYgSf2igH3IJNXxq1Ikl/1G3C9ncIw+kQRPsRIIYHaq3Eey/DwNb4tk7eMGPakq9jHyrbznIJAWTHXXyHSruCwaKRmmecK0j2n7VXKS+CVR/JvxTs4E1sXrd5f4TDD1BoVaxJTwtI9dKM2rCKxy/Sx1EHKPQESpolhkCOrAK6jWGAYTzkeY+486DTZtAEYwRNV+EXWVwUB35a89DXQ8JwbBY6R3Qttrram375ZilDtB2UvYJwD47bHw3APCfI/uttpXQW9MZGTg9Q2cGm1eV4ypcEwSAQD9YjfwmTR3H8SZQVPLpXOcDjWCrr4laQZIABEOMo6iK6LeZXVH08Qk89Rof5H3pPmYJetS+NivLl9umTW9FXCY0jWTVjEcSOkCoLgVapXsSK8tprYXQw2uP5ViNa9pNv4iKympP5N0oXeEsAtHuy1pTcu3G2Chf8xzH/Sh+aU8E5px7O2SbDxMsxGnKQqfkWNWwX1iMC1TSB3H8UrZQVEAFyPNhpy5Lk+9S9leC37ds48W1yMjC2pbKzAmM8RGXQxrrRPg3Zk42+3eEpaBl9ROUbIByJMj2NPPHWVVCqAAAAByAAgD0GlPm1HgZOMW6QncMNxntll7pZkBiQxYDeN49acLn0Fv4VP+ViaTrmLXOpJkqZJgbxA+Nab8O0qB1EfKn+YqLK7dm6NIC7S2BswlPHm/7Tl1+4PtXG+OYQ2rr2+anTzG4I9ort/Hrg/V7d3cAhX8wRkb7R8VyjtfYOZRPVfUDUfzo8bBnxYF4XxIow1I8wY+9NjdobgTS8+22mtI74NhtqPvXi4lgIn2NFLEpOzceWlQVxWMe6czszHMNzMDyqUW/uQPmh2Euz8/lTd2c4LdxTAKIt7sx20MeEczpHtW/aDWooYDCEeILMH3MHkKstfRZbumkkk5onfkWFda4fwJLaZVHudz1Jr3GcMtupVlBHpQ+2XwM9UDkVrihzEZZO3iA09SAKL2cR4YW1B5mAJ+/wB6Ycd2HssPBIPrSljeE38Ix3Kzof8AnrT4Zb2aEzxNbphfh2L7m6LiyvNk6HcERuproltEuILbxcFxSWDfSVO5PTfSuW4u2l22LglLijWdCYI5bEedHez+Ouqq3JklQiA6QFBAj3kk+dbkkkzsS1JoBcU4CLGKewrM4MOkTORpidI01EzyozxfE9zYtCSHBMq31ZWGhE7iViaabWFV7lpnHi7rKD1UHT4k1a4r2cXEqqnUpMeh/wCayeSTi49DXPZI5ja40TIJrVsYSZozxHsQ9uTrHKgx4a4kZT8VLUTU2yN8VJr2ormAYnY1ldSO3BNm2RFO3DcSVwiKDllrhJAknQqN9vq/002p+j1OdAu0fCVt3BYXMxRA2VQWMMScxjQD1o/EzKWT6k0qEYoapUwr2Bu5rFxyd7kf5UE/dmNW+N35GUCWPwBVns7aRcLayJlBEncHNMEn4qPG5dSBqdN+XxW54SnJtDYThF0ce4txRu/yamHA+Dua61wO5mVDXNO0WGRLkoNdSZPOSa6T2ZB7u2SIMAnylOYpM1SQxu9wZfuZsLiE/dZo9jIrn/asgC1PMD7CP5inS+8Ye63J7hI8/HSB2zu/tEXfIoU+p1P5x7UOB3IzKvpZSCdK3OGB+pQar4Enb8/5VMcaymPDHX/irCWmbrwWbdy5bEC3BYTyJ3HpXVv0c2IwyNtMx6AkD+dJnBWZ7GMUAH9isR/EWH21p+w+ENrD21W33hVQAJgTGpPSkZJb0ymENhoy6VVurSLiMbi7NyRaNsEScrllPllIMn+5pnXGN3HfN6nyjeh1dUHpa3L/AHVRX8OjqVdQwOhBpOPboTKpCzGa4SBPsKP8E493+hCGfxWzI96bGSAkmc0x5Fu5csLJGaBOv4tB7aU68G4Um/ehhIj+EAfT5DnSz2i4dOOugDw5gSegIWT81Jjb91bVnG4Q5lCKl5RvIJyswHKDE+QpidvdWLjF7tOh94jeAv4cNvlYSuxEr051e7N8ZktnOqswPpmigvBMfbxdq3eUZbtuYUqCrGBIPmY0NU+y2IDZxdnxXmDjVSMxfMOo/wDVbN72jYxWnS/3udHx1gOOoNDbPBF5gV52JxOa06M2Y27jJMzIBIB+1MeSkSwyk7EuWl0LV3gCE/SK8pkKV7S3hmb7WbUv8Y4dbW618L47qqrHqLc5f9x+1H5qpxSxnQ9RqP79KryU47C8bqSYGW3ltKo5D8zNDcQvOi2M0jyAofcXTeirY29znfaKyFcMBL65ZjLbA1NxuU6iJ568hTb2cvA4VWSW0gHmx1E6/wB60pduFJKRIWYgczyJ6mjuGvdzg7VtdGaF9J3PsNPc1HmdIphbIONutqyqDxLaWT0Z2MKPSfsK5rxhSzljqSWJ8/EaeO0GLHcEdXU+wkIPsPmlhcJnvZCwBChR5tAJH3Ndg2VhTV7HmH4UDbDW20O4IBjSom7PXC6gwZ+mNj6nlRXs9hWV/EIVTDk7BTpz33o3jeKYcXBYTN3RZZYfUDsSCd5FVIXIp9lmt4VryXiFzpoZ8PMZdt5P+qum4AA2gfIVzbj72jZOVIuIzkgmQFR1Gh6wAaOYnjLCxKnfLB3+pZ095+KnzbSsZj+pUMSYW0zbAx1q5isMDaKciD996WeDcQKpKLnPMkySeh6V7d7YGSvcuY0KkEbedDjlG9xk0+jyxwQAkI+k6ggNr7iifD+AW7LG4oAY7kaA+w0pTxXHCL/eDw5olOQPlTFZ46DbzNtBPsBJootaqByXpsX+0Vs2kv4savdfKg6IjQxjmT4ifICgnZXG93dbu5CvqokZTOpXXTefiqvGOJ4rGdy6AG3aUgKuhGaCSepgCteAmCyNoN8sa+1HN1wbjXTOo8P4ipPjRVPoAftV27hLdxhcUhXGs8m0gZuvrSDh8ZlIGb/Pp99qO4Hip0gr8j+tBHPXJksXwOXAuGCymikSZMbSd/Wjdi7POaVMLxhlHxHqSAB8xRw3f2oI5jX2jX86thkU1sQ5IOL3C1eV7NZXWgClaxAPOpc4oMlmrFhSNSdq8LBnk5KIxlDGP4iPmq14actd6nxTamop0617bMQh9urLCz3imMrrPpt80OfiM5RuEAjzJA/nPtTT2rwve4a5bB1I+/L8q5q0rJZhoOUnyips0LZTilSLWLxclSdZeQOpXRZ8pJJ9hVDH2D4Z1JY+pPX5ohwjAm5eViDEiJ/dGsCNqKW8Kv6yoInIsgfxNrr6UEHUlFDHG1uUxh3UqHJJaAZ22kE+dVOIkK43OaCCOc7CjHarw5EnVmGY9BIj+vxVPivDitlLg8Xi8JHqfjanxfYPFxohebneT+I3vtbM/cVb7McQL2VV9QDl9gRp6iR81X4MYZA42NxvmF/+1U8KTh7r2j9JaVMaA7g+kae1ZljqiFCk1XZ02/hCjF7XdgPlLq48LQIBBBBVgNJB+YFDscob/poFM6zfuFfiJPPSav2r1u/YUMY035ihmC4aqMWa8W5xsPzNTRfVDbVAbEcPt2yHvMbjEzqTHoBPhH3qW3dDJdjT9m0DkABt66k+1DO2nFVtsVUZn5eXSoL10jDoAczMg1Gxa4f/ANHTyqnDit6pE852tgXh8I9u1bdHZSxE68p0NEOF2HuOR3gzQdx/DI1HU6Uz2uD2xbwy3DmJUrA2lZifeg/DbDXMVcCjIFjQAZiUUeEdD18qa4RfIpTkqo0s8PxLMLbBc0DNmkZfUjepjw28pI8JiSN9QNyBExTYyqhFxiGdgoy8gRofWKiwSzie8f8AEO7X0O59JrX40HutgllnRr2ctBQHNzPH0qPpB666k/lT5wOyzHO/9+VA7dmzaaRblp110J6xyora443JIqCfkxwvRQmT1O2Mde0vrxlz+GspT87H8MyiRb1TW7kg+lK9nHnnRTh2NnTmZqXxl/uxObIL58R51q50On9fWvLh8RM86gxFzTXoa900rYoyDSDxbBgZ19Y+dP6U8YthHOT+X8qSu1rQsD8TH1jn+X3rGrCTosdmCIJnY5fTTn96J4fBEG5iJBzGB1RY8TRzoBgMQ2Qrm1I1JjMABsTv817j2zplJcKw3TTnIBPWpkmsllP3Rorcdxmdix11kD32+KlxGPRsNaUyp1kCSNzrS+bpJZCZgkSRBI6xVm8QVgfhIH2H9aoaQFtx2/QNJhs9vvLRJbu20P8A3htPZRUfHbCs7AHOyC0Tl+k23tgkj+IXM3nBFXOB4gBAHEBVyhhuJ6jnzrzBoqXGCsGzzBjkw8Y9NA3tWsBWyHA2bmUFCzLzynxL6r+L2r1muhjJdgOQBE+XlRzheBhyNmG8ae/mKN3sJp4j8afekuG9jPbtTOW3+EXrjtcYajWOQ5ID7xTERbuLaukZIKghTIbuVgsPMkqNKl7ZYxLdtbFnR7m8funf7A6+dUEulxk0i0gtiBuT47h035D2p8dkmxauTpBbCcWPdW8iwUuCSdWg/wBmq/ZtS2IclspY3GU6iSW208vyrOFW1AuLzyyJ6g6fnVvAcHVHXNiQCCNE9tNDW3bpG+tRVyC+MwyKUcvErlg8iOg85ry68le7EsYj/tBorxCxhktsHu5srAjTXX/ituFuoIyLKtvGhIA6nWqI7pMW57NLYh4xie6a0DHjzk9R9JE9N6mt40UD/SBiAr2XMINRrtJIn8hUODxAZfqEiOe87RXn+d42takt/wDAq9thj/xMCspea4ayvFfjyO1MKltRpU+GuFWB86pPc1hQT16Vob0GYoYbO+wgxfMSZ351XFyR1+1RHM65SCenlJ/KqGNd7SnMoAneRr9693Dl9kFJBI8xd8Zo2OtKVy/bxGKFt2ZAs5WWNSNTAbfaKm4zxIuCLRm4dJB26xyJ8q84DhbbqTeEMBAkQS3UeY8qoQSSezCV21hH7zvLq23K+HvFNu566aEelULWD0Pd3ZXyK6+xFWuM8PjIhYMEXnuJ1if60Bx+CRfEQIAnTQn4rtNh1KO5U43ZFlkLAZmzMGBkn8IX0makwnDi1nvF1lgInXMZJ9RANAcdjDdyKdkBAJ3gmdaO2Mfkt2rRE5czSNDJHXnvWPkVYYt24sIuoYl2b0UECorNrMhg68j0MGKvYJRdsXXVvEq5YbQjMQd6h4Hwa5clbZBM66nwjmSeYoXxyUQaUqaL/C8U7LazjRFKZhvofpbzB2PMGinE8ZkRp5DQ78t63s9igsxiW1AkZYUsNmjNS32nR7MWbrqTAMrJzLOVRrtJj4rdNi3S6B3Dz3ty5fcEhPCo31GpH2A9q2wCtOUSSAS0ayzan86cOAdn7a2UBDasSwldxtJPKhgYW3NhSS5JBW0ACeZm4elc+2FCdNAdsM4gZlQuQDJ1C5hO2xO1XwUFwAsC0gQJgQagwyFrrK0WyoOS2NdzGZjzMc6KcL4Ue9WNPENZnnWp27s77Y8dhTit2xcSXZh4+St0jpW/C7NvTurrGOQ9utWeJcIcW2kr/wBTrJ51TwPD3GqJBB3JjpT43sLuO+3QH/S3cF1bFqQjh2Pi/EuVQTp5kCl/BYiLyEHRQqt5wIo7+lW2gxeG8Slu6118I8Yyz6w1JvGyExDi2TBCnpqVBMeU0uTudAxrSdCAB1B0rKpdksUty1lO6xvXlfPeS548rimDQZw/GLcH8IJ0Gp8Ma/lNQXMbakyfDAI852pXZjlEk85kRAgR9jUYlhDEQRPQjYct9p1o/Vq/gdZ0vgJDpnZGy5oWBoYAGaTy1+1CONC3dciWUDQTBHrrR/hPEESxatrBy2156DSCWPrIjc1auIGEtBGhbrBkT9vsa9nBD044wj0jk/k57iuBga2yGPlo3rB3qpeTEIgLKWTXKrL9zImui8RxC2vBZVFbSWAHhB29TS/fslySSSTuSZP3rMmeMNqtlUcbnvwjmw4gwaLmYg89fvWmPMC4B+4D58iZ+a6Hd4arbgfFUb3ZhHYtLAka67iI2NAvKXaNlgfTOZcOALQ21EcW0OByCj/Vr+UU62uxmHX975q/huzeGXUoGP8AESdthB0is98QY4JLsEdiMMXLllmxAzk7Fhqqjn6+3WugW8UxA/Vjb0EFTosDlptWmB7m0gtqiqg3gAKDzqa+qOIOSPTX2ih1N7ocku0JPaLjmJ/WO5VrewLFCSQGPInnpV7tB2YbFYe148rqQTmkgrvBjoYNG7mCwudLjoha2ISBAA05c9evnU1/igJCquh9o9qoiuxc91VCM/Cb9hSGlxMhlJMdZG4pf4nxUJczDNm/yweetP2J4wA0eZB+ahxGCw2JH7RFJ6jQ/IrNW4GnYS+BcYdmNwgK2aCeUH+mtNuHxzowuOquqtrkYg67GOdeYfsrZt/RsdYOtFcPhbawroGUCJESB6GQ1amka02t2UsZx8PbgWrs5p0Zjp6yar4Xj+mUFbTTE3kc/wComKJ4vspctqLuHZbybwBlePITDfah2G4mgfu7wk7FLiifQg67VTBO6FvRptMXe2FkPihmWH7tAxE5WILQyzsCIoNewBLACSYiPIbUd7VHLilVHZrQH7MNPgzGWQE7jaPWpWtggOujAazoetReRKUW3ED/AInnCV7lYiNBm15zWVTccyZ3+fOsrzM2L3y1sGzXFYkkDTnBJ1AmIHXb8xWF9JcqAfpmdWiNh5zrVxcOoAB5a7DeY9JiPmo24YGGYmBOg5/UCQAOWm9OtGGWeL3bagqZLa6b5hzy/i6bcz1otwnj14KBdlrghCT9JTmhI0Jk7/wnrVG7bAMTO0kchtlHT06VKcNlAyCWBkydJJ0I6wIovc0zj1+M3kY5/wB4n1B0UE9dvirtrjegJADcl6+CZ8taovhiwGmxzQ3i03aQee1VmXV3A8OUKo1JBJEt5iQfnyoX9T2GrPJBi1xgQZIJ/wBOgmtr3F4gCCTt1PUx60OtAaeHXYAR4y0yPXnWz8PkAgFiCyzynUjTffn5+9Yl8hLyJFy5xeInQ8t6q/4q0jUmTEff8qzHYYtbKDPIDEgamQxzR6SfYmh9tpZjvJHhBiSIAH8IAj4PWslUdwv9S/gbl4nbW2HyhwyiVO+vSec6VUW5buB2S41srPgOo2nSdaBpZYlHDFWXYgeWwnUjYT/zVxL2hZlXPkAMfVmKAk+xFF7FQa8hUEf8Ol/2mJ8I/dEE/J0NTXMVYssO7DHNGplpNL2FUXW8TsUlRm03gnMOk6xVk3EdjbsW/pIGdj4oMmdf71FUYskdILypsCX8ZLtOgBP51fwXEVAgE0KxHD2Q5ZzAnwk5gMuU+KCJ9TyrXhtmcxnXLBnUCToJ/e2rJT32F+5jXa4noddQY1noDUd3jRB12jfrt/WhtuyxDmdFjl9U5SFjn51G+HOZjIQASOercvPf7eVLlldm+38Dn2U7TEBbTZcsrJYkFS3hMeUifevO0vFMNc8Xh+glXgGWkZVjZlIzE0r2MMqq0FSsLlJG4DScx8jsP5VSNsknMMwAPKcwjSPLUz6UyPmSS0pCJK3Ze4jdW8yMEAbuwD0Roj/blPzWhxwykKg00YnWZPLoaqXCBIlg0AsTsJ/3MeZ8q0t3SVJAHoBpOaRMelJlOTbORFirR+hT4dI57Aztr0rytxZgBjM7yfpM7gT56zzrKzTZxcZtAeZ1J+DU1jXLOupr2soTeixfOVbbDQydfQ6VZnUH+CfckCaysrJHHmK+j0zfnUIUaCNCqn3O/puaysoU+QWa4JAplRBzfyO3StrbFsMCxnVv94H5VlZRLj+f+DOy8+jKeZ5/FVruFQozRrlGuo/FH5VlZWPkI1VBlGmw0/yk/nVaw37T3J/0GsrK6X3r9EYZgkGU6c5953q+VEjQamDpuIG9eVlc/tORRx9wkiSeQ9jEgdNzUtvBp3L+EdfdQpB9Qayso19xyLONw6qhAEDuc3/l4tapBR4Ry7tT7kgk/LH5rysrOzSXG7e5HsCapE6OOQzfZzXlZQS5/l/Y4hs6DTkUjnEuQftpV3FjKbpXQwT7xMxXlZTY8r9/JjA4cyTPT+dZWVlauDmf/9k="
                     style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div style="flex: 1; padding: 30px;">
                <h2 style="color:#0a3d62;">Your New Smile Starts Here</h2>
                <p style="font-size:16px;">Experience dental care that’s all about comfort, confidence, and real results. Let’s make your smile shine — book your consultation today..</p>
            </div>
        </div>
    """)

    put_button("book now",onclick=lambda:show_booking_form())

    put_html("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f9f9f9;
            padding: 0;
            color: #333;
        }
        .contact-container {
            max-width: 800px;
            margin: auto;
            background-color: white;
            padding: 2em;

            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.05);
        }
        h1 {
            color: #0072CE;
            font-size: 2.5em;
        }
        p {
            font-size: 1.1em;
        }
        .info {
            margin-bottom: 1.5em;
        }
    </style>

    <div class="contact-container">
        <h1>Description</h1>
        <p class="info">
            this clinic is a structure like this:
        </p>
        <p>
            *The clinic is conveniently located on the first floor, ensuring easy access for all visitors. 
            Upon arrival, patients are welcomed into a spacious and thoughtfully designed waiting area that can comfortably accommodate up to 20 individuals. 
            For the convenience and comfort of all guests, the seating arrangement is organized to provide separate areas for men and women, in accordance with cultural considerations.



        </p>
        <p>
            *The clinic is staffed by a dedicated and professional team consisting of two highly trained members who are committed to delivering the highest standard of care. 
            Within the facility, there is a single, well-equipped treatment room that has been carefully designed to offer a calm, hygienic, and efficient environment for medical procedures and consultations.
        </p>  

        <p>
            *Every detail of the clinic reflects a commitment to quality, comfort, and patient-centered service

        </p>
    </div>
    """)




    put_html("""
    <div style="text-align:center;">
        <h2>📍 Find Us</h2>
        <p>We are located at: <strong>Coop el rahmane lot n 16 hai khemisti bir el djir - ORAN</strong>Coop el rahmane lot n 16 hai khemisti bir el djir - ORAN</p>
        <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d640.9918604663586!2d-0.5740993797151686!3d35.73370127348192!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd7e63002a7708ed%3A0xce06573e3044ec7!2sCabinet%20dentaire%20dr%20benmahammed.%20F!5e1!3m2!1sfr!2sdz!4v1752688468924!5m2!1sfr!2sdz" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
    """)


    put_html("""
    <div style="text-align:center; margin-top:20px;">
        <h3>📱 Follow Us on Social Media</h3>
        <div style="display:inline-block; margin:10px;">
            <a href="https://www.facebook.com/brush_dental*" target="_blank" style="text-decoration:none;">
                <img src="https://simpleicons.org/icons/facebook.svg" alt="Facebook" width="40" style="vertical-align:middle;">
                <span style="margin-left:8px; vertical-align:middle; font-family:'Segoe UI',sans-serif;">Facebook</span>
            </a>
        </div>
        <div style="display:inline-block; margin:10px;">
            <a href="https://www.instagram.com/brush__dental" target="_blank" style="text-decoration:none;">
                <img src="https://simpleicons.org/icons/instagram.svg" alt="Instagram" width="40" style="vertical-align:middle;">
                <span style="margin-left:8px; vertical-align:middle; font-family:'Segoe UI',sans-serif;">Instagram</span>
            </a>
        </div>
        
    </div>
    """)

    put_html('''
    <div style="text-align:center; margin-top: 20px;">
      
      

      <!-- Google AdSense Code -->
      <ins class="adsbygoogle"
           style="display:block"
           data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
           data-ad-slot="XXXXXXXXXX"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
      <script>
           (adsbygoogle = window.adsbygoogle || []).push({});
      </script>
    </div>
    ''')

    put_html("</div>")

    # Listen for custom event to show booking form (JS -> PyWebIO)
    event = pin_wait_change('custom_event', timeout=None)
    if event and event['event'] == 'show_booking':
        show_booking_form()
        App()  # Go back to main menu after booking

# Flask and PyWebIO integration
app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>brush_detal</title>
    <link rel="icon" href="/favicon.png" type="image/png" />
</head>
<body>
    <script>window.location.href = "/app";</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/favicon.png')
def favicon():
    return send_file('favicon.png')

def main():
    App()

app.add_url_rule('/app', 'webio_view', webio_view(main), methods=['GET', 'POST'])


