import os
import shutil
import pprint

from beets import config
from beets.plugins import BeetsPlugin
from beets.ui.commands import PromptChoice
from beets import mediafile


class SomePlugin(BeetsPlugin):
    seen = []
    include_extensions = ['.nfo', '.jpg']
    pp = pprint.PrettyPrinter()

    def __init__(self):
        super(SomePlugin, self).__init__()
     
        # self.register_listener('item_copied', self.item_copied)
        # self.register_listener('item_moved', self.item_moved)
        self.album_template_fields['quality'] = _tmpl_album_quality

    def get_target_filename(self, source_filename, dest):
        filename, ext = os.path.splitext(source_filename)
        dest_dir = os.path.dirname(dest)

        if ext == '.nfo':            
            return os.path.join(dest_dir + '\\', 'info.nfo')
        elif ext in ['.jpg', '.jpeg']:
            source_filename = source_filename.lstrip('_')
            return os.path.join(dest_dir, '_' + source_filename)
        else:
            return os.path.join(dest_dir, source_filename)

    def item_copied(self, item, source, destination):
        source_dir_name = os.path.dirname(source)
        dest_dir_name = os.path.dirname(destination)

        if source_dir_name in self.seen:
            return

        self.seen.append(source_dir_name)

        results = [f for f in os.listdir(os.path.dirname(
            source)) if os.path.splitext(f)[1] in self.include_extensions]

        try:
            target_fname = ''
            for r in results:
                target_fname = self.get_target_filename(r, destination)
                print '%s -> %s' % (r, target_fname)

                shutil.copy2(os.path.join(source_dir_name, r), target_fname)
                # print 'copied ' + os.path.join(source_dir_name, r) + ' -> ' + target_fname
        except Exception as e:
            print 'fuck...'
            print e.message
            print e

    def item_moved(self, item, source, destination):
        source_dir_name = os.path.dirname(source)
        dest_dir_name = os.path.dirname(destination)

        if source_dir_name in self.seen:
            print 'dir ' + source_dir_name + ' already seen.'
            return

        self.seen.append(source_dir_name)

        results = [f for f in os.listdir(os.path.dirname(
            source)) if os.path.splitext(f)[1] in ['.nfo', '.jpg']]

        print results

        try:
            target_fname = ''
            for r in results:
                if r.endswith('.nfo'):
                    target_fname = os.path.join(dest_dir_name, 'info.nfo')
                elif r.endswith('.jpg'):
                    target_fname = os.path.join(dest_dir_name, '_' + r)
                else:
                    target_fname = os.path.join(dest_dir_name, r)

                shutil.copy2(os.path.join(source_dir_name, r), target_fname)
                print 'copied ' + os.path.join(source_dir_name, r) + ' -> ' + target_fname
        except Exception as e:
            print 'fuck...'
            print e.message
            print e


