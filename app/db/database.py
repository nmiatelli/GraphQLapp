from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job, User, JobApplication
from app.settings.config import DB_URL
from app.db.data import jobs_data, employers_data, users_data, applications_data




engine = create_engine(DB_URL, echo=True)
conn = engine.connect()

# "segura" todos os dados antes de enviar/deletar no banco
Session = sessionmaker(bind=engine)


# Sempre que reiniciar o servidor ele deleta tudo e cria de novo (ambiente de dev)
def prepare_database():
    from app.settings.utils import hash_password
    Base.metadata.drop_all(engine)
    # Cria efetivamente as tabelas no banco
    Base.metadata.create_all(engine)
    session = Session()


    for employer in employers_data:
    #create a new instance of employer and add it to the session -> Employer(id=employer.get("id"), name=employer.get("name")..)
    # ** -> unpack dictionaire
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))
    
    for user in users_data:
       
        user["password_hash"] = hash_password(user['password'])
        del user['password']
        session.add(User(**user))
    
    for apl in applications_data:
        session.add(JobApplication(**apl))

    # Persistindo os dados no DB
    session.commit()
    session.close()