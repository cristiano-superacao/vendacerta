# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, IntegerField, BooleanField, SelectMultipleField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from models import Usuario, Vendedor, Equipe, Empresa, Cliente
import re

class LoginForm(FlaskForm):
    """Formulário de login"""
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória')
    ])

class RegistroForm(FlaskForm):
    """Formulário de registro de nova empresa e usuário administrador"""
    # Dados do Usuário
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    senha = PasswordField('Senha', validators=[
        DataRequired(message='Senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('senha', message='As senhas não coincidem')
    ])

    # Dados da Empresa
    nome_empresa = StringField('Nome da Empresa', validators=[
        DataRequired(message='Nome da empresa é obrigatório'),
        Length(min=3, max=200, message='Nome deve ter entre 3 e 200 caracteres')
    ])
    cnpj = StringField('CNPJ', validators=[
        DataRequired(message='CNPJ é obrigatório'),
        Length(min=14, max=18, message='CNPJ inválido')
    ])
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório')
    ])

    def validate_email(self, email):
        """Valida se o email já existe"""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está cadastrado.')

    def validate_cnpj(self, cnpj):
        """Valida se o CNPJ já existe"""
        # Remover caracteres não numéricos
        cnpj_limpo = re.sub(r'\D', '', cnpj.data)
        empresa = Empresa.query.filter_by(cnpj=cnpj_limpo).first()
        # Também verificar com formatação original por segurança
        empresa_raw = Empresa.query.filter_by(cnpj=cnpj.data).first()

        if empresa or empresa_raw:
            raise ValidationError('Este CNPJ já está cadastrado.')

class UsuarioForm(FlaskForm):
    """Formulário de gerenciamento de usuários pelo super admin"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    cargo = SelectField('Cargo', choices=[
        ('usuario', 'Usuário'),
        ('auxiliar', 'Auxiliar'),
        ('vendedor', 'Vendedor'),
        ('supervisor', 'Supervisor de Vendas'),
        ('supervisor_manutencao', 'Supervisor de Manutenção'),
        ('gerente_manutencao', 'Gerente de Manutenção'),
        ('gerente', 'Gerente'),
        ('administrativo', 'Administrativo'),
        ('tecnico', 'Técnico'),
        ('admin', 'Administrador')
    ], validators=[DataRequired()])
    empresa_id = SelectField('Empresa', coerce=int, validators=[
        DataRequired(message='Empresa é obrigatória')
    ])
    ativo = SelectField('Status', choices=[
        ('1', 'Ativo'),
        ('0', 'Inativo')
    ], default='1', coerce=int)
    bloqueado = SelectField('Bloqueado', choices=[
        ('0', 'Não'),
        ('1', 'Sim')
    ], default='0', coerce=int)
    motivo_bloqueio = TextAreaField('Motivo do Bloqueio', validators=[Optional()])

    def __init__(self, usuario_id=None, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.usuario_id = usuario_id

    def validate_email(self, email):
        """Valida se o email já existe"""
        from models import Usuario
        try:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario and (self.usuario_id is None or usuario.id != self.usuario_id):
                raise ValidationError('Este email já está cadastrado.')
        except Exception as e:
            # Se houver erro na consulta, registra mas não bloqueia
            print(f'Erro ao validar email: {str(e)}')
            pass

class VendedorForm(FlaskForm):
    """Formulário de cadastro de vendedor"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    telefone = StringField('Telefone', validators=[
        Optional(),
        Length(max=20)
    ])
    cpf = StringField('CPF', validators=[
        Optional(),
        Length(min=11, max=14, message='CPF inválido')
    ])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[Optional()])
    equipe_id = SelectField('Equipe', coerce=int, validators=[Optional()])

    def __init__(self, vendedor_id=None, *args, **kwargs):
        super(VendedorForm, self).__init__(*args, **kwargs)
        self.vendedor_id = vendedor_id

    def validate_email(self, email):
        """Valida se o email já existe (ignora próprio registro em edição)"""
        vendedor = Vendedor.query.filter_by(email=email.data).first()
        if vendedor and (self.vendedor_id is None or vendedor.id != self.vendedor_id):
            raise ValidationError('Este email já está cadastrado.')

    def validate_cpf(self, cpf):
        """Valida formato do CPF (ignora próprio registro em edição)"""
        if cpf.data:
            # Remove caracteres não numéricos
            cpf_numeros = re.sub(r'\D', '', cpf.data)
            if len(cpf_numeros) != 11:
                raise ValidationError('CPF deve ter 11 dígitos.')

            # Verifica se já existe (ignora próprio registro)
            vendedor = Vendedor.query.filter_by(cpf=cpf.data).first()
            if vendedor and (self.vendedor_id is None or vendedor.id != self.vendedor_id):
                raise ValidationError('Este CPF já está cadastrado.')

class MetaForm(FlaskForm):
    """Formulário de cadastro/edição de meta"""
    vendedor_id = SelectField('Vendedor', coerce=int, validators=[
        DataRequired(message='Vendedor é obrigatório')
    ])
    mes = SelectField('Mês', coerce=int, choices=[
        (1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'),
        (4, 'Abril'), (5, 'Maio'), (6, 'Junho'),
        (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'),
        (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')
    ], validators=[DataRequired(message='Mês é obrigatório')])
    ano = IntegerField('Ano', validators=[
        DataRequired(message='Ano é obrigatório')
    ])
    valor_meta = FloatField('Valor da Meta (R$)', validators=[
        DataRequired(message='Valor da meta é obrigatório')
    ])
    receita_alcancada = FloatField('Receita Alcançada (R$)', validators=[
        Optional()
    ], default=0.0)
    status_comissao = SelectField('Status da Comissão', choices=[
        ('Pendente', 'Pendente'),
        ('Aprovado', 'Aprovado'),
        ('Pago', 'Pago')
    ], default='Pendente')
    observacoes = TextAreaField('Observações', validators=[Optional()])

class AtualizarReceitaForm(FlaskForm):
    """Formulário simplificado para atualizar receita"""
    receita_alcancada = FloatField('Receita Alcançada (R$)', validators=[
        DataRequired(message='Receita é obrigatória')
    ])
    observacoes = TextAreaField('Observações', validators=[Optional()])

class RecuperarSenhaForm(FlaskForm):
    """Formulário de recuperação de senha"""
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])

class RedefinirSenhaForm(FlaskForm):
    """Formulário de redefinição de senha"""
    nova_senha = PasswordField('Nova Senha', validators=[
        DataRequired(message='Nova senha é obrigatória'),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[
        DataRequired(message='Confirmação de senha é obrigatória'),
        EqualTo('nova_senha', message='As senhas não coincidem')
    ])

class EquipeForm(FlaskForm):
    """Formulário de cadastro de equipe"""
    nome = StringField('Nome da Equipe', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres')
    ])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[
        DataRequired(message='Supervisor é obrigatório')
    ])

    def __init__(self, equipe_id=None, *args, **kwargs):
        super(EquipeForm, self).__init__(*args, **kwargs)
        self.equipe_id = equipe_id

    def validate_nome(self, nome):
        """Valida se o nome da equipe já existe (ignora próprio registro em edição)"""
        equipe = Equipe.query.filter_by(nome=nome.data).first()
        if equipe and (self.equipe_id is None or equipe.id != self.equipe_id):
            raise ValidationError('Já existe uma equipe com este nome.')

class EmpresaForm(FlaskForm):
    """Formulário de cadastro de empresa"""
    nome = StringField('Nome da Empresa', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=200, message='Nome deve ter entre 3 e 200 caracteres')
    ])
    cnpj = StringField('CNPJ', validators=[
        DataRequired(message='CNPJ é obrigatório'),
        Length(min=14, max=18, message='CNPJ inválido')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    telefone = StringField('Telefone', validators=[Optional()])
    endereco = StringField('Endereço', validators=[Optional()])
    cidade = StringField('Cidade', validators=[Optional()])
    estado = StringField('Estado', validators=[
        Optional(),
        Length(max=2, message='Use a sigla do estado (ex: BA)')
    ])
    plano = SelectField('Plano', choices=[
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise')
    ], default='basico')
    max_usuarios = IntegerField('Máximo de Usuários', validators=[
        DataRequired(message='Limite de usuários é obrigatório')
    ], default=10)
    max_vendedores = IntegerField('Máximo de Vendedores', validators=[
        DataRequired(message='Limite de vendedores é obrigatório')
    ], default=50)

    def __init__(self, empresa_id=None, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.empresa_id = empresa_id

    def validate_cnpj(self, cnpj):
        """Valida formato e unicidade do CNPJ"""
        # Remove caracteres não numéricos
        cnpj_numbers = re.sub(r'\D', '', cnpj.data)

        # Verifica se tem 14 dígitos
        if len(cnpj_numbers) != 14:
            raise ValidationError('CNPJ deve ter 14 dígitos')

        # Verifica se já existe (ignora próprio registro em edição)
        from models import Empresa
        empresa = Empresa.query.filter_by(cnpj=cnpj_numbers).first()
        if empresa and (self.empresa_id is None or empresa.id != self.empresa_id):
            raise ValidationError('Este CNPJ já está cadastrado.')

class ClienteForm(FlaskForm):
    """Formulário de cadastro de cliente"""
    # Identificação
    vendedor_id = SelectField('Vendedor', coerce=int, validators=[
        DataRequired(message='Vendedor é obrigatório')
    ])

    supervisor_id = SelectField('Supervisor', coerce=int, validators=[Optional()])

    supervisor_nome = StringField('Supervisor', validators=[Optional()], render_kw={'readonly': True})

    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=200, message='Nome deve ter entre 3 e 200 caracteres')
    ])

    razao_social = StringField('Razão Social', validators=[
        Optional(),
        Length(max=200)
    ])

    sigla = StringField('Sigla/Apelido', validators=[
        Optional(),
        Length(max=50)
    ])

    # Documentos
    cpf = StringField('CPF', validators=[
        Optional(),
        Length(min=11, max=14, message='CPF inválido')
    ])

    cnpj = StringField('CNPJ', validators=[
        Optional(),
        Length(min=14, max=18, message='CNPJ inválido')
    ])

    inscricao_estadual = StringField('Inscr. Estadual', validators=[
        Optional(),
        Length(max=20)
    ])

    codigo_bp = StringField('Código BP', validators=[
        Optional(),
        Length(max=50)
    ])

    # Endereço
    logradouro = StringField('Logradouro', validators=[
        Optional(),
        Length(max=255)
    ])

    municipio = StringField('Município', validators=[
        Optional(),
        Length(max=100)
    ])

    bairro = StringField('Bairro', validators=[
        Optional(),
        Length(max=100)
    ])

    estado = SelectField('Estado (UF)', choices=[
        ('', 'Selecione...'),
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], validators=[Optional()])

    cep = StringField('CEP', validators=[
        Optional(),
        Length(max=10)
    ])

    cidade = StringField('Cidade (legado)', validators=[
        Optional(),
        Length(max=100)
    ], render_kw={'style': 'display:none;'})

    ponto_referencia = StringField('Ponto de Referência', validators=[
        Optional(),
        Length(max=255)
    ])

    # Coordenadas
    coordenada_x = StringField('Coordenada X (Longitude)', validators=[
        Optional(),
        Length(max=50)
    ])

    coordenada_y = StringField('Coordenada Y (Latitude)', validators=[
        Optional(),
        Length(max=50)
    ])

    longitude = StringField('Longitude', validators=[
        Optional(),
        Length(max=50)
    ])

    latitude = StringField('Latitude', validators=[
        Optional(),
        Length(max=50)
    ])

    # Contato
    telefone = StringField('Fone (1)', validators=[
        Optional(),
        Length(max=20)
    ])

    telefone2 = StringField('Fone (2)', validators=[
        Optional(),
        Length(max=20)
    ])

    celular = StringField('Cel (1)', validators=[
        Optional(),
        Length(max=20)
    ])

    celular2 = StringField('Cel (2)', validators=[
        Optional(),
        Length(max=20)
    ])

    email = StringField('Email', validators=[
        Optional(),
        Email(message='Email inválido')
    ])

    # Código especial
    codigo_bw = StringField('Código-BW', validators=[
        Optional(),
        Length(max=50)
    ])

    # Formas de pagamento (múltipla escolha)
    formas_pagamento = SelectMultipleField('Formas de Pagamento', choices=[
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
        ('boleto', 'Boleto')
    ], validators=[Optional()])

    dia_visita = SelectField('Dia da Visita', choices=[
        ('', 'Selecione...'),
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ], validators=[Optional()])

    observacoes = TextAreaField('Observações', validators=[Optional()])

    ativo = BooleanField('Cliente Ativo', default=True)

    def __init__(self, cliente_id=None, empresa_id=None, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.cliente_id = cliente_id
        self.empresa_id = empresa_id

        # Popula lista de vendedores da empresa
        if empresa_id:
            vendedores = Vendedor.query.filter_by(
                empresa_id=empresa_id,
                ativo=True
            ).order_by(Vendedor.nome).all()
            self.vendedor_id.choices = [(v.id, v.nome) for v in vendedores]
            
            # Popula lista de supervisores da empresa
            from models import Usuario
            supervisores = Usuario.query.filter_by(
                empresa_id=empresa_id,
                cargo='supervisor',
                ativo=True
            ).order_by(Usuario.nome).all()
            # Usa 0 para representar "Nenhum" e evitar erro de conversão int('')
            self.supervisor_id.choices = [(0, 'Nenhum')] + [(s.id, s.nome) for s in supervisores]
        else:
            self.vendedor_id.choices = []
            # Lista padrão quando não há empresa: apenas opção "Nenhum"
            self.supervisor_id.choices = [(0, 'Nenhum')]

    def validate(self, extra_validators=None):
        """Validação customizada: CPF OU CNPJ deve ser preenchido"""
        if not super(ClienteForm, self).validate(extra_validators):
            return False

        if not self.cpf.data and not self.cnpj.data:
            self.cpf.errors.append('Preencha CPF ou CNPJ')
            self.cnpj.errors.append('Preencha CPF ou CNPJ')
            return False

        return True

    def validate_cpf(self, cpf):
        """Valida formato e unicidade do CPF"""
        if cpf.data:
            # Remove caracteres não numéricos
            cpf_numbers = re.sub(r'\D', '', cpf.data)

            if len(cpf_numbers) != 11:
                raise ValidationError('CPF deve ter 11 dígitos')

            # Verifica se já existe (ignora próprio registro em edição)
            cliente = Cliente.query.filter_by(cpf=cpf_numbers).first()
            if cliente and (self.cliente_id is None or cliente.id != self.cliente_id):
                raise ValidationError('Este CPF já está cadastrado.')

    def validate_cnpj(self, cnpj):
        """Valida formato e unicidade do CNPJ"""
        if cnpj.data:
            # Remove caracteres não numéricos
            cnpj_numbers = re.sub(r'\D', '', cnpj.data)

            if len(cnpj_numbers) != 14:
                raise ValidationError('CNPJ deve ter 14 dígitos')

            # Verifica se já existe (ignora próprio registro em edição)
            cliente = Cliente.query.filter_by(cnpj=cnpj_numbers).first()
            if cliente and (self.cliente_id is None or cliente.id != self.cliente_id):
                raise ValidationError('Este CNPJ já está cadastrado.')

class CompraClienteForm(FlaskForm):
    """Formulário de registro de compra do cliente"""
    cliente_id = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message='Cliente é obrigatório')
    ])

    valor = FloatField('Valor da Compra (R$)', validators=[
        DataRequired(message='Valor é obrigatório')
    ])

    forma_pagamento = SelectField('Forma de Pagamento', choices=[
        ('', 'Selecione...'),
        ('cartao', 'Cartão'),
        ('pix', 'PIX'),
        ('dinheiro', 'Dinheiro'),
        ('boleto', 'Boleto')
    ], validators=[DataRequired(message='Forma de pagamento é obrigatória')])

    observacoes = TextAreaField('Observações', validators=[Optional()])

class FiltroClienteForm(FlaskForm):
    """Formulário de filtros para listagem de clientes"""
    status = SelectField('Status', choices=[
        ('todos', 'Todos'),
        ('verde', 'Positivados (Verde)'),
        ('amarelo', 'Atenção (Amarelo)'),
        ('vermelho', 'Sem Compras (Vermelho)')
    ], default='todos')

    cidade = StringField('Cidade', validators=[Optional()])

    bairro = StringField('Bairro', validators=[Optional()])

    dia_visita = SelectField('Dia da Visita', choices=[
        ('', 'Todos'),
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
        ('domingo', 'Domingo')
    ], validators=[Optional()])

# ============================================================================
# FORMULÁRIOS DE ESTOQUE E MANUTENÇÃO
# ============================================================================

class ProdutoForm(FlaskForm):
    """Formulário para cadastro/edição de produtos"""
    codigo = StringField('Código do Produto', validators=[
        DataRequired(message='Código é obrigatório'),
        Length(max=50, message='Código deve ter no máximo 50 caracteres')
    ])
    codigo_barra = StringField('Código de Barras (EAN/UPC)', validators=[
        Optional(),
        Length(max=100, message='Código de barras deve ter no máximo 100 caracteres')
    ])
    referencia = StringField('Referência do Fabricante', validators=[
        Optional(),
        Length(max=100, message='Referência deve ter no máximo 100 caracteres')
    ])
    ncm = StringField('NCM (Código Fiscal)', validators=[
        Optional(),
        Length(max=20, message='NCM deve ter no máximo 20 caracteres')
    ])
    nome = StringField('Nome do Produto', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(max=200, message='Nome deve ter no máximo 200 caracteres')
    ])
    descricao = TextAreaField('Descrição', validators=[Optional()])
    categoria = SelectField('Categoria', choices=[
        ('pecas', 'Peças'),
        ('equipamentos', 'Equipamentos'),
        ('consumiveis', 'Consumíveis'),
        ('ferramentas', 'Ferramentas'),
        ('outros', 'Outros')
    ], validators=[Optional()])
    fornecedor = StringField('Fornecedor Principal', validators=[
        Optional(),
        Length(max=200, message='Fornecedor deve ter no máximo 200 caracteres')
    ])
    unidade = SelectField('Unidade', choices=[
        ('UN', 'Unidade'),
        ('CX', 'Caixa'),
        ('KG', 'Quilograma'),
        ('MT', 'Metro'),
        ('LT', 'Litro'),
        ('PC', 'Peça'),
        ('KIT', 'Kit')
    ], default='UN', validators=[DataRequired()])
    estoque_minimo = FloatField('Estoque Mínimo', validators=[Optional()], default=0)
    custo_medio = FloatField('Custo Médio (R$)', validators=[Optional()], default=0)
    preco_venda = FloatField('Preço de Venda (R$)', validators=[Optional()], default=0)
    preco_servico = FloatField('Preço do Serviço (R$)', validators=[Optional()], default=0)
    localizacao = StringField('Localização no Estoque', validators=[Optional(), Length(max=100)])
    ativo = BooleanField('Produto Ativo', default=True)
    submit = SubmitField('Salvar Produto')

class EstoqueMovimentoForm(FlaskForm):
    """Formulário para movimentação de estoque"""
    produto_id = SelectField('Produto', coerce=int, validators=[DataRequired(message='Selecione um produto')])
    tipo = SelectField('Tipo de Movimento', choices=[
        ('entrada', 'Entrada'),
        ('saida', 'Saída')
    ], validators=[DataRequired()])
    motivo = SelectField('Motivo', coerce=str, validators=[DataRequired(message='Selecione o motivo')])
    quantidade = FloatField('Quantidade', validators=[
        DataRequired(message='Quantidade é obrigatória')
    ])
    valor_unitario = FloatField('Valor Unitário (R$)', validators=[Optional()], default=0)
    documento = StringField('Documento (NF, OS, etc)', validators=[Optional(), Length(max=100)])
    fornecedor = StringField('Fornecedor', validators=[Optional(), Length(max=200)])
    cliente_id = SelectField('Cliente', coerce=int, validators=[Optional()])
    ordem_servico_id = SelectField('Ordem de Serviço', coerce=int, validators=[Optional()])
    observacoes = TextAreaField('Observações', validators=[Optional()])

class TecnicoForm(FlaskForm):
    """Formulário para cadastro/edição de técnicos"""
    nome = StringField('Nome Completo', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(max=200, message='Nome deve ter no máximo 200 caracteres')
    ])
    cpf = StringField('CPF', validators=[
        DataRequired(message='CPF é obrigatório'),
        Length(min=11, max=14, message='CPF inválido')
    ])
    email = StringField('Email', validators=[
        Optional(),
        Email(message='Email inválido'),
        Length(max=120)
    ])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    celular = StringField('Celular', validators=[Optional(), Length(max=20)])
    especialidades = TextAreaField('Especialidades (uma por linha)', validators=[Optional()])
    supervisor_id = SelectField('Supervisor de Manutenção', coerce=int, validators=[Optional()])
    usuario_id = SelectField('Usuário do Sistema (Opcional)', coerce=int, validators=[Optional()])
    ativo = BooleanField('Técnico Ativo', default=True)
    disponivel = BooleanField('Disponível para Novas OS', default=True)

class OrdemServicoForm(FlaskForm):
    """Formulário para criação/edição de Ordem de Serviço"""
    cliente_id = SelectField('Cliente', coerce=int, validators=[
        DataRequired(message='Selecione um cliente')
    ])
    titulo = StringField('Título da OS', validators=[
        DataRequired(message='Título é obrigatório'),
        Length(max=200, message='Título deve ter no máximo 200 caracteres')
    ])
    descricao_problema = TextAreaField('Descrição do Problema', validators=[
        DataRequired(message='Descrição do problema é obrigatória')
    ])
    prioridade = SelectField('Prioridade', choices=[
        ('baixa', 'Baixa'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente')
    ], default='normal', validators=[DataRequired()])
    tecnico_id = SelectField('Técnico Responsável', coerce=int, validators=[Optional()])
    submit = SubmitField('Criar Ordem de Serviço')


class OrdemServicoAvaliarForm(FlaskForm):
    """Formulário para aprovação de OS (Supervisor)"""
    aprovar = BooleanField('Aprovar OS')
    motivo_reprovacao = TextAreaField('Motivo da Reprovação (se reprovar)', validators=[Optional()])
    tecnico_id = SelectField('Atribuir Técnico', coerce=int, validators=[Optional()])
    data_previsao = StringField('Previsão de Conclusão', validators=[Optional()])

class OrdemServicoAndamentoForm(FlaskForm):
    """Formulário para atualização de andamento (Técnico)"""
    status = SelectField('Status', choices=[
        ('em_andamento', 'Em Andamento'),
        ('aguardando_peca', 'Aguardando Peça'),
        ('concluida', 'Concluída')
    ], validators=[DataRequired()])
    data_previsao = DateField('Previsão de Conclusão', format='%Y-%m-%d', validators=[Optional()])
    descricao_solucao = TextAreaField('Descrição da Solução', validators=[Optional()])
    feedback_tecnico = TextAreaField('Feedback do Técnico', validators=[Optional()])
    valor_mao_obra = FloatField('Valor Mão de Obra (R$)', validators=[Optional()], default=0)
    valor_pecas = FloatField('Valor Peças (R$)', validators=[Optional()], default=0)
    submit = SubmitField('Atualizar Ordem de Serviço')

class OrdemServicoAvaliacaoForm(FlaskForm):
    """Formulário para avaliação do cliente"""
    avaliacao_cliente = SelectField('Avaliação', choices=[
        ('5', '⭐⭐⭐⭐⭐ Excelente'),
        ('4', '⭐⭐⭐⭐ Muito Bom'),
        ('3', '⭐⭐⭐ Bom'),
        ('2', '⭐⭐ Regular'),
        ('1', '⭐ Ruim')
    ], coerce=int, validators=[DataRequired()])
    comentario_cliente = TextAreaField('Comentário', validators=[Optional()])
# Adicionar ao final de forms.py

class UsuarioPermissoesForm(FlaskForm):
    """Formulário para configurar permissões granulares de um usuário"""

    # Permissões Gerais
    pode_ver_dashboard = BooleanField('Ver Dashboard')
    pode_enviar_mensagens = BooleanField('Enviar Mensagens')
    pode_exportar_dados = BooleanField('Exportar Dados')

    # Permissões de Vendas
    pode_gerenciar_vendedores = BooleanField('Gerenciar Vendedores')
    pode_gerenciar_metas = BooleanField('Gerenciar Metas')
    pode_gerenciar_equipes = BooleanField('Gerenciar Equipes')
    pode_gerenciar_comissoes = BooleanField('Gerenciar Comissões')
    pode_ver_todas_metas = BooleanField('Ver Todas as Metas')
    pode_aprovar_comissoes = BooleanField('Aprovar Comissões')

    # Permissões de Clientes
    pode_acessar_clientes = BooleanField('Acessar Módulo de Clientes')
    pode_criar_clientes = BooleanField('Criar Novos Clientes')
    pode_editar_clientes = BooleanField('Editar Clientes')
    pode_excluir_clientes = BooleanField('Excluir Clientes')
    pode_importar_clientes = BooleanField('Importar Clientes')

    # Permissões de Ordens de Serviço
    pode_acessar_os = BooleanField('Acessar Módulo de OS')
    pode_criar_os = BooleanField('Criar Ordens de Serviço')
    pode_aprovar_os = BooleanField('Aprovar Ordens de Serviço')
    pode_atualizar_os = BooleanField('Atualizar Status de OS')
    pode_cancelar_os = BooleanField('Cancelar Ordens de Serviço')

    # Permissões de Estoque
    pode_acessar_estoque = BooleanField('Acessar Módulo de Estoque')
    pode_gerenciar_produtos = BooleanField('Cadastrar/Editar Produtos')
    pode_movimentar_estoque = BooleanField('Movimentar Estoque')
    pode_ver_custos = BooleanField('Ver Custos e Preços')
    pode_ajustar_estoque = BooleanField('Fazer Ajustes de Estoque')

    # Permissões de Técnicos
    pode_gerenciar_tecnicos = BooleanField('Gerenciar Técnicos')
    pode_atribuir_tecnicos = BooleanField('Atribuir Técnicos às OS')

    submit = SubmitField('Salvar Permissões')



