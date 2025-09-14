from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'
    
    cod = db.Column(db.Integer, primary_key=True)
    nome_do_produto = db.Column(db.Text)
    marca = db.Column(db.Text)
    ceara = db.Column(db.Integer, default=0)
    santa_catarina = db.Column(db.Integer, default=0)
    sao_paulo = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)
    reserva = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'cod': self.cod,
            'nome_do_produto': self.nome_do_produto,
            'marca': self.marca,
            'ceara': self.ceara,
            'santa_catarina': self.santa_catarina,
            'sao_paulo': self.sao_paulo,
            'total': self.total,
            'reserva': self.reserva
        }

