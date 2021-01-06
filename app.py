#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Chave do cesto de compras: user
# {
#     "user_teste":{
            # "produtos":{
            #     "coca-cola":{
            #                 "qtd":5
            #                 "valor" 1.0:
            #     }
            # }
#       }
# }

basket = {
    
}

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Prova Técnica Market4U</h1>
    <h2>Por: João Pedro Santos Rodrigues</h2>'''


def get_basket(user):
    retorno = {}
    print(basket)
    if user in basket.keys():
        return basket[user]
    else:
        return {"Message":"user nao existe"}

def add_product(user, count, product, price):
    print("adding user: {}".format(user))
    if user in basket.keys():
        if product in basket[user].keys():
            basket[user][product]['price'] = price
            count_items = basket[user][product]['count']
            basket[user][product]['count'] = count_items + count
            
        else:
            print("Produto ainda não existe com este user. Adicionando...")
            basket[user] = {}
            basket[user][product]= {"price":price, "count":count}
    else:
        print("Produto ainda não existe com este user. Adicionando...")
        basket[user] = {}
        basket[user][product]= {"price":price, "count":count}
        
  
    return basket[user]

def remove_product(user, count, product):
    if product in basket[user].keys():
        count_items = basket[user][product]['count']
        basket[user][product]['count'] = count_items - count
        
        if basket[user][product]['count'] <=0:
            del basket[user][product]

    return basket[user]

def process_payload(payload_json):
    error_list = []
    for item in payload_json:
        if 'user' in item.keys() and 'type' in item.keys() and 'product' in item.keys() and 'count' in item.keys(): 
            user = item['user']
            count = item['count']
            product = item['product']
            type = item['type']
        
            if type == 'add':
            
                if float(item["price"]) > 0:
                    price = item['price']
                    add_product(user, count, product, price)
                else:
                    error_list.append(item)
                    #return jsonify({"Message":"Produto sem preco!"})

            elif type == 'remove':
                remove_product(user, count, product)
            else:
                error_list.append(item)

        else:
            error_list.append(item)
            # return jsonify({"Message":"Erro na requisicao"})
    return {"error_list":error_list}

@app.route('/basket/events', methods=['GET', 'POST'])
def events():

    #Processar Payload
    if request.method == 'POST':
        
        payload_json = request.get_json()
        error_list = process_payload(payload_json)
        return error_list
        

    #Retornar cesto de compra
    elif request.method == 'GET':
        if 'user' in request.args:
            user = str(request.args['user'])
            return get_basket(user)
            
        else:
            return jsonify({"Message":"Erro na requisicao"})
    else:
        return jsonify({"Message":"Erro no metodo"})

    return jsonify({"Message":"Erro geral"})
    
  

app.run(port=8000)