# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template_string, render_template, url_for, request, redirect, session, flash, Response
import folium

from folium import IFrame
import json
# import cv2

usuarios =  {
    "usuario1": {
        "correo": "usuario1@gmail.com", 
        "clave": "123", 
        "rol" : "vendedor"
    },
    "usuario2": {
        "correo": "usuario2@gmail.com", 
        "clave": "456",
        "rol": "vendedor"
    },
    "usuario3": {
        "correo": "usuario3@gmail.com",
        "clave": "789",
        "rol": "gerente"
    }
}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/validar_login', methods=['POST'])
def validar_login():
    usuario_formulario = request.form['username']
    clave_formulario = request.form['password']
    
    if(usuario_formulario in usuarios):
        user_data = usuarios[usuario_formulario]
        user_login = user_data
        user_clave = user_data['clave']
        user_rol = user_data['rol']
        if(user_clave == clave_formulario):
            session['usuarios_logueado'] = usuario_formulario
            session['rol'] = user_rol
            return render_template('index.html')
    else:
        return redirect(url_for('login'))




@app.route('/mapa')
def mapa():
    m = folium.Map(location=[-17.3935, -66.1570], zoom_start=15)
    folium.Marker(
        location=[-17.3935, -66.1570],
        popup='Cochabamba, Bolivia',
        tooltip='Haz click para más información'
    ).add_to(m)
    mapa_html = m._repr_html_()  # Corregido aquí
    path ='./mapa_cbb.html'
    m.save(path)
    return render_template_string(mapa_html)

@app.route('/ver_mapa')
def ver_mapa():
    m = folium.Map(location=[-17.3935, -66.1570], zoom_start=15)

    foto = 'tienda_barrio.jpg'
    foto_url = url_for('static', filename=foto)
    nombre_tienda = 'Doña Filomena'
    contacto = 'Filomena Delgado'
    direccion = 'calle La Tablada # 4533'
    fecha = '10 Agosto 2024'

    tiendas = [
        {   'nombre_tienda': 'Doña filomena',
            'contacto': 'Filomena Delgado',
            'direccion': 'calle La Tablada # 4533',
            'fecha': '10 Agosto 2024',
            'coordenadas': [-17.3935, -66.1570],
            'foto': 'tienda_barrio.jpg'
        },

        {   'nombre_tienda': 'Tienda Maria',
            'contacto': 'Juanita perez',
            'direccion': 'Av. Trinidad y Tomas Oconor # 1020',
            'fecha': '15 Agosto 2024',
            'coordenadas': [-17.375906, -66.157694],
            'foto': './images/tienda_Maria.png'
        },

        {   'nombre_tienda': 'Tiena Pepe',
            'contacto': 'Oscar flores',
            'direccion': 'Av. Melchor urquidi y zenon salinas # 1320',
            'fecha': '25 Agosto 2024',
            'coordenadas': [-17.374338, -66.149587],
            'foto': './images/tienda_Pepe.png'
        },

        {   'nombre_tienda': 'Tiena Don aguilar',
            'contacto': 'Pedro aguilar',
            'direccion': 'Av. Santa cruz y Buenos Aires # 1253',
            'fecha': '22 Agosto 2024',
            'coordenadas': [-17.374155, -66.156953],
            'foto': './images/tienda_Pep.png'
        },
        {   'nombre_tienda': 'Tiena Copacabana',
            'contacto': 'Luis Miguel',
            'direccion': 'Av. Portales y A.M. Torrico # 1254',
            'fecha': '05 Octubre 2024',
            'coordenadas': [-17.375054, -66.155478],
            'foto': './images/tienda_Copacabana.png'
        }
    ]

    for tienda in tiendas:
        foto_url = url_for('static', filename=tienda['foto'])  # Obtener la URL de la foto

        # Crear el código HTML para el popup de cada tienda
        htmlcode = f"""
        <table border="1" class="table table-success table-striped">
            <tr><td colspan="2"><img src='{foto_url}' width='250' height='200'></td></tr>
            <tr><td>Tienda:</td><td>{tienda['nombre_tienda']}</td></tr>
            <tr><td>Contacto:</td><td>{tienda['contacto']}</td></tr>
            <tr><td>Dirección:</td><td>{tienda['direccion']}</td></tr>
            <tr><td>Fecha:</td><td>{tienda['fecha']}</td></tr>
            <tr><td colspan="2"><center><a class="btn btn-primary" href="{url_for('pedido')}" style="color: white;">Hacer Pedido</a></center></td></tr>
        </table>"""

        folium.Marker(
            location=tienda['coordenadas'],
            popup=htmlcode,
            tooltip=f"{tienda['nombre_tienda']}: Haz click para más información"
        ).add_to(m)
 

    # Usar el método correcto para generar el HTML del mapa
    mapa_html = m._repr_html_()

    # Renderizar la plantilla HTML y pasarle el mapa
    return render_template('mapa.html', mapa=mapa_html)





@app.route('/pedido')
def pedido():
    return render_template("ventanamodal.html")

@app.route('/ventanamodal')
def ventanamodal():
    return render_template("ventanamodal.html")

if __name__ == '__main__':
    app.run(debug=True)