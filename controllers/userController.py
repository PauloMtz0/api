from models.User import User
from flask import jsonify
from config import db
from flask_jwt_extended import create_access_token

def get_all_users():
    try: 
        return [  user.to_dict()  for user in User.query.all()]
    except Exception as error:
        print(f"error {error}")
        return jsonify({ 'msg' : 'error al crear usuario' }), 500

def create_user(name, email, password):
    try: 
        new_user = User(name, email, password)

        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict()
    
    except Exception as e: 
        print(f"error {e}")
        return jsonify({ 'msg' : 'error al crear usuario' }), 500 
        


#actualizar usuario
def update_user (id, name, email):
    try:
        user = User.query.get(id)
        if not user:
            return None
    
        user.name = name
        user.email = email
        db.session.commit()

        return user.to_dict()
    except Exception as e:
        print(f"ERROR {e}")


#eliminar usuario
def delete_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return None
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"})
    
    except Exception as e:
        db.session.rollback()
        print(f"ERROR {e}")
    

#especifico usuario
def get_user(id):
    try:
        user = User.query.get(id)
        return user.to_dict()
    
    except Exception as e:
        print(f"ERROR {e}")


def login_user (email, password):
        user = User.query.filter_by(email=email).first();

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id);
            return jsonify({
                'access_token': access_token,
                'user': {
                    "id" : user.id,
                    "name" : user.name,
                    "email" : user.email
                }
            })
        return jsonify({"msg": "Credenciales invalidas"}), 401



#user = User.query.all();
#   print(user)