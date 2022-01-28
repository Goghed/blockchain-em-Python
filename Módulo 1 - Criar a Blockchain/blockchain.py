import datetime
import hashlib
import json
from flask import Flask, jsonify

# criando classe para criar um blockchain

class Blockchain:

    #criando função para criar a blockchain
    def __init__(self):

        #criando uma lista
        self.chain = []
        #criando um bloco
        self.create_block(proof=1, previous_hash='0')

    #criando função para criaçao dos blocos
    def create_block(self, proof, previous_hash):

        #criando um dicionário para armazenar as informações em forma de bloco
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}

        #adicionando o bloco na blockchain
        self.chain.append(block)
        #pedindo para retornar os blocos
        return block

    #criando função para pega o bloco anterior
    def get_previous_block(self):

        #para pega o bloco anterior, pega o objeto atual e faz a subtração com -1
        return self.chain[-1]

    #criando a função do proof of work
    def proof_of_work(self, previous_proof):

        #variavel para iniciar o quebra-cabeça
        new_proof = 1
        #varivavel para controlar o laço
        check_proof = False

        #repetição para achar se foi decifrado o quebra-cabeça
        while check_proof is False:

            #gerando o hash
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            #condição para verificar se o hash começa com 0000
            if hash_operation[:4] == '0000':

                #mudando o valor da variavel para True
                check_proof = True

            #Senão precisa continuar
            else:

                #mudando o valor do proof se não conseguir achar o hash correto para continuar procurando
                new_proof += 1

        #retorna o valor do proof
        return new_proof

    #criando a função hash para estruturar melhor o código
    def hash(self, block):

        #gerando um arquivo json do bloco para gerar o hash
        encoded_block = json.dumps(block, sort_keys=True).encode()

        #retornando o hash 256 desse arquivo json
        return hashlib.sha256(encoded_block).hexdigest()

    #criando função para validar a cadeia da bockchain
    def is_chain_valid(self, chain):

        #colocando o valor inicial do bloco anterior
        previous_block = chain[0]
        #colocando o valor do bloco atual
        block_index = 1

        #criando a repetição para correr toda a blockchain
        while block_index < len(chain):

            #colocando o valor do bloco como valor atual
            block = chain[block_index]

            #verificar se o hash do bloco atual é igual ao bloco anterior
            if block['previous_hash'] != self.hash(previous_block):

                #retorna False pq a verificação falhou
                return False

            #prova anterior recebendo o valor proof do bloco anterior
            previous_proof = previous_block['proof']

            #a prova recebendo o valor proof do bloco atual
            proof = block['proof']

            #gerando o hash dos 2 blocos
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()

            #condição para verificar os 4 primeiros digitos do hash
            if hash_operation[:4] != '0000':
                return False

            #atualizando o valor do bloco anterior
            bloco_anterior = block

            #para atualizar o indice do bloco atual
            block_index += 1
        return True

#iniciando a nossa aplicação apartir daqui
app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

#atribuindo a variavel blockchain a sua função Blockchain
blockchain = Blockchain()

#criando a função para minerar o bloco
@app.route('/mine_block', methods = ['GET'])
def mine_block():

    #pegando o valor do bloco anterior com o metodo da classe criada
    previous_block = blockchain.get_previous_block()

    #pegar o proof desse bloco
    previous_proof = previous_block['proof']

    #
    proof = blockchain.proof_of_work(previous_proof)

    #precisamos do hash anterior
    previous_hash = blockchain.hash(previous_block)

    #criação do bloco
    block = blockchain.create_block(proof, previous_hash)

    #exibir o resultado da blockchain
    response = {'message': 'Parabens voce acabou de minerar um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain():

    response= {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5000)

