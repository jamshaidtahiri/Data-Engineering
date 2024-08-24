from app import app, db, Client
from werkzeug.security import gen_salt

def register_client():
    client_id = gen_salt(40)
    client_secret = gen_salt(50)
    client = Client(
        client_id=client_id,
        client_secret=client_secret,
        client_type='confidential',  # or 'public' depending on your use case
        redirect_uris='http://localhost:8000/callback',
        default_scope='email',
    )
    db.session.add(client)
    db.session.commit()

    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")

if __name__ == '__main__':
    with app.app_context():  # Correctly use the app context here
        register_client()
