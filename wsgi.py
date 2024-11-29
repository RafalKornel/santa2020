from santa import app

if __name__ == "__main__":
    app.run(ssl_context=('fullchain.pem', 'privkey.pem'))