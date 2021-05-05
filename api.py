from flasgger import swag_from
from datetime import datetime
from create_base import *
import logging



#region Clients

@app.route('/clients', methods=['GET'])
@swag_from('docs-swagger/clients.yml')
def get_client():
    app.logger.info('Processing default request')
    '''Fonctions pour afficher tous les clients'''
    return jsonify({'clients': Client.getall_client()})


# route pour client par id
@app.route('/client/<int:id>', methods=['GET'])
def get_client_by_id(id):
    return_value = Client.get_client(id)
    return jsonify(return_value)


# route pour ajouter un client
@app.route('/client', methods=['POST'])
def add_client():
    '''Fonction pour ajouter un client dans la base de donnée'''
    request_data = request.get_json()  # getting data from client
    for data in request_data:
        nom = request_data['nom']
        prenom = request_data['prenom']
        Client.add_client(prenom, nom)
        response = Response("Client ajouté", 201, mimetype='application/json')
        return response
    return Response("Erreur API: Lecture des données client impossible", 500)


# route pour modifier un client par POST methode
@app.route('/client/<int:id>', methods=['PUT'])
def update_client(id):
    '''Fonction pour modifier un client dans la base de donnée'''
    request_data = request.get_json()
    Client.update_client(id, request_data['nom'],request_data['prenom'])
    response = Response("Mis à jour client :"+ str(id),status=200, mimetype='application/json')
    return response


# route pour supprimer un client par méthode DELETE
@app.route('/client/<int:id>', methods=['DELETE'])
def remove_client(id):
    '''Fonction pour supprimer un client de la base de donnée'''
    Client.delete_client(id)
    response = Response("Client supprimé :" + id, status=200, mimetype='application/json')
    return response



#endregion

#region Collaborateurs

# route pour voir tous les collaborateurs
@app.route('/collaborateurs', methods=['GET'])
@swag_from('docs-swagger/collaborateurs.yml')
def get_collaborateur():
    '''Fonction pourvoir tous les collaborareurs de la base de donnée'''
    return jsonify({'Collaborateurs': Collaborateur.getall_collab()})


# route pour voir un collaborateur par son id
@app.route('/collaborateur/<int:id>', methods=['GET'])
def get_collaborateur_by_id(id):
    return_value = Collaborateur.get_collab(id)
    return jsonify(return_value)


# route pour ajouter un nouveau collaborateur
@app.route('/collaborateur', methods=['POST'])
def add_collaborateur():
    '''Fonction pour ajouter un collaborateur dans la base de donnée'''
    request_data = request.get_json()  # getting data from client
    Collaborateur.add_collab(request_data["id"], request_data["nom"], request_data["prenom"])
    response = Response("Collaborateur ajouté", 201, mimetype='application/json')
    return response


# route pour modifier un collaborateur par méthode POST
@app.route('/collaborateur/<int:id>', methods=['PUT'])
def update_collaborateur(id):
    '''Fonction pour modifier un collaborateur dans la base de donnée'''
    request_data = request.get_json()
    Collaborateur.update_collab(id, request_data['id'], request_data['nom'], request_data['prenom'])
    response = Response("Collaborateur Updated", status=200, mimetype='application/json')
    return response


# route pour supprimer un collaborateur par méthode DELETE
@app.route('/collaborateur/<int:id>', methods=['DELETE'])
def remove_collaborateur(id):
    '''Fonction pour supprimer un collaborateur de la base de donnée'''
    Collaborateur.delete_collab(id)
    response = Response("Collaborateur supprimé", status=200, mimetype='application/json')
    return response


#endregion

#region Categories

@app.route('/categories', methods=['GET'])
@swag_from('docs-swagger/categories.yml')
def get_categories():
    '''Fonction pour voir toutes les categories de la base de donnée'''
    return jsonify({'Categories': Categorie.getall_categorie()})

@app.route('/categorie/<int:id>', methods=['GET'])
def get_categorie(id):
    return_value = Categorie.get_categorie(id)
    return jsonify(return_value)

#endregion

#region Data

# route pour voir tous les comptes-rendus
@app.route('/datas', methods=['GET'])
def get_datas():
    '''Fonction pour voir tous les comptes-rendus de la base de donnée'''
    app.logger.info('Processing default request')
    return jsonify({'Data': Data.get_all_datas()})


@app.route('/datas/formated',methods=['GET'])
def get_formated_data():
    return jsonify({'Data': Data.get_formated_datas()})


@app.route('/datas/extended',methods=['GET'])
def get_extended_data():
    return jsonify({'Data': Data.get_all_datas_extended()})


@app.route('/datas/extended/client/<int:id>')
def get_extended_data_client(id):
    return jsonify({'Data': Data.get_datas_extended_byCLient(id)})


@app.route('/datas/extended/collab/<string:id>')
def get_extended_data_collab(id):
    return jsonify({'Data': Data.get_datas_extended_byCollab(id)})


@app.route('/data/<int:id>', methods=['GET'])
def get_data(id):
    return jsonify({'Data': Data.get_data(id)});


# route pour ajouter un compte rendu par méthode POST
@app.route('/data', methods=['POST'])
def add_data():
    '''Fonction pour ajoute un compte-rendu à la base de donnée'''
    request_data = request.get_json()  # getting data from client
    Data.add_data(request_data['id_collab'], request_data['id_client'], request_data['compte_rendu'], False)
    response = Response("Compte rendu ajouté", 201, mimetype='application/json')
    return response

#endregion


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4666, debug=True)
