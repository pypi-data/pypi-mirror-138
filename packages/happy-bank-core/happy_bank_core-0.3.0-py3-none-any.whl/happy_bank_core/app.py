"""
Runs happy bank core app.

Represents REST Api layer.
"""

from flask import Flask

api = Flask(__name__)


@api.route("/health")
def health():
    """Returns health status"""
    return "Happy Bank Core app is up and running.", 200


@api.route("/transfer/<sender>/<receiver>/<amount>")
def transfer(sender, receiver, amount):
    """Ensures transfer between 2 accounts of given money"""
    return f"{sender} -> {receiver} ({amount})", 200


def main():
    """Main method to run code as a module"""
    api.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
