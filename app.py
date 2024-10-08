# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template_string, render_template, url_for, request, redirect, session, flash, Response
import folium

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

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

    htmlcode = f"""
    <table border="1" class="table table-success table-striped">
        <tr><td colspan="2"><img src='{foto_url}' width='250' height='200'></td></tr>
        <tr><td>Tienda:</td><td>{nombre_tienda}</td></tr>
        <tr><td>Contacto:</td><td>{contacto}</td></tr>
        <tr><td>Dirección:</td><td>{direccion}</td></tr>
        <tr><td>Fecha:</td><td>{fecha}</td></tr>
        <tr><td colspan="2"><center><a class="btn btn-primary" href="{url_for('pedido')}" style="color: white;">Hacer Pedido</a></center></td></tr>
    </table>"""

    folium.Marker(
        location=[-17.3935, -66.1570],
        popup=htmlcode,
        tooltip='Haz click para más información'
    ).add_to(m)

    
    # path = '/home/patitofeo/mysite/mapa_cbb2.html'
    # m.save(path)

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