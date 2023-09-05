from db_con import Session
from models import Data_Optimization, DataOptmizers
from schemas import DataOptimization, Optmizers


# Создание декоратора для обращении к сесии БД и ее закрытие
def Get_session(func):
    def wrapper(*args, **kwargs):
        with Session() as session_db:
            out = func(*args, **kwargs, session_db=session_db)
        return out

    return wrapper


@Get_session
def get_name(session_db):
    name = session_db.query(Data_Optimization.name).all()
    return name


@Get_session
def update_data(models: DataOptimization, session_db):
    data = session_db.query(Data_Optimization).get(models.name)
    data.variables = models.variables
    data.matrix = models.matrix
    session_db.commit()

@Get_session
def update_options(models: DataOptimization, session_db):
    data = session_db.query(Data_Optimization).get(models.name)
    data.options = models.options
    session_db.commit()

@Get_session
def get_variables(select_name, session_db):
    name = session_db.query(Data_Optimization.variables).filter(Data_Optimization.name == select_name).one()[0]
    return name


@Get_session
def get_target(select_name, session_db):
    target = session_db.query(Data_Optimization.obj).filter(Data_Optimization.name == select_name).one()[0]
    return target


@Get_session
def get_matrix(select_name, session_db):
    matrix = session_db.query(Data_Optimization.matrix).filter(Data_Optimization.name == select_name).one()[0]
    return matrix

@Get_session
def get_options(select_name, session_db):
    options = session_db.query(Data_Optimization.options).filter(Data_Optimization.name == select_name).one()[0]
    return options


@Get_session
def create_model(models: DataOptimization, session_db):
    model = Data_Optimization(name=models.name, variables=models.variables, matrix=models.matrix, options = models.options)
    session_db.add(model)
    session_db.commit()


@Get_session
def create_target(models: DataOptimization, session_db):
    data = session_db.query(Data_Optimization).get(models.name)
    data.obj = models.obj
    session_db.commit()

@Get_session
def create_optimizer(models: Optmizers, session_db):
    opt = DataOptmizers(name=models.name, description=models.description)
    session_db.add(opt)
    session_db.commit()

@Get_session
def get_optimizer_descript(session_db):
    opt = session_db.query(DataOptmizers.description).all()
    print(opt)
    return opt


@Get_session
def get_optimizer_by_descript(description: str, session_db):
    opt = session_db.query(DataOptmizers).filter(DataOptmizers.description == description).one()
    return opt

@Get_session
def get_optimization(select_name, session_db):
    data = session_db.query(Data_Optimization).filter(Data_Optimization.name == select_name).one()
    return data

@Get_session
def delete_variables(select_name, session_db):
    variables = session_db.query(Data_Optimization).get(select_name)
    session_db.delete(variables)
    session_db.commit()

@Get_session
def create_opt(optimization: Optmizers, session_db):
    opt = DataOptmizers(name=optimization.name, description=optimization.description)
    session_db.add(opt)
    session_db.commit()

@Get_session
def delete_opt(name, session_db):
    opt = session_db.query(DataOptmizers).get(name)
    session_db.delete(opt)
    session_db.commit()

@Get_session
def get_name_opt(session_db):
    name = session_db.query(DataOptmizers.name).all()
    return name

#create_optimizer(Optmizers(name = 'IPOPTOptimizerMatrix',description='Оптимизация матрици методом IPOPT'))