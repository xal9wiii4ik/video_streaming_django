import typing as tp
import fleep

from rest_framework.exceptions import ValidationError


def validate_file(data: tp.Dict[str, tp.Any]) -> tp.Tuple[bytes, tp.List[str]]:
    """
    Validate file
    """

    if data.get('file') is None:
        raise ValidationError({'file': 'field file in create method is required'})

    file = data.pop('file')

    # get file and file info
    file_bytes = file.read()
    file_info = fleep.get(file_bytes)

    # validate file
    if not any(file_info.mime) or file_info.mime[0].split('/')[0] != 'video':
        raise ValidationError('File must be of the video type')

    return file_bytes, file_info.mime
