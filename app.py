from mqtt import publish
from price import price_miota
from basic import account_manager
from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
import datetime
import iota_wallet as iw
import iota_client as ic



app = Flask(__name__)
CORS(app)

topicPub1 = 'v1/devices/wallet/send'
topicPub2 = 'v1/devices/wallet/demo'

@app.route('/certificate', methods=['POST'])
def certificate():
    try:
        client = ic.Client(local_pow=False)
        some_utf_data = f"{request.json['hola']}".encode("utf8")
        message = client.message(
            index="Zignar Technologies", data=some_utf_data
        )
        print(message)

        return jsonify({
            "error": False,
            "message_id": message['message_id']
        })
    except:
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })


@app.route('/balance')
def getBalance():
    try:
        precio = price_miota()
        cuenta_val = account_manager("CuentaR")
        
        print('Syncing...')
        synced = cuenta_val.sync().execute()
        
        print("Total balance:")
        valor = cuenta_val.balance()

        return jsonify({
            "error": False,
            "data": {
                "balance": valor['total']/1000000,
                "conversion": round(precio, 2)
            }
        })
    except:
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })

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
            synced = cuenta_val.sync().execute()
            transactions = cuenta_val.list_messages()
        else:
            if not (status == 'Received' or status == 'Sent'):
                abort(404)
            transactions = cuenta_val.list_messages(message_type=status)
            
        for ac in reversed(transactions):
            list_t.append({
                "id":f"{ac['id']}",
                "amount": ac['payload']['transaction'][0]['essence']['regular']['value']/1000000,
                "date": ac['timestamp']*1000,
                "status": ac['payload']['transaction'][0]['essence']['regular']['incoming']
            })

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
        print(f"mensaje: {request.json}\n")
        cuenta_val = account_manager("CuentaR")
        synced = cuenta_val.sync().execute()
        valor = cuenta_val.balance()

        if valor['total'] < int(request.json['cost']):
            return jsonify({
            "error": True,
            "message": "Not enough IOTAS"
            })

        #prueba = [task['name'] for task in request.json['rover']['tasks']]
        #timestamp = datetime.datetime.fromtimestamp(int(request.json['dateUTC']))
        
        transfer = iw.Transfer(
            amount=int('{0:_}'.format(int(request.json['cost']))),
            # Direccion de la cuenta en C
            #address='atoi1qzn7wgchlh9eh4gn6h2gvv3j8nagpuvaxpvx9qal5wp6mwz74r44zl3lkz7',
            # Direccion de la cuenta de CuentaZ
            address='atoi1qrjj505wfzqt2n2wzpxe5vkjlktv3uvkemun8cz4eyc5utun26dlkvc6hek',
            # Direccion de la cuenta de CuentaR
            # address='atoi1qz7xrvchj6kjhk5p7wndlw2aj50wesqhaezc2npzvvch4csvwzz3j8mqdyk',
            remainder_value_strategy='ReuseAddress',
            indexation={
                'index': "Zignar Technologies".encode(),
                #'data': f"{request.json}".encode()
                'data': f"""Device: {request.json['rover']['name']}
task: {request.json['rover']['tasks']}
location:  {request.json['rover']['location']}
cost: {request.json['cost']}
reference: {request.json['reference']}
farm_sections_involved: {request.json['farm_sections_involved']}
banner: {request.json['banner']}
dateGMT: {request.json['dateGMT']}""".encode()
            }
        )

        node_response = cuenta_val.transfer(transfer)
        print(f"mensaje: {request.json}\n")
        print(node_response)

        if request.json['mode'] == "send":
            publish(topicPub1, f"Task: {request.json['rover']['tasks']}", 0)
            print("\nsend")
        else:
            publish(topicPub2, f"Task: {request.json['rover']['tasks']}", 0)  
            print("\ndemo")  

        valor2 = valor['total'] - node_response['payload']['transaction'][0]['essence']['regular']['value']

        return jsonify({
            "error": False,
            "link": f"{node_response['id']}",
            "balance": valor2/1000000
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
        cuenta_val2 = account_manager("CuentaR")

        synced = cuenta_val.sync().execute()
        synced2 = cuenta_val2.sync().execute()
        valor = cuenta_val.balance()

        valor2 = cuenta_val2.balance()
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

        balance_final = valor['total'] + valor2['total']

        return jsonify({
            "error": False,
            "link": f"{node_response['id']}",
            "balance": balance_final/1000000
        })
        
    except Exception as e:
        print(e)
        return jsonify({
            "error": True,
            "message": "An error has occurred"
        })


if __name__ == '__main__':
    app.run(debug=False, port=4000, host="0.0.0.0")
#     #host="0.0.0.0"
