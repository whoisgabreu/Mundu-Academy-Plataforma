import hashlib
import secrets
from io import BytesIO

from django.utils import timezone

from cursos.models import Certificate, CertificateTemplate


def build_certificate_code(prefix='CERT'):
    return f'{prefix}-{secrets.token_hex(6).upper()}'


def build_qr_matrix(payload, size=7):
    digest = hashlib.sha256((payload or '').encode('utf-8')).hexdigest()
    bits = ''.join(f'{int(char, 16):04b}' for char in digest)
    matrix = []
    cursor = 0
    for row in range(size):
        cells = []
        for col in range(size):
            finder = (row < 2 and col < 2) or (row < 2 and col >= size - 2) or (row >= size - 2 and col < 2)
            cells.append(finder or bits[cursor % len(bits)] == '1')
            cursor += 1
        matrix.append(cells)
    return matrix


def issue_certificate(user, template=None, modulo=None, trilha=None, verification_url=''):
    template = template or CertificateTemplate.objects.filter(ativo=True).first()
    course_name = ''
    if modulo:
        course_name = modulo.titulo
    elif trilha:
        course_name = trilha.titulo

    lookup = {'usuario': user, 'modulo': modulo, 'trilha': trilha, 'template': template}
    cert = Certificate.objects.filter(**lookup).first()
    if cert:
        return cert, False

    code = build_certificate_code()
    payload = verification_url or code
    cert = Certificate.objects.create(
        usuario=user,
        modulo=modulo,
        trilha=trilha,
        template=template,
        codigo=code,
        nome_aluno=user.get_full_name() or user.username,
        curso=course_name,
        carga_horaria=template.carga_horaria if template else 0,
        assinatura=template.assinatura if template else '',
        logo=template.logo if template else '',
        qr_payload=payload,
    )
    return cert, True


def certificate_context(certificate):
    course = certificate.curso
    if not course and certificate.modulo:
        course = certificate.modulo.titulo
    if not course and certificate.trilha:
        course = certificate.trilha.titulo
    issued_at = certificate.emitido_em or timezone.now()
    return {
        'certificate': certificate,
        'nome_aluno': certificate.nome_aluno or certificate.usuario.get_full_name() or certificate.usuario.username,
        'curso': course or 'Mundu Academy',
        'data': issued_at.strftime('%d/%m/%Y'),
        'codigo': certificate.codigo,
        'carga_horaria': certificate.carga_horaria,
        'assinatura': certificate.assinatura,
        'logo': certificate.logo,
        'qr_matrix': build_qr_matrix(certificate.qr_payload or certificate.codigo),
    }


def _pdf_text(text):
    return str(text or '').encode('cp1252', errors='replace').decode('cp1252')


def certificate_pdf_bytes(certificate):
    ctx = certificate_context(certificate)
    lines = [
        'MUNDU ACADEMY',
        'CERTIFICADO',
        f"Certificamos que {ctx['nome_aluno']}",
        f"concluiu {ctx['curso']}.",
        f"Carga horaria: {ctx['carga_horaria']} horas",
        f"Emitido em: {ctx['data']}",
        f"Codigo unico: {ctx['codigo']}",
        f"Assinatura: {ctx['assinatura'] or 'Mundu Academy'}",
    ]
    stream_lines = ['BT', '/F1 24 Tf', '72 760 Td', '32 TL']
    for index, line in enumerate(lines):
        font_size = 24 if index < 2 else 14
        stream_lines.append(f'/F1 {font_size} Tf')
        escaped = _pdf_text(line).replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        stream_lines.append(f'({escaped}) Tj')
        stream_lines.append('T*')
    stream_lines.append('ET')
    stream = '\n'.join(stream_lines).encode('cp1252', errors='replace')

    objects = [
        b'<< /Type /Catalog /Pages 2 0 R >>',
        b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
        b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 842 595] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
        b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
        b'<< /Length ' + str(len(stream)).encode('ascii') + b' >>\nstream\n' + stream + b'\nendstream',
    ]
    pdf = BytesIO()
    pdf.write(b'%PDF-1.4\n')
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f'{number} 0 obj\n'.encode('ascii'))
        pdf.write(obj)
        pdf.write(b'\nendobj\n')
    xref_offset = pdf.tell()
    pdf.write(f'xref\n0 {len(objects) + 1}\n'.encode('ascii'))
    pdf.write(b'0000000000 65535 f \n')
    for offset in offsets[1:]:
        pdf.write(f'{offset:010d} 00000 n \n'.encode('ascii'))
    pdf.write(f'trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n'.encode('ascii'))
    pdf.write(f'startxref\n{xref_offset}\n%%EOF'.encode('ascii'))
    return pdf.getvalue()
