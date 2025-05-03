from flask import Flask, render_template, request, redirect, url_for
from web3 import Web3
import json

app = Flask(__name__)

# Connect to Ganache local blockchain
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load ABI from Truffle build output
with open("../build/contracts/RideChain.json") as f:
    abi = json.load(f)['abi']

# Replace with your actual deployed contract address
contract_address = "0xD22631C4c303A5B05aAC464e6E7334edc3887c42"

# Instantiate the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Default account (use any available account from Ganache)
default_account = web3.eth.accounts[0]

@app.route("/")
def index():
    return render_template("index.html", account=default_account)

@app.route("/offer", methods=["GET", "POST"])
def offer_ride():
    if request.method == "POST":
        origin = request.form["origin"]
        destination = request.form["destination"]
        fare = int(request.form["fare"])
        tx_hash = contract.functions.offerRide(origin, destination, fare).transact({
            "from": default_account
        })
        web3.eth.wait_for_transaction_receipt(tx_hash)
        return redirect(url_for("index"))
    return render_template("offer_ride.html", account=default_account)

@app.route("/rides")
def rides():
    count = contract.functions.rideCount().call()
    ride_list = []
    for i in range(1, count + 1):
        ride = contract.functions.getRide(i).call()
        ride_list.append(ride)
    return render_template("rides.html", rides=ride_list, account=default_account)

@app.route("/book/<int:ride_id>")
def book_ride(ride_id):
    ride = contract.functions.getRide(ride_id).call()
    fare = ride[4]
    tx_hash = contract.functions.bookRide(ride_id).transact({
        "from": web3.eth.accounts[1],
        "value": fare
    })
    web3.eth.wait_for_transaction_receipt(tx_hash)
    return redirect(url_for("rides"))

@app.route("/history")
def history():
    account = request.args.get("account")  # Get the account from URL parameters
    
    # Convert the account address to checksum format
    account = Web3.to_checksum_address(account)

    # Fetch rides for the user (driver or passenger)
    rides = contract.functions.getUserRides(account).call()  
    
    return render_template("history.html", rides=rides, account=account)

if __name__ == "__main__":
    app.run(debug=True)
