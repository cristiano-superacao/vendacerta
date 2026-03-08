# otimizacoes_cache.py
"""
Sistema de cache para melhorar performance do sistema
Reduz carga no banco de dados e acelera respostas
"""

from functools import wraps
from datetime import datetime, timedelta
import json
import hashlib

# Cache simples em memória (para desenvolvimento)
# Em produção, usar Redis ou Memcached
_cache = {}
_cache_expiry = {}

def cache_key(*args, **kwargs):
    """Gera chave única para cache baseada nos argumentos"""
    key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True, default=str)
    return hashlib.md5(key_data.encode()).hexdigest()

def cached(timeout=300):
    """
    Decorator para cachear resultado de funções
    
    Args:
        timeout: Tempo de expiração em segundos (padrão: 5 minutos)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Gerar chave de cache
            key = f"{f.__name__}:{cache_key(*args, **kwargs)}"
            
            # Verificar se está no cache e não expirou
            now = datetime.now()
            if key in _cache and key in _cache_expiry:
                if _cache_expiry[key] > now:
                    return _cache[key]
            
            # Executar função e cachear resultado
            result = f(*args, **kwargs)
            _cache[key] = result
            _cache_expiry[key] = now + timedelta(seconds=timeout)
            
            return result
        return decorated_function
    return decorator

def clear_cache(pattern=None):
    """
    Limpa o cache
    
    Args:
        pattern: Padrão para limpar apenas chaves específicas
    """
    if pattern is None:
        _cache.clear()
        _cache_expiry.clear()
    else:
        keys_to_delete = [k for k in _cache.keys() if pattern in k]
        for key in keys_to_delete:
            del _cache[key]
            if key in _cache_expiry:
                del _cache_expiry[key]

def get_cache_stats():
    """Retorna estatísticas do cache"""
    now = datetime.now()
    active_keys = sum(1 for k, v in _cache_expiry.items() if v > now)
    expired_keys = len(_cache) - active_keys
    
    return {
        'total_keys': len(_cache),
        'active_keys': active_keys,
        'expired_keys': expired_keys,
        'memory_size': len(json.dumps(list(_cache.values()), default=str))
    }

# Funções auxiliares para cache de queries específicas

@cached(timeout=600)  # 10 minutos
def get_vendedores_ativos(empresa_id=None):
    """Retorna vendedores ativos (cacheado)"""
    from models import Vendedor
    
    query = Vendedor.query.filter_by(ativo=True)
    if empresa_id:
        query = query.filter_by(empresa_id=empresa_id)
    
    return query.all()

@cached(timeout=300)  # 5 minutos
def get_metas_mes(mes, ano, empresa_id=None):
    """Retorna metas do mês (cacheado)"""
    from models import Meta
    from sqlalchemy.orm import joinedload
    
    query = Meta.query.options(
        joinedload(Meta.vendedor)
    ).filter_by(
        mes=mes,
        ano=ano
    )
    
    if empresa_id:
        query = query.join(Meta.vendedor).filter_by(empresa_id=empresa_id)
    
    return query.all()

@cached(timeout=1800)  # 30 minutos
def get_equipes_ativas(empresa_id=None):
    """Retorna equipes ativas (cacheado)"""
    from models import Equipe
    
    query = Equipe.query.filter_by(ativa=True)
    if empresa_id:
        query = query.filter_by(empresa_id=empresa_id)
    
    return query.all()

def invalidar_cache_vendedor(vendedor_id):
    """Invalida cache relacionado a um vendedor"""
    clear_cache(f"vendedor_{vendedor_id}")
    clear_cache("get_vendedores_ativos")

def invalidar_cache_meta(meta_id):
    """Invalida cache relacionado a uma meta"""
    clear_cache(f"meta_{meta_id}")
    clear_cache("get_metas_mes")

def invalidar_cache_equipe(equipe_id):
    """Invalida cache relacionado a uma equipe"""
    clear_cache(f"equipe_{equipe_id}")
    clear_cache("get_equipes_ativas")
