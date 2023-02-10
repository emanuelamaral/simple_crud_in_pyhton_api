from flask import Flask, make_response, jsonify, request
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mysql',
    database='loja_carros'
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/carros', methods=['GET'])
def get_carros():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM tb_carros')
    meus_carros = my_cursor.fetchall()

    carros = list()
    for carro in meus_carros:
        carros.append(
            {
                'id': carro[0],
                'marca': carro[1],
                'modelo': carro[2],
                'ano': carro[3]
            }
        )

    return make_response(jsonify(
        mensagem='Lista de carros',
        dados=carros
    ))


@app.route('/carros/<int:id_carro>', methods=['GET'])
def get_carros_by_id(id_carro):
    my_cursor = mydb.cursor()

    sql = f"SELECT * FROM tb_carros c WHERE c.id = {id_carro}"

    my_cursor.execute(sql)
    carro = my_cursor.fetchone()

    carro_by_id = list()
    carro_by_id.append(
        {
            "id": carro[0],
            "marca": carro[1],
            "modelo": carro[2],
            "ano": carro[3]
        }
    )

    return make_response(jsonify(
        mensagem='Carro pesquisado por id:',
        dado=carro_by_id
    ))


@app.route('/carros', methods=['POST'])
def create_carro():
    carro = request.json

    my_cursor = mydb.cursor()

    sql = "INSERT INTO tb_carros (marca, modelo, ano) " \
          f"VALUES ('{carro['marca']}', '{carro['modelo']}', '{carro['ano']}')"

    my_cursor.execute(sql)

    mydb.commit()

    return make_response(jsonify(
        mensagem='Carro cadastrado com sucesso',
        carro=carro
    ))


@app.route('/carros/<int:id_carro>', methods=['DELETE'])
def delete_carro(id_carro):
    my_cursor = mydb.cursor()

    sql_select = f"SELECT * FROM tb_carros c WHERE c.id = {id_carro}"
    my_cursor.execute(sql_select)
    carro_deletado = my_cursor.fetchone()

    carro_delete = list()
    carro_delete.append(
        {
            "id": carro_deletado[0],
            "marca": carro_deletado[1],
            "modelo": carro_deletado[2],
            "ano": carro_deletado[3]
        }
    )

    sql_delete = f"DELETE FROM tb_carros  WHERE id = {id_carro}"
    my_cursor.execute(sql_delete)

    return make_response(jsonify(
        mensagem="Carro deletado:",
        carro=carro_delete
    ))


@app.route('/carros/<int:id_carro>', methods=['PUT'])
def update_carro(id_carro):
    carro = request.json

    my_cursor = mydb.cursor()

    sql = "UPDATE tb_carros SET " \
          f"   marca = '{carro['marca']}'," \
          f"  modelo = '{carro['modelo']}'," \
          f"     ano = '{carro['ano']}'" \
          f"WHERE id = {id_carro} "

    my_cursor.execute(sql)

    sql = f"SELECT * FROM tb_carros c WHERE c.id = {id_carro}"

    my_cursor.execute(sql)
    carro = my_cursor.fetchone()

    carro_atualizado = list()
    carro_atualizado.append(
        {
            "id": carro[0],
            "marca": carro[1],
            "modelo": carro[2],
            "ano": carro[3]
        }
    )

    return make_response(jsonify(
        mensagem="Carro atualizado:",
        carro=carro_atualizado
    ))


app.run()
