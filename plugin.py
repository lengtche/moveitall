import os
import shutil

from beets import config
from beets.plugins import BeetsPlugin


class SomePlugin(BeetsPlugin):
    seen = []
    # rename_rules = [
    #     '.nfo': lambda fname: n
    # ]

    def __init__(self):
        super(SomePlugin, self).__init__()

        self.register_listener('item_copied', self.item_copied)
        self.register_listener('item_moved', self.item_moved)

    def get_target_filename(self, source_filename, dest):
        r"""
        Return the target filename.

        >>> SomePlugin().get_target_filename('00-artist-album-1234.nfo', 'c:\\')
        c:\info.nfo
        """
        filename, ext = os.path.splitext(source_filename)
        dest_dir = os.path.dirname(dest)

        if ext == '.nfo':            
            if dest_dir.endswith('\\'):
                dest_dir = dest_dir[:-1]
            print dest_dir
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
            # print 'dir ' + source_dir_name + ' already seen.'
            return

        self.seen.append(source_dir_name)

        results = [f for f in os.listdir(os.path.dirname(
            source)) if os.path.splitext(f)[1] in ['.nfo', '.jpg']]

        # print results

        try:
            target_fname = ''
            for r in results:
                print '%s -> %s' % (r, self.get_target_filename(r, destination))
                if r.endswith('.nfo'):
                    target_fname = os.path.join(dest_dir_name, 'info.nfo')
                elif r.endswith('.jpg'):
                    target_fname = os.path.join(dest_dir_name, '_' + r)
                else:
                    target_fname = os.path.join(dest_dir_name, r)

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
