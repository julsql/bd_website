from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from main.core.application.usecases.attachments.attachments_service import AttachmentsService
from main.core.domain.model.attachment_type import AttachmentType
from main.core.infrastructure.persistence.file.attachments_adapter import AttachmentsAdapter


@login_required
def signed_copies_view(request: HttpRequest) -> HttpResponse:
    return attachment_view(request, AttachmentType.SIGNED_COPY)


@login_required
def exlibris_view(request: HttpRequest) -> HttpResponse:
    return attachment_view(request, AttachmentType.EXLIBRIS)


def attachment_view(request: HttpRequest, attachment_type: AttachmentType) -> HttpResponse:
    repository = AttachmentsAdapter()
    service = AttachmentsService(repository)
    if request.user.current_collection:
        collection = request.user.current_collection
    else:
        collection = request.user.collections.all().first()

    if attachment_type == AttachmentType.SIGNED_COPY:
        attachments = service.main_signed_copies(collection.id)
    else:
        attachments = service.main_ex_libris(collection.id)

    return render(request, 'attachments/module.html', {
        'attachments': [{'isbn': attachment.isbn,
                         'album': attachment.title,
                         'number': attachment.number,
                         'series': attachment.series,
                         'range': attachment.range_attachment,
                         'total': attachment.total}
                        for attachment in attachments.attachments_list],
        'attachments_sum': attachments.sum,
        'title': attachments.title,
        'subtitle': attachments.subtitle,
        'type': attachments.type,
        'image_path': attachments.image_path,
    })
