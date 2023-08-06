# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
# from external import configure
from temp import Client


# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.

# kable = configure({
#     "environment": "TEST",
#     "clientId": "stripe",
#     "clientSecret": "sk_test.SDfZPCLp.8SAR7H2asLE8uMXgBNf8AAf9UGiE8zAt",
#     "baseUrl": "someUrl"
# })

# kable = configure({
#     "client_id": 'kci_75bfe76dea214218be408fe6fa241f07',
#     "client_secret": 'sk_test.jjrhHXZL.XdSSvBt22dKQdmMvjpiQ9F9v1DGtw26h',
#     "environment": 'TEST',
#     "base_url": 'https://something.com'
# })


@app.route('/')
@Client.get
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run()
