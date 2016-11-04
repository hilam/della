from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import reverse
from django.db.models import Q, Max
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .forms import MessageCreateForm
from .models import Message, Thread
from . import inbox_service


@method_decorator(login_required, name='dispatch')
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm

    def post(self, request, pk, *args, **kwargs):
        self.thread = self._validate_and_get_thread(thread_id=pk)
        if not self.thread:
            raise Http404('Haxxeru?')
        return super(MessageCreateView, self).post(
            request, pk, *args, **kwargs)

    def form_valid(self, form):
        message = form.save(commit=False)
        message.sent_by = self.request.user
        message.thread = self.thread
        return super(MessageCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('inbox:thread-detail', args=(self.thread.id,))

    def _validate_and_get_thread(self, thread_id):
        user = self.request.user
        return Thread.objects.filter(
            Q(pk=thread_id) & Q(
                Q(participant_1=user) | Q(participant_2=user))).first()


@method_decorator(login_required, name='dispatch')
class ThreadListView(ListView):
    model = Thread

    def get_queryset(self):
        user = self.request.user
        return Thread.objects.filter(Q(participant_1=user) | Q(
            participant_2=user)).annotate(
            last_message_time=Max('messages__created_on')).order_by(
                '-last_message_time')


@method_decorator(login_required, name='dispatch')
class ThreadDetailView(DetailView):
    model = Thread
    form_class = MessageCreateForm

    def get_object(self):
        user = self.request.user
        recipient_name = self.kwargs.get('recipient')
        recipient = get_object_or_404(User, username=recipient_name)
        participant_1, participant_2 = inbox_service.get_participants(
            user_1=user, user_2=recipient)
        thread, _ = Thread.objects.get_or_create(
            participant_1=participant_1, participant_2=participant_2)
        return thread

    def get_context_data(self, **kwargs):
        context = {}
        context['form'] = self.form_class()
        return super(ThreadDetailView, self).get_context_data(**context)