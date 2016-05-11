from app import db,models

def add_com(u):
	db.session.add(u)
	db.session.commit()

u=models.User(username='admin',userpassword='2f8341dd723bc9ab229cb01f9308a334')
add_com(u)
