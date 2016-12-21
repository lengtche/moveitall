import glob
import logging
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from subprocess import CalledProcessError

from beets import config
from beets.plugins import BeetsPlugin


class AlbumQualityPlugin(BeetsPlugin):
    def __init__(self):
        super(AlbumQualityPlugin, self).__init__()

        self.album_template_fields['quality'] = _tmpl_album_quality


def _tmpl_album_quality(album):
    plugin_logger = logging.getLogger()
    plugin_logger.setLevel(logging.DEBUG)
    # plugin_logger.debug(sys.stdout.encoding)
    MEDIA_INFO_BIN=os.path.abspath('bin/mediainfo.exe')

    first_track_path = album.items()[0].path
    try:
        from beets.util import command_output

        output = command_output([MEDIA_INFO_BIN, first_track_path.decode('utf-8'), '--output=XML'], shell=True)
        # print output
    except CalledProcessError as cpe:
        print cpe.args
        print cpe.cmd
        print cpe.message
        print cpe.output
        print cpe.returncode

        import pdb;pdb.set_trace()

    try:
        xml_root = ET.fromstring(output)
    except UnicodeDecodeError as ede:
        import pdb;pdb.set_trace()

    bitrate_mode = xml_root.find('.//Bit_rate_mode').text
    basename = lambda file_path: os.path.basename(first_track_path)

    try:
        if bitrate_mode.lower() == 'constant':
            bitrate = xml_root.find('.//Bit_rate').text.replace(' Kbps', 'K')
            plugin_logger.debug('%s -> %s' % (basename(first_track_path), bitrate))

            return bitrate
        else:
            encoding_settings = xml_root.find('.//Encoding_settings')
            if encoding_settings is not None:
                encoding_settings = encoding_settings.text
                regex = re.compile(r'\-V\s(?P<preset>[0-9])')
                match = regex.search(encoding_settings)
                preset = 'V%s' % match.groupdict()['preset']
                plugin_logger.debug('%s -> %s (%s)' % (basename(first_track_path), preset, encoding_settings))

                return preset
            else:
                encoding_settings = 'VBR'  
                plugin_logger.debug('%s -> %s' % (basename(first_track_path), encoding_settings))

                return encoding_settings   
    except Exception as e:
        plugin_logger.error('there was an error', e)
        return 'WTF'
