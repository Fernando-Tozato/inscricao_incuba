from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from database.models import Inscrito, Aluno, Unidade, Curso, Turma
from interno.tasks import log_action


@receiver(post_save, sender=Inscrito)
@receiver(post_save, sender=Aluno)
@receiver(post_save, sender=Unidade)
@receiver(post_save, sender=Curso)
@receiver(post_save, sender=Turma)
def log_create_update(sender, instance, created, **kwargs):
    action = 'Cadastrado' if created else 'Atualizado'
    log_action(action, instance)

@receiver(post_delete, sender=Inscrito)
@receiver(post_delete, sender=Aluno)
@receiver(post_delete, sender=Unidade)
@receiver(post_delete, sender=Curso)
@receiver(post_delete, sender=Turma)
def log_delete(sender, instance, **kwargs):
    log_action('Removido', instance)
