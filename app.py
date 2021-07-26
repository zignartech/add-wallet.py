from mqtt import publish
from price import price_miota
from basic import account_manager
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import datetime
import iota_wallet as iw



app = Flask(__name__)
CORS(app)

topicPub = 'v1/devices/iota/task'

@app.route('/balance')
def getBalance():
    try:
        precio = price_miota()
        cuenta_val = account_manager("CuentaR")
        print("Total balance:")
        valor = cuenta_val.balance()

        return jsonify({
            "error": False,
            "data": {
                "balance": valor['total']/1000000,
                "usd": round(precio*(valor['total']/1000000), 2),
                "conversion": round(precio, 2)
            }
        })
    except:
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })


# @app.route('/transactions/last')
# def lastTransfer():
#    cuenta_val = account_manager("Cesar")
#    ac = cuenta_val.list_messages()
#    return jsonify({"message": ac[-1]['id'], "confirmation status": ac[-1]['confirmed'],
#                    "value": ac[-1]['payload']['transaction'][0]['essence']['regular']['value']})

@app.route('/address')
def listAddress():
    try:
        cuenta_val = account_manager("CuentaR")
        last_address_obj = cuenta_val.latest_address()
        return jsonify({
            "error": False,
            "Last address": last_address_obj['address']['inner']
        })
    except:
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })

@app.route('/transactions', methods=['GET'])
def listTransfers():
    try:
        cuenta_val = account_manager("CuentaR")
        list_t = []
        status = request.args.get('status')
        transactions = None 
        
        if(status is None):
            transactions = cuenta_val.list_messages()
        else:
            if not (status == 'Received' or status == 'Sent'):
                abort(404)
            transactions = cuenta_val.list_messages(message_type=status)
        
        for ac in reversed(transactions):
            list_t.append({
                "id":f"{ac['id']}",
                "amount": ac['payload']['transaction'][0]['essence']['regular']['value']/1000000,
                "date": ac['timestamp'],
                "status": ac['payload']['transaction'][0]['essence']['regular']['incoming']
            })

        #resultado = [count for count in reversed(list_t)]
        if len(list_t)<10:
            lista = list_t
        else:
            lista = list_t[0:10]

        return jsonify({
            "error": False,
            "transactions": lista
        })

    except Exception as e:
        print(e)
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })
 
@app.route('/send-tokens', methods=['POST'])
def sendTokens():
    try:
        cuenta_val = account_manager("CuentaR")
        valor = cuenta_val.balance()
        #print(valor['total'])
        if valor['total'] < int(request.json['cost']):
            return jsonify({
            "error": True,
            "message": "Not enough IOTAS"
            })
        prueba = [task['name'] for task in request.json['rover']['tasks']]
        timestamp = datetime.datetime.fromtimestamp(int(request.json['date']))
        transfer = iw.Transfer(
            amount=int('{0:_}'.format(int(request.json['cost']))),
            # Direccion de la cuenta de CuentaZ
            address='atoi1qrjj505wfzqt2n2wzpxe5vkjlktv3uvkemun8cz4eyc5utun26dlkvc6hek',
            # Direccion de la cuenta de CuentaR
            # address='atoi1qz7xrvchj6kjhk5p7wndlw2aj50wesqhaezc2npzvvch4csvwzz3j8mqdyk',
            remainder_value_strategy='ReuseAddress',
            indexation={
                'index': "Zignar Technologies".encode(),
                #'data': f"{request.json}".encode()
                'data': f"""Device: {request.json['rover']['name']}
task: {prueba}
location:  {request.json['rover']['location']}
cost: {request.json['cost']}
reference: {request.json['reference']}
farm_sections_involved: {request.json['farm_sections_involved']}
banner: {request.json['banner']}
date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}""".encode()
            }
        )

        node_response = cuenta_val.transfer(transfer)
        #on_confirmation_state_change(callback)
        print(f"mensaje: {request.json}\n")
        print(node_response)

        publish(topicPub, f"{request.json}", 0)

        return jsonify({
            "error": False,
            "link": f"{node_response['id']}"
        })
        
    except Exception as e:
        print(e)
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })

@app.route('/return-tokens')
def returnTokens():
    try:
        cuenta_val = account_manager("CuentaZ")
        valor = cuenta_val.balance()
        #print(valor['total'])
        if valor['total'] == 0:
            return jsonify({
            "error": False,
            "message": "Not enough IOTAS"
            })
        transfer = iw.Transfer(
            amount=int('{0:_}'.format(int(valor['total']))),
            address='atoi1qz7xrvchj6kjhk5p7wndlw2aj50wesqhaezc2npzvvch4csvwzz3j8mqdyk',
            remainder_value_strategy='ReuseAddress',
        )

        node_response = cuenta_val.transfer(transfer)
        #status_transfer = transfer.on_transfer_progress(node_response)
        # print(f"mensaje: {request.json}\n")

        return jsonify({
            "error": False,
            "link": f"{node_response['id']}"
        })
        
    except Exception as e:
        print(e)
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })

@app.route('/prueba', methods=['POST'])
def prueba():
    prueba = [task['name'] for task in request.json['rover']['tasks']]
    timestamp = datetime.datetime.fromtimestamp(int(request.json['date']))
        #print(task['name'])
    #print(prueba)
    #print({f"deviceId: {request.json['rover']['name']}, task: {prueba}"})
    print(f"""Device: {request.json['rover']['name']}
task: {prueba}
location:  {request.json['rover']['location']}
cost: {request.json['cost']}
reference: {request.json['reference']}
farm_sections_involved: {request.json['farm_sections_involved']}
banner: {request.json['banner']}
date: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}""")
    return "aea"

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    #host="0.0.0.0"
