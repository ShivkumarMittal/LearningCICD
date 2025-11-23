from rest_framework import viewsets, permissions
from .models import LeadStatus, Leads
from .serializers import LeadStatusSerializer, LeadsSerializer


class LeadStatusViewSet(viewsets.ModelViewSet):
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    permission_classes = [permissions.IsAuthenticated]


class LeadsViewSet(viewsets.ModelViewSet):
    queryset = Leads.objects.all().order_by('-created_at')
    serializer_class = LeadsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
