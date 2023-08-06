__version__ = '0.1.6'


from .volume import CloudVolume
from . import precomputed
from . import graphene


precomputed.register()
graphene.register()
