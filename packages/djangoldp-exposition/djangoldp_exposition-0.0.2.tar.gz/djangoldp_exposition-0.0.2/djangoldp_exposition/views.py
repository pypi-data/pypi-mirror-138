from djangoldp.views import LDPViewSet
from .models import Expo, Materiel

class ExpositionsByUser(LDPViewSet):
  model = Expo

  def get_queryset(self, *args, **kwargs):
    username = self.kwargs['username']
    
    # Additional filter criteria: , target__value=target
    return super().get_queryset(*args, **kwargs)\
          .filter(username=username)



class MaterialsByUser(LDPViewSet):
  model = Materiel

  def get_queryset(self, *args, **kwargs):
    username = self.kwargs['username']
    
    # Additional filter criteria: , target__value=target
    return super().get_queryset(*args, **kwargs)\
          .filter(username=username)
