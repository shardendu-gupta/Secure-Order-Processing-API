from rest_framework import generics
from .models import AuditLog
from .serializers import AuditLogSerializer
from .permissions import AuditPermission




class AuditLogListView(generics.ListAPIView):

    queryset = AuditLog.objects.select_related('user').all()
    serializer_class = AuditLogSerializer
    permission_classes = [AuditPermission]
    ordering = ['-created_at']
