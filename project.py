from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

from flask import Flask, render_template, request,redirect,url_for
app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant')
def restaurant():
    restaurant= session.query(Restaurant).all()

    output = ''
    output+='<h2>Restaurants</h2></br>'
    for i in restaurant:
        output+= i.name
        output+= '</br></br>'
    return output
@app.route('/restaurant/<int:restaurant_id>/')
def restaurantmenu(restaurant_id):
    restaurant=session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html',restaurant=restaurant,items=items)

@app.route('/restaurant/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method=='POST':
        newItem=MenuItem(name = request.form['name'], price=request.form['price'], description=request.form['description'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantmenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id,menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name=request.form['name']
            session.add(editedItem)
            session.commit()
            return render_template(url_for('restaurantmenu', restaurant_id=restaurant_id, menu_id=menu_id), i= editedItem)
    else:
        return render_template(url_for('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i= editMenuItem))

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id,menu_id):
    return "this is to delete menu items"


if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)