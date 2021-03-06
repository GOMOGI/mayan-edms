from __future__ import absolute_import

import base64
import os
import urllib

from django.core.files import File

from converter.api import convert
from mimetype.api import get_mimetype


class StagingFile(object):
    """
    Simple class to extend the File class to add preview capabilities
    files in a directory on a storage
    """
    def __init__(self, staging_folder, filename=None, encoded_filename=None):
        self.staging_folder = staging_folder
        if encoded_filename:
            self.encoded_filename = str(encoded_filename)
            self.filename = base64.urlsafe_b64decode(urllib.unquote_plus(self.encoded_filename))
        else:
            self.filename = filename
            self.encoded_filename = base64.urlsafe_b64encode(filename)

    def __unicode__(self):
        return unicode(self.filename)

    def as_file(self):
        return File(file=open(self.get_full_path(), mode='rb'), name=self.filename)

    def get_full_path(self):
        return os.path.join(self.staging_folder.folder_path, self.filename)

    def get_image(self, size, page, zoom, rotation, as_base64=True):
        # TODO: add support for transformations
        converted_file_path = convert(self.get_full_path(), size=size)

        if as_base64:
            mimetype = get_mimetype(open(converted_file_path, 'r'), converted_file_path, mimetype_only=True)[0]
            image = open(converted_file_path, 'r')
            base64_data = base64.b64encode(image.read())
            image.close()
            return u'data:%s;base64,%s' % (mimetype, base64_data)
        else:
            return converted_file_path

    def delete(self):
        os.unlink(self.get_full_path())
