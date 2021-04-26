import traceback

import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
from settings import *
from datetime import datetime
import json
from sqlalchemy import text
import numpy as np

# Initialisation de la base de donnée
db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'client'  # creation du nom de la table
    id = db.Column(db.Integer, primary_key=True)  # Clée primaire
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=True)

    def json(self):
        return {'id': self.id, 'nom': self.nom,
                'prenom': self.prenom}
        # Méthode pour convertir la sortie en json

    def add_client(_prenom, _nom):
        '''fonction pour ajouter un client à la base: _nom, _prenom sont des paramètres'''
        # Creation d'instance à la méthode client
        new_client = Client(prenom=_prenom, nom=_nom)
        db.session.add(new_client)  # ajouter un client
        db.session.commit()  # commit le changement

    def getall_client():
        '''fonction pour voir tous les clients'''
        return [Client.json(client) for client in Client.query.all()]

    def get_client(_id):
        '''fonction pour voir un client avec son id'''
        return [Client.json(Client.query.filter_by(id=_id).first())]
        # Client.json convertit la sortie en json
        # filter_by permet de trier par id
        # .first() renvoie le premier id

    def update_client(_id, _nom, _prenom):
        '''fonction pour modifier un détail de la fiche client'''
        client_to_update = Client.query.filter_by(id=_id).first()
        client_to_update.nom = _nom
        client_to_update.prenom = _prenom
        db.session.commit()

    def delete_client(_id):
        '''fonction pour supprimer un client'''
        Client.query.filter_by(id=_id).delete()
        # filtrer par id et supprime
        db.session.commit()  # commit le changement dans la base de donnée

class Collaborateur(db.Model):
    __tablename__ = 'collaborateur'  # création de la table
    id = db.Column(db.Integer, primary_key=True)  # initialisation de la clé primaire
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String, nullable=False)

    def json(self):
        return {'id': self.id, 'nom': self.nom,
                'prenom': self.prenom}
        # convertir la sortie en json

    def add_collab(_prenom, _nom):
        '''fonction pour ajouter un client à la base: _nom, _prenom sont des paramètres'''
        # creation d'une instance pour la class Collaborateurs
        new_collaborateur = Collaborateur(prenom=_prenom, nom=_nom)
        db.session.add(new_collaborateur)  # add new movie to database session
        db.session.commit()  # commit changes to session

    def getall_collab():
        '''fonction pour voir tous les collaborateurs de la base de donnée'''
        return [Collaborateur.json(collaborateur) for collaborateur in Collaborateur.query.all()]


    def get_collab(_id):
        '''fonction pour voir un collaborateur par rapport à son id'''
        return [Collaborateur.json(Collaborateur.query.filter_by(id=_id).first())]
        # Client.json convertit la sortie en json
        # filter_by permet de trier par id
        # .first() renvoie le premier id

    def update_collab(_id, _nom, _prenom):
        '''fonction pour modifier un collaborateur'''
        collab_to_update = Collaborateur.query.filter_by(id=_id).first()
        collab_to_update.nom = _nom
        collab_to_update.prenom = _prenom
        db.session.commit()

    def delete_collab(_id):
        '''fonction pour supprimer un collaborateur par son id'''
        Collaborateur.query.filter_by(id=_id).delete()
        # filtrer par id et supprime
        db.session.commit()  # commit le changement et met à jour sa base de donnée


data_categorie = db.Table(
    'data_categorie',
    db.Column('data_id', db.Integer, db.ForeignKey('data.id')),
    db.Column('categorie_id',db.Integer, db.ForeignKey('categorie.id'))
)

class Categorie(db.Model):
    __tablename__ = 'categorie'  # creation de la table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # utilisation de la clé primaire
    libelle = db.Column(db.String(80), nullable=False)

    def json(self):
        return {'id': self.id, 'libelle': self.libelle}
        # Methode qui convertit la sortie en json

    def add_categorie(_libelle):
        '''function to add collab to database using _nom, _prenom
        as parameters'''
        # creer une instance pour le constructeur categories
        new_categorie = Categorie(_libelle=_libelle)
        db.session.add(new_categorie)  # ajoute la nouvelle categorie à la base de donnée
        db.session.commit()  # commit le changement

    def getall_categorie():
        '''function to get all movies in our database'''
        return [Categorie.json(categorie) for categorie in Categorie.query.all()]

    def get_categorie(_id):
        '''function to get movie using the id of the movie as parameter'''
        return [Categorie.json(Categorie.query.filter_by(id=_id).first())]
        # Categorie.json convertit la sortie en json
        # filter_by permet de trier par id
        # .first() renvoie le premier id

    def update_categorie(_id, _nom, _prenom):
        '''function to update the details of a movie using the id, title,
        year and genre as parameters'''
        categorie_to_update = Categorie.query.filter_by(id=_id).first()
        categorie_to_update.nom = _nom
        categorie_to_update.prenom = _prenom
        db.session.commit()

    def delete_categorie(_id):
        '''function to delete a movie from our database using
           the id of the movie as a parameter'''
        Categorie.query.filter_by(id=_id).delete()
        # filtre par id et supprime
        db.session.commit()  # commit le changement

class Data(db.Model):
    __tablename__ = 'data'  # création de la table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # initialisation clé primaire
    id_collab = db.Column(db.Integer, nullable=False)
    id_client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False)
    compte_rendu = db.Column(db.String(5000), nullable=False)
    isProcessed = db.Column(db.Boolean, default=False)

    def json(self):
        return {'id': self.id, 'id_collab': self.id_collab,
        'id_client': self.id_client, 'date_creation': self.date_creation,
        'compte_rendu': self.compte_rendu, 'isProcessed': self.isProcessed}
        # convertie la sortie en json

    def formatedjson(self):
        return {
            'id': self[0],
            'datecreation': self[1].strftime("%d/%m/%Y, %H:%M:%S"),
            'client': self[2] + " " + self[3],
            'compte_rendu': self[4],
            'traitement':self[5]
        }

    def extendedjson(self):
        return {
            'id': self[0],
            'datecreation': self[1],
            'client': self[2] + " " + self[3],
            'compte_rendu': self[4].replace("'",r"\'"),
            'traitement':self[5],
            'categories':self[6],
            'collab':self[7],
        }

    def simplejson(self):
        return {
            'client': self[1] +" "+ self[2],
            'cr': self[3],
        }

    def add_data(_id_collab, _id_client, _compte_rendu, _isProcessed):
        date = datetime.today();
        '''fonction pour ajouter un compte rendu avec les paramètres:_id_client, _date_creation, _compte_rendu'''
        # creating an instance of our Movie constructor
        new_data = Data(id_collab=_id_collab, id_client=_id_client,date_creation=date,compte_rendu=_compte_rendu,isProcessed=_isProcessed)
        db.session.add(new_data)  # ajouter le compte rendu dans la base de donnée
        db.session.commit()
        result = Data.predict(new_data.id,_compte_rendu)
        if(result == 1):
            sql = text('UPDATE data SET isProcessed = true WHERE id = '+ str(new_data.id))
            db.engine.execute(sql)


    def get_all_datas():
        '''fonction pour voir tous les comptes-rendus '''
        return [Data.json(data) for data in Data.query.all()]

    def get_formated_datas():
        q = db.session.query(Data.id, Data.date_creation,Client.nom, Client.prenom, Data.compte_rendu,Data.isProcessed).join(Client, Client.id == Data.id_client).all()
        return [Data.formatedjson(element) for element in q];

    def get_all_datas_extended():
        sql = text('SELECT data.id,strftime(\'%d/%m/%Y à %Hh%M\' ,data.date_creation),cl.nom,cl.prenom,data.compte_rendu,data.isProcessed,json_group_array(c.libelle) as \'categories\',data.id_collab FROM data INNER JOIN client cl on data.id_client = cl.id LEFT JOIN data_categorie dc on data.id = dc.data_id LEFT JOIN categorie c on c.id = dc.categorie_id GROUP BY data.id ORDER BY data.id')
        result = db.engine.execute(sql)
        toReturn = [Data.extendedjson(element) for element in result ]
        return toReturn

    def get_datas_extended_byCollab(_id):
        sql = text(
            'SELECT data.id,strftime(\'%d/%m/%Y à %Hh%M\' ,data.date_creation),cl.nom,cl.prenom,data.compte_rendu,data.isProcessed,json_group_array(c.libelle) as \'categories\' ,data.id_collab FROM data INNER JOIN client cl on data.id_client = cl.id LEFT JOIN data_categorie dc on data.id = dc.data_id LEFT JOIN categorie c on c.id = dc.categorie_id WHERE data.id_collab LIKE "'+ _id +'" GROUP BY data.id ORDER BY data.id')
        result = db.engine.execute(sql)
        toReturn = [Data.extendedjson(element) for element in result]
        return toReturn

    def get_datas_extended_byCLient(_id):
        sql = text(
            'SELECT data.id,data.date_creation,cl.nom,cl.prenom,data.compte_rendu,data.isProcessed,json_group_array(c.libelle) as \'categories\' ,data.id_collab FROM data INNER JOIN client cl on data.id_client = cl.id LEFT JOIN data_categorie dc on data.id = dc.data_id LEFT JOIN categorie c on c.id = dc.categorie_id WHERE data.id_client = "'+ str(_id) +'" GROUP BY data.id ORDER BY data.id')
        result = db.engine.execute(sql)
        toReturn = [Data.extendedjson(element) for element in result]
        return toReturn

    def get_data(_id):
        '''fonction pour voir un compte-rendu'''
        sql = text(
            'SELECT data.id, cl.nom,cl.prenom,data.compte_rendu FROM data INNER JOIN client cl on data.id_client = cl.id WHERE data.id = '+str(_id))
        result = db.engine.execute(sql)
        toReturn = [Data.simplejson(element) for element in result]
        return toReturn
        #return [Data.json(Data.query.filter_by(id=_id).first())]
        # Data.json convertit la sortie en json
        # filter_by permet de trier par id
        # .first() renvoie le premier id

    def predict(_id,_txt):
        '''Utilisation du model pour prédire les catégories'''
        lr = joblib.load('./machine_learning/model_decision_tree.pkl') #Chargement du model
        #model_columns = joblib.load('') #Chargement des colonnes
        if lr:
            try:
                #Prediction via le model
                cleaned_txt = Tools.clean_text(_txt)
                query_df = pd.DataFrame([{"text":cleaned_txt}])
                query = pd.get_dummies(query_df)
                prediction = lr.predict(query)
                prediction_json = str(prediction).replace(" ", ",").replace("[[","{").replace("]]","}")

                #Enregistrement de la prediction
                if(prediction[0][0] == 1):
                    #Upload to datatable Montant
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 19)")
                    result = db.engine.execute(sql)

                if(prediction[0][1] == 1):
                    #Upload to datatable credit vehicule
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 8)")
                    result = db.engine.execute(sql)

                if(prediction[0][2] == 1):
                    #Upload to datatable date
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 18)")
                    result = db.engine.execute(sql)

                if(prediction[0][3] == 1):
                    #Upload to datatable bilan suivi relationnel
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 3)")
                    result = db.engine.execute(sql)

                if(prediction[0][4] == 1):
                    #Upload to datatable epargne terme
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 7)")
                    result = db.engine.execute(sql)

                if(prediction[0][5] == 1):
                    #Upload to datatable credit travaux
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 17)")
                    result = db.engine.execute(sql)

                if(prediction[0][6] == 1):
                    #Upload to datatable entree en relation conquete
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 2)")
                    result = db.engine.execute(sql)

                if(prediction[0][7] == 1):
                    #Upload to datatable point intention risque
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 1)")
                    result = db.engine.execute(sql)

                if(prediction[0][8] == 1):
                    #Upload to datatable reclamation
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 6)")
                    result = db.engine.execute(sql)

                if(prediction[0][9] == 1):
                    #Upload to datatable credit conso
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 5)")
                    result = db.engine.execute(sql)

                if(prediction[0][10] == 1):
                    #Upload to datatable evenement de vie
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 15)")
                    result = db.engine.execute(sql)

                if(prediction[0][11] == 1):
                    #Upload to datatable epargne disponible
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 4)")
                    result = db.engine.execute(sql)

                if(prediction[0][12] == 1):
                    #Upload to datatable non specifie credit assurance epargne
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 11)")
                    result = db.engine.execute(sql)

                if(prediction[0][13] == 1):
                    #Upload to datatable assurance de bien
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 12)")
                    result = db.engine.execute(sql)

                if(prediction[0][14] == 1):
                    #Upload to datatable assurance de personne
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 9)")
                    result = db.engine.execute(sql)

                if(prediction[0][15] == 1):
                    #Upload to datatable baq service bancaires
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 14)")
                    result = db.engine.execute(sql)

                if(prediction[0][16] == 1):
                    #Upload to datatable credit habitat
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 13)")
                    result = db.engine.execute(sql)

                if(prediction[0][17] == 1):
                    #Upload to datatable credit agri pro
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 10)")
                    result = db.engine.execute(sql)

                if(prediction[0][18] == 1):
                    #Upload to datatable projet exceptionnel
                    sql = text("INSERT INTO data_categorie (data_id, categorie_id) VALUES ("+ str(_id) +", 16)")
                    result = db.engine.execute(sql)


                return 1;
            except:
                return jsonify({'trace': traceback.format_exc()})
        else:
            print('Erreur de chargement du model.')
            return ('No model loaded')

class Tools():
    def clean_text(txt):
        stop_words = stopwords.words('french')
        ps = PorterStemmer()

        txt = txt.lower()  # lowercase
        txt = re.sub("[^a-zA-Z]", " ", txt)  # Remove everything except alphabetical characters
        txt = word_tokenize(txt)  # tokenize (split into list and remove whitespace)

        # initialize list to store clean text
        clean_text = ""

        # iterate over each word
        for w in txt:
            # remove stopwords
            if w not in stop_words:
                # stem=ps.stem(w) #stem
                stem = w
                clean_text += stem + " "
        return clean_text