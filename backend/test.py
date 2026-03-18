# from sqlalchemy import Column, Integer, String, create_engine, Sequence, ForeignKey
# from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# engine = create_engine('sqlite:///cwd.db')
# Session = sessionmaker(bind=engine)
# session = Session()


# Base = declarative_base()


# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer , Sequence('user_id_seq') , primary_key=True)
#     name = Column(String(50))
#     email = Column(String(50))
#     posts = relationship('post' , back_popuates='user')
 

# class Post(Base):
#     __tablename__ = 'posts'
#     id = Column(Integer, primary_key=True)
#     title = Column(String(50))
#     content  = Column(String(50))
#     user_id = Column(Integer , ForeignKey('user-id'))
#     user =relationship('User' , back_popuates='posts')


# Base.metadata.create_all(engine)


# user1 = User(name='brahim' , email='brahim@gmail.com')
# user2 = User(name='ouhammou' , email='ouhammou@gmail.com')


# user = session.query(User).filter_by(name="brahim").first()

# # session.delete(user)
# # session.commit()



from datetime import datetime

print(datetime.utcnow())