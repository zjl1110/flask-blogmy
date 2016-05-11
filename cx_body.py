from app import db, models

users=models.User.query.all()
print users
for u in users:
	print u.id,u.username
e=models.User.query.get(1)
print e
p=models.User.query.filter_by(username='admin').first()
print p.id

dd=models.User.query.filter(models.User.id).all()
print 'dd: ',dd

d=models.Post.query.filter(models.Post.body).all()
print d

posts=models.Post.query.all()

for post in posts:
	print post.tilte

cc=models.Post.query.filter_by(id=7).first()
print 'aa:',cc.id
print 'bb:',cc.body

xxx=models.Post.query.get(7)
print xxx
pingls=models.Pinl.query.filter_by(body_id=7).all()
print pingls
for pingl in pingls:
    db.session.delete(pingl)
    db.session.commit()
print pingls