from flask import Blueprint, jsonify, request
from controllers.userController import get_all_users, create_user, login_user, update_user, delete_user, get_user

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def index():
    """
    Obtener todos los usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
    """
    users = get_all_users()
    return jsonify(users)


@user_bp.route('/<int:id>', methods=['GET'])
def user(id):
    """
    Obtener un usuario por ID
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del usuario a buscar
    responses:
      200:
        description: Usuario encontrado
      404:
        description: Usuario no encontrado
    """
    user = get_user(id)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user)


@user_bp.route('/<int:id>', methods=['PUT'])
def user_update(id):
    """
    Actualizar usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del usuario a actualizar
      - in: body
        name: user
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              example: "Juan Actualizado"
            email:
              type: string
              example: "juan@nuevocorreo.com"
    responses:
      200:
        description: Usuario actualizado exitosamente
      404:
        description: Usuario no encontrado
    """
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    user = update_user(id, name, email)
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    return jsonify(user)


@user_bp.route('/<int:id>', methods=['DELETE'])
def user_delete(id):
    """
    Eliminar usuario
    ---
    tags:
      - Usuarios
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID del usuario a eliminar
    responses:
      200:
        description: Usuario eliminado exitosamente
      404:
        description: Usuario no encontrado
    """
    result = delete_user(id)
    if result is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(result), 200


@user_bp.route('/', methods=['POST'])
def user_store():
    """
    Crear un usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: user
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
              example: "Juan Pérez"
            email:
              type: string
              example: "juan@example.com"
            password:
              type: string
              example: "123456"
    responses:
      201:
        description: Usuario creado exitosamente
    """
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    new_user = create_user(name, email, password)
    return jsonify(new_user), 201


@user_bp.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión
    ---
    tags:
     - Autenticación
    parameters:
      - in: body
        name: credentials
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: "juan@example.com"
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Inicio de sesión exitoso
    """
    data = request.get_json()
    return login_user(data['email'], data['password'])
