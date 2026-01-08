# models.py
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Empresa(db.Model):
    """Modelo de empresa/organização"""
    __tablename__ = 'empresas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(18), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    cidade = db.Column(db.String(100))
    estado = db.Column(db.String(2))

    # Plano e status
    plano = db.Column(db.String(20), default='basico')  # 'basico', 'premium', 'enterprise'
    ativo = db.Column(db.Boolean, default=True)
    bloqueado = db.Column(db.Boolean, default=False)
    motivo_bloqueio = db.Column(db.Text)

    # Limites do plano
    max_usuarios = db.Column(db.Integer, default=10)
    max_vendedores = db.Column(db.Integer, default=50)

    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Empresa {self.nome}>'


class Usuario(UserMixin, db.Model):
    """Modelo de usuário para autenticação"""
    __tablename__ = 'usuarios'
    # Removido __bind_key__ para usar o mesmo banco que vendedores

    # Índices compostos para queries comuns
    __table_args__ = (
        db.Index('idx_usuario_empresa_cargo', 'empresa_id', 'cargo', 'ativo'),
        db.Index('idx_usuario_gerente', 'gerente_id', 'ativo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)

    # Níveis de acesso
    cargo = db.Column(
        db.String(50),
        default='usuario',
        index=True
    )  # 'admin', 'supervisor', 'gerente', 'usuario', 'vendedor', 'rh', 'financeiro'

    # Departamento (para funcionários administrativos)
    departamento = db.Column(
        db.String(50),
        nullable=True
    )  # 'rh', 'financeiro', 'comercial', 'ti', 'administrativo'

    # Relacionamento com empresa
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey('empresas.id'),
        nullable=True
    )
    empresa = db.relationship('Empresa', backref='usuarios')

    # Hierarquia: supervisor vinculado a gerente/administrador
    gerente_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=True
    )
    # Relacionamento self-referential para supervisores vinculados a gerente
    supervisores = db.relationship(
        'Usuario',
        backref=db.backref('gerente', remote_side=[id]),
        foreign_keys=[gerente_id]
    )

    # Hierarquia: vendedores/usuários vinculados a supervisor
    supervisor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=True
    )
    # Relacionamento para usuários supervisionados (vendedores, técnicos)
    subordinados = db.relationship(
        'Usuario',
        backref=db.backref('supervisor', remote_side=[id]),
        foreign_keys=[supervisor_id]
    )

    # Vínculo opcional com um vendedor específico (login de vendedor)
    vendedor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendedores.id'),
        nullable=True,
        index=True
    )
    vendedor = db.relationship(
        'Vendedor',
        backref=db.backref('usuario_login', uselist=False),
        foreign_keys=[vendedor_id]
    )

    # Super admin (acessa todas as empresas)
    is_super_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        server_default='0'
    )

    # Status e bloqueio
    ativo = db.Column(db.Boolean, default=True)
    bloqueado = db.Column(db.Boolean, default=False)
    motivo_bloqueio = db.Column(db.Text)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Permissões detalhadas por módulo
    # Permissões Gerais
    pode_ver_dashboard = db.Column(db.Boolean, default=True)
    pode_enviar_mensagens = db.Column(db.Boolean, default=True)
    pode_exportar_dados = db.Column(db.Boolean, default=False)

    # Permissões de Vendas
    pode_gerenciar_vendedores = db.Column(db.Boolean, default=False)
    pode_gerenciar_metas = db.Column(db.Boolean, default=False)
    pode_gerenciar_equipes = db.Column(db.Boolean, default=False)
    pode_gerenciar_comissoes = db.Column(db.Boolean, default=False)
    pode_ver_todas_metas = db.Column(db.Boolean, default=False)
    pode_aprovar_comissoes = db.Column(db.Boolean, default=False)

    # Permissões de Clientes
    pode_acessar_clientes = db.Column(db.Boolean, default=True)
    pode_criar_clientes = db.Column(db.Boolean, default=False)
    pode_editar_clientes = db.Column(db.Boolean, default=False)
    pode_excluir_clientes = db.Column(db.Boolean, default=False)
    pode_importar_clientes = db.Column(db.Boolean, default=False)

    # Permissões de Ordens de Serviço
    pode_acessar_os = db.Column(db.Boolean, default=False)
    pode_criar_os = db.Column(db.Boolean, default=False)
    pode_aprovar_os = db.Column(db.Boolean, default=False)
    pode_atualizar_os = db.Column(db.Boolean, default=False)
    pode_cancelar_os = db.Column(db.Boolean, default=False)

    # Permissões de Estoque
    pode_acessar_estoque = db.Column(db.Boolean, default=False)
    pode_gerenciar_produtos = db.Column(db.Boolean, default=False)
    pode_movimentar_estoque = db.Column(db.Boolean, default=False)
    pode_ver_custos = db.Column(db.Boolean, default=False)
    pode_ajustar_estoque = db.Column(db.Boolean, default=False)

    # Permissões de Técnicos
    pode_gerenciar_tecnicos = db.Column(db.Boolean, default=False)
    pode_atribuir_tecnicos = db.Column(db.Boolean, default=False)

    # Relacionamento com vendedores (se for supervisor)
    vendedores = db.relationship(
        'Vendedor',
        backref='supervisor_obj',
        lazy=True,
        foreign_keys='Vendedor.supervisor_id'
    )

    # Relacionamentos de mensagens
    mensagens_enviadas = db.relationship(
        'Mensagem',
        backref='remetente',
        lazy='dynamic',
        foreign_keys='Mensagem.remetente_id',
        cascade='all, delete-orphan'
    )

    mensagens_recebidas = db.relationship(
        'Mensagem',
        backref='destinatario',
        lazy='dynamic',
        foreign_keys='Mensagem.destinatario_id',
        cascade='all, delete-orphan'
    )

    def set_senha(self, senha):
        """Gera hash da senha"""
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, senha)

    def calcular_meta_supervisionada(self, mes, ano):
        """
        Calcula a meta do supervisor como somatório das metas de seus vendedores

        Args:
            mes (int): Mês de referência (1-12)
            ano (int): Ano de referência

        Returns:
            float: Valor total das metas dos vendedores supervisionados
        """
        if not self.vendedores:
            return 0.0

        total_meta = 0.0
        for vendedor in self.vendedores:
            # Buscar meta do vendedor para o mês/ano específico
            meta = Meta.query.filter_by(
                vendedor_id=vendedor.id,
                mes=mes,
                ano=ano
            ).first()

            if meta and meta.valor_meta:
                total_meta += meta.valor_meta

        return total_meta

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Vendedor(db.Model):
    """Modelo de vendedor"""
    __tablename__ = 'vendedores'
    # Removido __bind_key__ para usar o mesmo banco que usuarios

    # Índices compostos para queries comuns
    __table_args__ = (
        db.Index('idx_vendedor_supervisor', 'supervisor_id', 'ativo'),
        db.Index('idx_vendedor_equipe', 'equipe_id', 'ativo'),
        db.Index('idx_vendedor_empresa', 'empresa_id', 'ativo'),
    )

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(14), unique=True, index=True)

    # Relacionamento com empresa
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey('empresas.id'),
        nullable=True
    )

    # Relacionamento com supervisor
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    supervisor_nome = db.Column(db.String(100))

    # Relacionamento com equipe
    equipe_id = db.Column(db.Integer, db.ForeignKey('equipes.id'))

    # Status
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com metas
    metas = db.relationship(
        'Meta',
        backref='vendedor',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f'<Vendedor {self.nome}>'


class Meta(db.Model):
    """Modelo de meta mensal - Suporta meta de Valor e Volume"""
    __tablename__ = 'metas'

    id = db.Column(db.Integer, primary_key=True)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'), nullable=False)

    # Período da meta
    mes = db.Column(db.Integer, nullable=False)  # 1-12
    ano = db.Column(db.Integer, nullable=False)

    # NOVO: Tipo de meta
    tipo_meta = db.Column(db.String(20), default='valor')  # 'valor' ou 'volume'

    # Meta de VALOR (financeiro)
    valor_meta = db.Column(db.Float, nullable=True)
    receita_alcancada = db.Column(db.Float, default=0.0)

    # NOVO: Meta de VOLUME (quantidade de vendas)
    volume_meta = db.Column(db.Integer, nullable=True)
    volume_alcancado = db.Column(db.Integer, default=0)

    # Comissão calculada
    percentual_alcance = db.Column(db.Float, default=0.0)
    comissao_total = db.Column(db.Float, default=0.0)

    # NOVO: Balanceamento
    periodo_historico = db.Column(db.Integer, default=6)  # 3-12 meses de histórico
    data_base_calculo = db.Column(db.DateTime)  # Data em que foi calculada
    meta_balanceada = db.Column(db.Boolean, default=False)  # Foi calculada automaticamente?
    tendencia_calculada = db.Column(db.Float)  # Tendência de crescimento/queda
    media_mensal_historico = db.Column(db.Float)  # Média mensal do período

    # Status
    status_comissao = db.Column(db.String(20), default='Pendente')  # 'Pendente', 'Aprovado', 'Pago'
    observacoes = db.Column(db.Text)

    # Auditoria
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Índice composto para garantir uma meta por vendedor por mês
    __table_args__ = (
        db.UniqueConstraint('vendedor_id', 'mes', 'ano', name='_vendedor_mes_ano_uc'),
        db.Index('idx_meta_vendedor_periodo', 'vendedor_id', 'ano', 'mes'),
        db.Index('idx_meta_status', 'status_comissao', 'ano', 'mes'),
    )

    def calcular_comissao(self):
        """Calcula o percentual de alcance e a comissão.

        Prioridade:
        1) Usar faixas configuradas em FaixaComissaoVendedor (por empresa ou globais),
           exatamente como exibidas na tela de "Configuração de Faixas de Comissão".
        2) Se não houver faixas configuradas, usar o cálculo padrão de calculo_comissao.py
           para manter compatibilidade.
        """
        from calculo_comissao import calcular_percentual_alcance, calcular_comissao

        # Tipo de meta financeiro (padrão)
        if self.tipo_meta == 'valor':
            if not self.valor_meta or self.valor_meta <= 0:
                self.percentual_alcance = 0.0
                self.comissao_total = 0.0
                return

            # 1) Percentual de alcance da meta
            self.percentual_alcance = calcular_percentual_alcance(
                self.receita_alcancada or 0.0,
                self.valor_meta,
            )

            # 2) Tentar usar faixas configuradas em FaixaComissaoVendedor
            taxa_aplicada = None

            try:
                # Descobrir empresa do vendedor, se disponível
                empresa_id = None
                if hasattr(self, 'vendedor') and self.vendedor is not None:
                    empresa_id = getattr(self.vendedor, 'empresa_id', None)

                from models import FaixaComissaoVendedor  # evitar import circular em tempo de definição

                query = FaixaComissaoVendedor.query.filter_by(ativa=True)
                if empresa_id:
                    faixas = (
                        query.filter_by(empresa_id=empresa_id)
                        .order_by(FaixaComissaoVendedor.alcance_min)
                        .all()
                    )
                else:
                    faixas = []

                # Se não houver faixas da empresa, buscar faixas globais
                if not faixas:
                    faixas = (
                        FaixaComissaoVendedor.query.filter(
                            FaixaComissaoVendedor.empresa_id.is_(None),
                            FaixaComissaoVendedor.ativa.is_(True),
                        )
                        .order_by(FaixaComissaoVendedor.alcance_min)
                        .all()
                    )

                if faixas:
                    perc = self.percentual_alcance or 0.0
                    # Garante ordenação por alcance_min
                    faixas_ordenadas = sorted(
                        faixas, key=lambda f: (f.alcance_min or 0)
                    )
                    for faixa in faixas_ordenadas:
                        if perc <= (faixa.alcance_max or perc):
                            taxa_aplicada = faixa.taxa_comissao
                            break
                    # Se não entrou em nenhuma faixa explícita, usa a última
                    if taxa_aplicada is None:
                        taxa_aplicada = faixas_ordenadas[-1].taxa_comissao

            except Exception:
                # Em caso de qualquer erro, mantemos taxa_aplicada = None
                taxa_aplicada = None

            if taxa_aplicada is not None:
                # Comissão baseada na taxa configurada
                self.comissao_total = (self.receita_alcancada or 0.0) * float(
                    taxa_aplicada
                )
            else:
                # Fallback: cálculo padrão legado
                self.comissao_total = calcular_comissao(
                    self.receita_alcancada or 0.0,
                    self.percentual_alcance,
                )

        # Tipo de meta em volume mantém comportamento anterior,
        # usando o cálculo padrão de comissão.
        elif self.tipo_meta == 'volume':
            if self.volume_meta and self.volume_meta > 0:
                self.percentual_alcance = (
                    (self.volume_alcancado or 0) / self.volume_meta
                ) * 100
                self.comissao_total = calcular_comissao(
                    self.volume_alcancado or 0,
                    self.percentual_alcance,
                )
            else:
                self.percentual_alcance = 0.0
                self.comissao_total = 0.0

    def __repr__(self):
        return f'<Meta {self.vendedor_id} - {self.mes}/{self.ano} ({self.tipo_meta})>'


class Equipe(db.Model):
    """Modelo de equipe de vendedores"""
    __tablename__ = 'equipes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)

    # Relacionamento com empresa
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey('empresas.id'),
        nullable=True
    )

    # Relacionamento com supervisor
    supervisor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )
    supervisor = db.relationship('Usuario', backref='equipes_supervisionadas')

    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com vendedores
    vendedores = db.relationship(
        'Vendedor',
        backref='equipe_obj',
        lazy=True,
        foreign_keys='Vendedor.equipe_id'
    )

    def __repr__(self):
        return f'<Equipe {self.nome}>'


class Configuracao(db.Model):
    """Modelo para configurações do sistema"""
    __tablename__ = 'configuracoes'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)
    descricao = db.Column(db.String(255))
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Configuracao {self.chave}>'

class FaixaComissao(db.Model):
    """
    Modelo para faixas de comissão configuráveis
    (DEPRECADO - usar FaixaComissaoVendedor e FaixaComissaoSupervisor)
    """
    __tablename__ = 'faixas_comissao'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)

    # Faixa de alcance
    alcance_min = db.Column(db.Float, nullable=False, default=0)  # % mínimo
    alcance_max = db.Column(db.Float, nullable=False)  # % máximo

    # Taxa de comissão
    taxa_comissao = db.Column(db.Float, nullable=False)  # valor decimal (0.01 = 1%)

    # Cor para visualização
    cor = db.Column(db.String(20), default='primary')  # danger, warning, info, success, etc

    # Ordem de exibição
    ordem = db.Column(db.Integer, default=0)

    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com empresa
    empresa = db.relationship('Empresa', backref='faixas_comissao')

    def __repr__(self):
        return f'<FaixaComissao {self.alcance_min}-{self.alcance_max}% = {self.taxa_comissao*100}%>'

    def to_dict(self):
        """Converte para dicionário para usar em JSON/API"""
        return {
            'id': self.id,
            'alcance_min': self.alcance_min,
            'alcance_max': self.alcance_max,
            'taxa_comissao': self.taxa_comissao,
            'taxa_percentual': self.taxa_comissao * 100,
            'cor': self.cor,
            'ordem': self.ordem,
            'ativa': self.ativa
        }


class FaixaComissaoVendedor(db.Model):
    """Modelo para faixas de comissão específicas de VENDEDORES"""
    __tablename__ = 'faixas_comissao_vendedor'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)

    # Faixa de alcance
    alcance_min = db.Column(db.Float, nullable=False, default=0)  # % mínimo
    alcance_max = db.Column(db.Float, nullable=False)  # % máximo

    # Taxa de comissão
    taxa_comissao = db.Column(db.Float, nullable=False)  # valor decimal (0.01 = 1%)

    # Cor para visualização
    cor = db.Column(db.String(20), default='primary')  # danger, warning, info, success, etc

    # Ordem de exibição
    ordem = db.Column(db.Integer, default=0)

    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com empresa
    empresa = db.relationship('Empresa', backref='faixas_comissao_vendedor')

    def __repr__(self):
        return f'<FaixaComissaoVendedor {self.alcance_min}-{self.alcance_max}% = {self.taxa_comissao*100}%>'

    def to_dict(self):
        """Converte para dicionário para usar em JSON/API"""
        return {
            'id': self.id,
            'alcance_min': self.alcance_min,
            'alcance_max': self.alcance_max,
            'taxa_comissao': self.taxa_comissao,
            'taxa_percentual': self.taxa_comissao * 100,
            'cor': self.cor,
            'ordem': self.ordem,
            'ativa': self.ativa,
            'tipo': 'vendedor'
        }

    def copiar_para_supervisor(self, empresa_id=None):
        """Cria uma cópia desta faixa para supervisores"""
        nova_faixa = FaixaComissaoSupervisor(
            empresa_id=empresa_id or self.empresa_id,
            alcance_min=self.alcance_min,
            alcance_max=self.alcance_max,
            taxa_comissao=self.taxa_comissao,
            cor=self.cor,
            ordem=self.ordem,
            ativa=self.ativa
        )
        return nova_faixa


class FaixaComissaoSupervisor(db.Model):
    """Modelo para faixas de comissão específicas de SUPERVISORES"""
    __tablename__ = 'faixas_comissao_supervisor'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)

    # Faixa de alcance
    alcance_min = db.Column(db.Float, nullable=False, default=0)  # % mínimo
    alcance_max = db.Column(db.Float, nullable=False)  # % máximo

    # Taxa de comissão
    taxa_comissao = db.Column(db.Float, nullable=False)  # valor decimal (0.01 = 1%)

    # Cor para visualização
    cor = db.Column(db.String(20), default='primary')  # danger, warning, info, success, etc

    # Ordem de exibição
    ordem = db.Column(db.Integer, default=0)

    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com empresa
    empresa = db.relationship('Empresa', backref='faixas_comissao_supervisor')

    def __repr__(self):
        return f'<FaixaComissaoSupervisor {self.alcance_min}-{self.alcance_max}% = {self.taxa_comissao*100}%>'

    def to_dict(self):
        """Converte para dicionário para usar em JSON/API"""
        return {
            'id': self.id,
            'alcance_min': self.alcance_min,
            'alcance_max': self.alcance_max,
            'taxa_comissao': self.taxa_comissao,
            'taxa_percentual': self.taxa_comissao * 100,
            'cor': self.cor,
            'ordem': self.ordem,
            'ativa': self.ativa,
            'tipo': 'supervisor'
        }

    def copiar_para_vendedor(self, empresa_id=None):
        """Cria uma cópia desta faixa para vendedores"""
        nova_faixa = FaixaComissaoVendedor(
            empresa_id=empresa_id or self.empresa_id,
            alcance_min=self.alcance_min,
            alcance_max=self.alcance_max,
            taxa_comissao=self.taxa_comissao,
            cor=self.cor,
            ordem=self.ordem,
            ativa=self.ativa
        )
        return nova_faixa

class FaixaComissaoManutencao(db.Model):
    """Modelo para faixas de comissão específicas de MANUTENÇÃO (técnicos)"""
    __tablename__ = 'faixas_comissao_manutencao'

    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True)

    # Faixa de alcance (percentual de cumprimento de OS/receita de manutenção)
    alcance_min = db.Column(db.Float, nullable=False, default=0)
    alcance_max = db.Column(db.Float, nullable=False)

    # Taxa de comissão
    taxa_comissao = db.Column(db.Float, nullable=False)

    # Cor para visualização
    cor = db.Column(db.String(20), default='primary')

    # Ordem de exibição
    ordem = db.Column(db.Integer, default=0)

    # Status
    ativa = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com empresa
    empresa = db.relationship('Empresa', backref='faixas_comissao_manutencao')

    def __repr__(self):
        return f'<FaixaComissaoManutencao {self.alcance_min}-{self.alcance_max}% = {self.taxa_comissao*100}%>'

    def to_dict(self):
        return {
            'id': self.id,
            'alcance_min': self.alcance_min,
            'alcance_max': self.alcance_max,
            'taxa_comissao': self.taxa_comissao,
            'taxa_percentual': self.taxa_comissao * 100,
            'cor': self.cor,
            'ordem': self.ordem,
            'ativa': self.ativa,
            'tipo': 'manutencao'
        }

class Mensagem(db.Model):
    """Modelo para sistema de mensagens entre usuários"""
    __tablename__ = 'mensagens'

    id = db.Column(db.Integer, primary_key=True)

    # Remetente e destinatário
    remetente_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False,
        index=True
    )
    destinatario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False,
        index=True
    )

    # Conteúdo da mensagem
    assunto = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

    # Status
    lida = db.Column(db.Boolean, default=False)
    data_leitura = db.Column(db.DateTime, nullable=True)
    arquivada_remetente = db.Column(db.Boolean, default=False)
    arquivada_destinatario = db.Column(db.Boolean, default=False)

    # Prioridade
    prioridade = db.Column(db.String(20), default='normal')  # 'baixa', 'normal', 'alta', 'urgente'

    # Tipo de mensagem
    tipo = db.Column(db.String(50), default='normal')  # 'normal', 'sistema', 'notificacao'

    # Auditoria
    data_envio = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Mensagem {self.id}: {self.assunto[:30]}>'

    def marcar_como_lida(self):
        """Marca a mensagem como lida"""
        if not self.lida:
            self.lida = True
            self.data_leitura = datetime.utcnow()
            db.session.commit()

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'remetente_id': self.remetente_id,
            'remetente_nome': self.remetente.nome if self.remetente else 'Sistema',
            'destinatario_id': self.destinatario_id,
            'destinatario_nome': self.destinatario.nome if self.destinatario else '',
            'assunto': self.assunto,
            'mensagem': self.mensagem,
            'lida': self.lida,
            'data_leitura': self.data_leitura.isoformat() if self.data_leitura else None,
            'prioridade': self.prioridade,
            'tipo': self.tipo,
            'data_envio': self.data_envio.isoformat()
        }


class Cliente(db.Model):
    """Modelo para cadastro de clientes dos vendedores"""
    __tablename__ = 'clientes'

    # Índices compostos para otimização de queries
    __table_args__ = (
        db.Index('idx_cliente_vendedor_ativo', 'vendedor_id', 'ativo'),
        db.Index('idx_cliente_empresa_cidade', 'empresa_id', 'cidade'),
        db.Index('idx_cliente_vendedor_status', 'vendedor_id', 'ativo', 'data_cadastro'),
        db.Index('idx_cliente_cidade_ativo', 'cidade', 'ativo'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # Dados pessoais/jurídicos
    nome = db.Column(db.String(200), nullable=False, index=True)
    razao_social = db.Column(db.String(200))  # Para CNPJ
    sigla = db.Column(db.String(50))  # Sigla/Apelido
    cpf = db.Column(db.String(14), unique=True, nullable=True, index=True)
    cnpj = db.Column(db.String(18), unique=True, nullable=True, index=True)
    inscricao_estadual = db.Column(db.String(20))  # IE
    codigo_bp = db.Column(db.String(50))  # Código BP/ERP
    codigo_cliente = db.Column(db.String(9), unique=True, index=True)  # Código único: 0001-0001

    # Endereço
    logradouro = db.Column(db.String(255))  # Endereço completo
    municipio = db.Column(db.String(100), index=True)  # Município
    bairro = db.Column(db.String(100))
    estado = db.Column(db.String(2), index=True)  # UF (ex: SP, RJ, MG)
    cep = db.Column(db.String(10))
    cidade = db.Column(db.String(100), index=True)  # Mantém para compatibilidade
    ponto_referencia = db.Column(db.String(255))
    coordenada_x = db.Column(db.String(50))  # Longitude
    coordenada_y = db.Column(db.String(50))  # Latitude
    longitude = db.Column(db.String(50))  # Campo adicional para longitude
    latitude = db.Column(db.String(50))  # Campo adicional para latitude

    # Contato
    telefone = db.Column(db.String(20), nullable=True)  # Fone(1)
    telefone2 = db.Column(db.String(20), nullable=True)  # Fone(2)
    celular = db.Column(db.String(20), nullable=True)  # Cel(1)
    celular2 = db.Column(db.String(20), nullable=True)  # Cel(2)
    email = db.Column(db.String(120), nullable=True)

    # Códigos especiais
    codigo_bw = db.Column(db.String(50), index=True)  # Código-BW

    # Formas de pagamento (armazenadas como JSON)
    # Ex: ["cartao", "pix", "dinheiro"]
    formas_pagamento = db.Column(db.Text)  # JSON array

    # Dia de visita (segunda, terça, etc ou número do dia)
    dia_visita = db.Column(db.String(50))

    # Relacionamento com vendedor
    vendedor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendedores.id'),
        nullable=True,  # Permite NULL para importação sem vendedor
        index=True
    )
    vendedor = db.relationship('Vendedor', backref='clientes')

    # Relacionamento com supervisor (opcional)
    supervisor_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=True,
        index=True
    )
    supervisor = db.relationship('Usuario', foreign_keys=[supervisor_id], backref='clientes_supervisionados')

    # Relacionamento com empresa
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey('empresas.id'),
        nullable=True,
        index=True
    )
    empresa = db.relationship('Empresa', backref='clientes')

    # Status
    ativo = db.Column(db.Boolean, default=True)

    # Observações
    observacoes = db.Column(db.Text)

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com compras
    compras = db.relationship(
        'CompraCliente',
        backref='cliente',
        lazy='dynamic',
        cascade='all, delete-orphan',
        order_by='CompraCliente.data_compra.desc()'
    )

    def get_formas_pagamento_list(self):
        """Retorna lista de formas de pagamento"""
        if not self.formas_pagamento:
            return []
        try:
            import json
            return json.loads(self.formas_pagamento)
        except Exception:
            return []

    def set_formas_pagamento_list(self, formas):
        """Define lista de formas de pagamento"""
        self.formas_pagamento = json.dumps(formas) if formas else None

    def get_ultima_compra(self):
        """Retorna a última compra do cliente"""
        return self.compras.first()

    def get_status_cor(self):
        """
        Retorna a cor do status baseado na última compra:
        - verde: comprou nos últimos 30 dias
        - amarelo: 30-38 dias sem compra
        - vermelho: mais de 38 dias sem compra
        """
        ultima_compra = self.get_ultima_compra()

        if not ultima_compra:
            return 'vermelho'

        dias_sem_compra = (datetime.utcnow() - ultima_compra.data_compra).days

        if dias_sem_compra <= 30:
            return 'verde'
        elif dias_sem_compra <= 38:
            return 'amarelo'
        else:
            return 'vermelho'

    @staticmethod
    def gerar_codigo_cliente(cidade, empresa_id):
        """
        Gera código único para cliente: 0001-0001
        - 4 primeiros dígitos: código sequencial do município (ordem de cadastro)
        - 4 últimos dígitos: sequência do cliente no município
        
        Usa lock para evitar race conditions em cadastros simultâneos.
        """
        if not cidade or cidade.strip() == '':
            cidade = 'SEM_CIDADE'

        cidade_normalizada = cidade.strip().upper()
        max_tentativas = 10
        tentativa = 0
        
        while tentativa < max_tentativas:
            tentativa += 1
            
            try:
                # 1. Tentar encontrar código de município existente para esta cidade nesta empresa
                # Busca qualquer cliente desta cidade que já tenha código gerado
                # Usa with_for_update para garantir lock
                cliente_existente = Cliente.query.filter(
                    Cliente.empresa_id == empresa_id,
                    db.func.upper(Cliente.cidade) == cidade_normalizada,
                    Cliente.codigo_cliente.isnot(None),
                    Cliente.codigo_cliente != ''
                ).order_by(Cliente.codigo_cliente.desc()).first()

                codigo_municipio = None

                if cliente_existente:
                    try:
                        # Tenta extrair o prefixo do código existente
                        partes = cliente_existente.codigo_cliente.split('-')
                        if len(partes) >= 1 and len(partes[0]) == 4 and partes[0].isdigit():
                            codigo_municipio = partes[0]
                    except Exception:
                        pass

                # 2. Se não encontrou código para a cidade, gerar novo sequencial
                if not codigo_municipio:
                    # Buscar o maior código de município (prefixo) já utilizado na empresa
                    # Filtra apenas códigos que seguem o padrão XXXX-YYYY
                    stmt = db.session.query(db.func.max(db.func.substr(Cliente.codigo_cliente, 1, 4)))\
                        .filter(Cliente.empresa_id == empresa_id)\
                        .filter(Cliente.codigo_cliente.isnot(None))\
                        .filter(Cliente.codigo_cliente.like('____-%'))

                    maior_codigo = stmt.scalar()

                    if maior_codigo and maior_codigo.isdigit():
                        proximo_codigo = int(maior_codigo) + 1
                    else:
                        proximo_codigo = 1

                    codigo_municipio = str(proximo_codigo).zfill(4)

                # 3. Gerar sequência para o cliente dentro deste município
                # Busca o último cliente com lock para evitar duplicação
                prefixo_busca = f"{codigo_municipio}-%"
                ultimo_cliente = Cliente.query.filter(
                    Cliente.empresa_id == empresa_id,
                    Cliente.codigo_cliente.like(prefixo_busca)
                ).order_by(Cliente.codigo_cliente.desc()).first()

                proxima_sequencia = 1
                if ultimo_cliente and ultimo_cliente.codigo_cliente:
                    try:
                        partes = ultimo_cliente.codigo_cliente.split('-')
                        if len(partes) == 2 and partes[0] == codigo_municipio:
                            proxima_sequencia = int(partes[1]) + 1
                    except Exception:
                        pass

                codigo_sequencia = str(proxima_sequencia).zfill(4)
                codigo_gerado = f"{codigo_municipio}-{codigo_sequencia}"
                
                # Verificar se o código já existe antes de retornar
                verificacao = Cliente.query.filter(
                    Cliente.empresa_id == empresa_id,
                    Cliente.codigo_cliente == codigo_gerado
                ).first()
                
                if not verificacao:
                    return codigo_gerado
                    
                # Se chegou aqui, o código já existe, incrementar e tentar novamente
                proxima_sequencia += 1
                codigo_sequencia = str(proxima_sequencia).zfill(4)
                return f"{codigo_municipio}-{codigo_sequencia}"
                
            except Exception as e:
                # Em caso de erro, aguardar um pouco e tentar novamente
                import time
                time.sleep(0.1 * tentativa)
                continue
        
        # Fallback: gerar código único baseado em timestamp
        import time
        timestamp = str(int(time.time() * 1000))[-8:]
        return f"{timestamp[:4]}-{timestamp[4:8]}"

    def get_total_compras_mes(self, mes=None, ano=None):
        """Retorna o total de compras no mês especificado"""
        if mes is None:
            mes = datetime.utcnow().month
        if ano is None:
            ano = datetime.utcnow().year

        from sqlalchemy import extract
        return self.compras.filter(
            extract('month', CompraCliente.data_compra) == mes,
            extract('year', CompraCliente.data_compra) == ano
        ).count()

    def pode_comprar_no_mes(self, mes=None, ano=None):
        """
        Verifica se o cliente pode fazer mais compras no mês
        Máximo: 4 compras (semanas) ou 5 se mês tiver 5 semanas
        """
        if mes is None:
            mes = datetime.utcnow().month
        if ano is None:
            ano = datetime.utcnow().year

        total_compras = self.get_total_compras_mes(mes, ano)

        # Calcular número de semanas no mês
        import calendar
        num_semanas = len(calendar.monthcalendar(ano, mes))

        return total_compras < num_semanas

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        """Converte para dicionário"""
        ultima_compra = self.get_ultima_compra()

        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'cnpj': self.cnpj,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'ponto_referencia': self.ponto_referencia,
            'telefone': self.telefone,
            'email': self.email,
            'formas_pagamento': self.get_formas_pagamento_list(),
            'dia_visita': self.dia_visita,
            'vendedor_id': self.vendedor_id,
            'vendedor_nome': self.vendedor.nome if self.vendedor else '',
            'ativo': self.ativo,
            'observacoes': self.observacoes,
            'data_cadastro': self.data_cadastro.isoformat(),
            'status_cor': self.get_status_cor(),
            'ultima_compra': ultima_compra.data_compra.isoformat() if ultima_compra else None,
            'total_compras_mes': self.get_total_compras_mes()
        }


class CompraCliente(db.Model):
    """Modelo para registrar compras dos clientes"""
    __tablename__ = 'compras_clientes'

    # Índices compostos para otimização de queries e relatórios
    __table_args__ = (
        db.Index('idx_compra_vendedor_data', 'vendedor_id', 'data_compra'),
        db.Index('idx_compra_cliente_data', 'cliente_id', 'data_compra'),
        db.Index('idx_compra_empresa_data', 'empresa_id', 'data_compra'),
        db.Index('idx_compra_data_vendedor_valor', 'data_compra', 'vendedor_id', 'valor'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # Relacionamento com cliente
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id'),
        nullable=False,
        index=True
    )

    # Relacionamento com vendedor (redundante, mas útil para relatórios)
    vendedor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendedores.id'),
        nullable=False,
        index=True
    )
    vendedor = db.relationship('Vendedor', backref='compras_realizadas')

    # Relacionamento com empresa
    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey('empresas.id'),
        nullable=True,
        index=True
    )
    empresa = db.relationship('Empresa', backref='compras')

    # Dados da compra
    valor = db.Column(db.Float, default=0.0)
    forma_pagamento = db.Column(db.String(50))  # cartao, pix, dinheiro

    # Data da compra
    data_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Observações
    observacoes = db.Column(db.Text)

    # Auditoria
    data_registro = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CompraCliente cliente_id={self.cliente_id} data={self.data_compra}>'

    def to_dict(self):
        """Converte para dicionário"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else '',
            'vendedor_id': self.vendedor_id,
            'vendedor_nome': self.vendedor.nome if self.vendedor else '',
            'valor': self.valor,
            'forma_pagamento': self.forma_pagamento,
            'data_compra': self.data_compra.isoformat(),
            'observacoes': self.observacoes
        }

# ============================================================================
# MÓDULO DE ESTOQUE E MANUTENÇÃO
# ============================================================================

# ============================================================================

class Produto(db.Model):
    """Modelo para cadastro de produtos do estoque"""
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)

    # Identificação
    codigo = db.Column(db.String(50), unique=True, nullable=False, index=True)
    codigo_barra = db.Column(db.String(100), index=True)  # EAN, UPC, Code128, etc
    referencia = db.Column(db.String(100))  # Referência do fabricante
    ncm = db.Column(db.String(20))  # Nomenclatura Comum do Mercosul
    nome = db.Column(db.String(200), nullable=False, index=True)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(100))  # Peças, Equipamentos, Consumíveis, etc
    fornecedor = db.Column(db.String(200))  # Fornecedor principal

    # Controle de estoque
    unidade = db.Column(db.String(20), default='UN')  # UN, KG, MT, CX, etc
    estoque_minimo = db.Column(db.Float, default=0)
    estoque_atual = db.Column(db.Float, default=0)

    # Valores
    custo_medio = db.Column(db.Float, default=0)
    preco_venda = db.Column(db.Float, default=0)
    preco_servico = db.Column(db.Float, default=0)  # Preço do serviço

    # Localização
    localizacao = db.Column(db.String(100))  # Prateleira, Corredor, etc

    # Status
    ativo = db.Column(db.Boolean, default=True)

    # Empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True, index=True)
    empresa = db.relationship('Empresa', backref='produtos')

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    movimentos = db.relationship('EstoqueMovimento', backref='produto', lazy='dynamic')

    def __repr__(self):
        return f'<Produto {self.codigo} - {self.nome}>'

    def get_status_estoque(self):
        """Retorna status do estoque (baixo, normal, alto)"""
        if self.estoque_atual <= 0:
            return 'zerado'
        elif self.estoque_atual <= self.estoque_minimo:
            return 'baixo'
        elif self.estoque_atual <= (self.estoque_minimo * 1.5):
            return 'atencao'
        else:
            return 'normal'

    def get_cor_status(self):
        """Retorna cor Bootstrap baseada no status"""
        status = self.get_status_estoque()
        cores = {
            'zerado': 'danger',
            'baixo': 'warning',
            'atencao': 'info',
            'normal': 'success'
        }

        return cores.get(status, 'secondary')

class EstoqueMovimento(db.Model):
    """Modelo para movimentação de estoque (entrada/saída)"""
    __tablename__ = 'estoque_movimentos'

    id = db.Column(db.Integer, primary_key=True)

    # Produto
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False, index=True)

    # Tipo de movimento
    tipo = db.Column(db.String(20), nullable=False)  # entrada, saida
    motivo = db.Column(db.String(50), nullable=False)  # compra, venda, manutencao, ajuste, devolucao

    # Quantidade e valores
    quantidade = db.Column(db.Float, nullable=False)
    valor_unitario = db.Column(db.Float, default=0)
    valor_total = db.Column(db.Float, default=0)

    # Documentação
    documento = db.Column(db.String(100))  # Nota fiscal, OS, etc
    observacoes = db.Column(db.Text)

    # Relacionamentos
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordens_servico.id'), nullable=True, index=True)
    fornecedor = db.Column(db.String(200))  # Para compras
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True, index=True)
    cliente = db.relationship('Cliente', backref='movimentos_estoque')

    # Responsável
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    usuario = db.relationship('Usuario', backref='movimentos_estoque')

    # Empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True, index=True)
    empresa = db.relationship('Empresa', backref='movimentos_estoque')

    # Auditoria
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f'<EstoqueMovimento {self.tipo} - {self.produto_id} - {self.quantidade}>'

    def get_icone(self):
        """Retorna ícone Bootstrap para o tipo de movimento"""
        if self.tipo == 'entrada':
            return 'bi-arrow-down-circle-fill text-success'

        else:
            return 'bi-arrow-up-circle-fill text-danger'

class Tecnico(db.Model):
    """Modelo para técnicos de manutenção"""
    __tablename__ = 'tecnicos'

    id = db.Column(db.Integer, primary_key=True)

    # Dados pessoais
    nome = db.Column(db.String(200), nullable=False, index=True)
    cpf = db.Column(db.String(14), unique=True, index=True)
    email = db.Column(db.String(120), index=True)
    telefone = db.Column(db.String(20))
    celular = db.Column(db.String(20))

    # Especialidades
    especialidades = db.Column(db.Text)  # JSON: ["Elétrica", "Mecânica", "Hidráulica"]

    # Supervisor
    supervisor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    supervisor = db.relationship('Usuario', foreign_keys=[supervisor_id], backref='tecnicos_supervisionados')

    # Usuário do sistema (se tiver acesso)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id], backref='tecnico_perfil')

    # Empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True, index=True)
    empresa = db.relationship('Empresa', backref='tecnicos')

    # Faixa de comissão de manutenção associada
    faixa_manutencao_id = db.Column(db.Integer, db.ForeignKey('faixas_comissao_manutencao.id'), nullable=True, index=True)
    faixa_manutencao = db.relationship('FaixaComissaoManutencao', backref='tecnicos_associados')

    # Status
    ativo = db.Column(db.Boolean, default=True)
    disponivel = db.Column(db.Boolean, default=True)  # Se está disponível para novas OS

    # Estatísticas
    total_os = db.Column(db.Integer, default=0)
    os_concluidas = db.Column(db.Integer, default=0)
    avaliacao_media = db.Column(db.Float, default=0)

    # Auditoria
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    data_atualizacao = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    ordens_servico = db.relationship('OrdemServico', backref='tecnico', lazy='dynamic')

    def __repr__(self):
        return f'<Tecnico {self.nome}>'

    def get_taxa_conclusao(self):
        """Retorna taxa de conclusão de OS"""
        if self.total_os == 0:
            return 0

        return round((self.os_concluidas / self.total_os) * 100, 1)

class OrdemServico(db.Model):
    """Modelo para Ordens de Serviço (OS)"""
    __tablename__ = 'ordens_servico'

    id = db.Column(db.Integer, primary_key=True)

    # Número da OS (gerado automaticamente)
    numero_os = db.Column(db.String(20), unique=True, nullable=False, index=True)

    # Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False, index=True)
    cliente = db.relationship('Cliente', backref='ordens_servico')

    # Técnico
    tecnico_id = db.Column(db.Integer, db.ForeignKey('tecnicos.id'), nullable=True, index=True)

    # Descrição
    titulo = db.Column(db.String(200), nullable=False)
    descricao_problema = db.Column(db.Text, nullable=False)
    descricao_solucao = db.Column(db.Text)

    # Prioridade
    prioridade = db.Column(db.String(20), default='normal')  # baixa, normal, alta, urgente

    # Status
    status = db.Column(db.String(30), default='aguardando_aprovacao', nullable=False, index=True)
    # Status: aguardando_aprovacao, aprovada, em_andamento, aguardando_peca, concluida, cancelada

    # Datas
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    data_aprovacao = db.Column(db.DateTime)
    data_inicio = db.Column(db.DateTime)
    data_previsao = db.Column(db.DateTime)
    data_conclusao = db.Column(db.DateTime)

    # Valores
    valor_mao_obra = db.Column(db.Float, default=0)
    valor_pecas = db.Column(db.Float, default=0)
    valor_total = db.Column(db.Float, default=0)

    # Aprovação
    aprovada_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True, index=True)
    aprovada_por = db.relationship('Usuario', foreign_keys=[aprovada_por_id], backref='os_aprovadas')
    motivo_reprovacao = db.Column(db.Text)

    # Feedback e avaliação
    feedback_tecnico = db.Column(db.Text)
    avaliacao_cliente = db.Column(db.Integer)  # 1-5 estrelas
    comentario_cliente = db.Column(db.Text)

    # Criação
    criada_por_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    criada_por = db.relationship('Usuario', foreign_keys=[criada_por_id], backref='os_criadas')

    # Empresa
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=True, index=True)
    empresa = db.relationship('Empresa', backref='ordens_servico')

    # Relacionamentos
    movimentos_estoque = db.relationship('EstoqueMovimento', backref='ordem_servico', lazy='dynamic')

    def __repr__(self):
        return f'<OrdemServico {self.numero_os}>'

    def get_cor_status(self):
        """Retorna cor Bootstrap baseada no status"""
        cores = {
            'aguardando_aprovacao': 'warning',
            'aprovada': 'info',
            'em_andamento': 'primary',
            'aguardando_peca': 'secondary',
            'concluida': 'success',
            'cancelada': 'danger'
        }
        return cores.get(self.status, 'secondary')

    def get_cor_prioridade(self):
        """Retorna cor Bootstrap baseada na prioridade"""
        cores = {
            'baixa': 'secondary',
            'normal': 'info',
            'alta': 'warning',
            'urgente': 'danger'
        }
        return cores.get(self.prioridade, 'secondary')

    def pode_aprovar(self, usuario):
        """Verifica se usuário pode aprovar a OS"""
        return (
            usuario.cargo in ['admin', 'gerente_manutencao', 'supervisor_manutencao']
            or usuario.is_super_admin
        )

    def pode_editar(self, usuario):
        """Verifica se usuário pode editar a OS"""
        if usuario.is_super_admin or usuario.cargo in ['admin', 'gerente_manutencao']:
            return True
        if usuario.cargo == 'supervisor_manutencao':
            return True
        if usuario.cargo == 'administrativo' and self.status == 'aguardando_aprovacao':
            return True
        if usuario.cargo == 'tecnico' and self.tecnico and self.tecnico.usuario_id == usuario.id:
            return self.status in ['aprovada', 'em_andamento', 'aguardando_peca']
        return False

    @staticmethod
    def gerar_numero_os(empresa_id):
        """Gera número sequencial de OS"""
        # Formato: OS-YYYY-NNNN (ex: OS-2025-0001)
        ano = datetime.utcnow().year
        ultima_os = OrdemServico.query.filter(
            OrdemServico.numero_os.like(f'OS-{ano}-%'),
            OrdemServico.empresa_id == empresa_id
        ).order_by(OrdemServico.id.desc()).first()

        if ultima_os:
            ultimo_numero = int(ultima_os.numero_os.split('-')[-1])
            proximo_numero = ultimo_numero + 1
        else:
            proximo_numero = 1

        return f'OS-{ano}-{proximo_numero:04d}'

