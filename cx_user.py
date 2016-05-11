from app import db, models

users=models.User.query.all()
print users
for u in users:
    print u.usernmae,u.userpassword
e=models.User.query.get(1)
print e
p=models.User.query.filter_by(usernmae='admin').first()
print p.id
print p.usernmae
#d=models.User.query.filter(models.User.email.endswith('@email.com')).all()
#print d
