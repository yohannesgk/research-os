from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
import json
import uuid
from .models import ResearchSession, ResearchQuery, UserProfile

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'research/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sessions'] = ResearchSession.objects.filter(
            user=self.request.user
        )[:10]
        return context

class SessionView(LoginRequiredMixin, TemplateView):
    template_name = 'research/session.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = kwargs.get('session_id')
        session = get_object_or_404(
            ResearchSession, 
            id=session_id, 
            user=self.request.user
        )
        context['session'] = session
        context['queries'] = session.queries.all()
        context['sessions'] = ResearchSession.objects.filter(
            user=self.request.user
        )[:10]
        return context

class SessionListView(LoginRequiredMixin, View):
    def get(self, request):
        sessions = ResearchSession.objects.filter(user=request.user)
        data = [{
            'id': str(session.id),
            'title': session.title,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat(),
            'is_active': session.is_active
        } for session in sessions]
        return JsonResponse({'sessions': data})

@method_decorator(csrf_exempt, name='dispatch')
class CreateSessionView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        title = data.get('title', 'New Research Session')
        
        session = ResearchSession.objects.create(
            user=request.user,
            title=title
        )
        
        return JsonResponse({
            'id': str(session.id),
            'title': session.title,
            'created_at': session.created_at.isoformat(),
            'updated_at': session.updated_at.isoformat()
        })

@method_decorator(csrf_exempt, name='dispatch')
class QueryView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        session_id = data.get('session_id')
        query_text = data.get('query')
        query_type = data.get('type', 'research')
        
        session = get_object_or_404(
            ResearchSession, 
            id=session_id, 
            user=request.user
        )
        
        # Simulate AI response
        if query_type == 'research':
            response = f"Research results for: {query_text}\n\nThis is a simulated research response. In a real implementation, this would connect to your AI research service."
        else:
            response = f"Report generated for: {query_text}\n\nThis is a simulated report response. In a real implementation, this would generate a comprehensive report."
        
        query = ResearchQuery.objects.create(
            session=session,
            query_text=query_text,
            response_text=response,
            query_type=query_type
        )
        
        return JsonResponse({
            'id': str(query.id),
            'query': query.query_text,
            'response': query.response_text,
            'type': query.query_type,
            'created_at': query.created_at.isoformat()
        })

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'research/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context