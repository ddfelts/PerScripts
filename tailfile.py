import os
import select
import sys
import pynotify
import pyinotify

class Watcher(pyinotify.ProcessEvent):

    def __init__(self, paths):
        self._manager = pyinotify.WatchManager()
        self._notify = pyinotify.Notifier(self._manager, self)
        self._paths = {}
        for path in paths:
            self._manager.add_watch(path, pyinotify.IN_MODIFY)
            fh = open(path, 'rb')
            fh.seek(0, os.SEEK_END)
            self._paths[os.path.realpath(path)] = [fh, '']

    def run(self):
        while True:
            self._notify.process_events()
            if self._notify.check_events():
                self._notify.read_events()

    def process_default(self, evt):
        path = evt.pathname
        fh, buf = self._paths[path]
        data = fh.read()
        lines = data.split('\n')
        # output previous incomplete line.
        if buf:
            lines[0] = buf + lines[0]
        # only output the last line if it was complete.
        if lines[-1]:
            buf = lines[-1]
        lines.pop()

        # display a notification
        notice = pynotify.Notification('%s changed' % path, '\n'.join(lines))
        notice.show()

        # and output to stdout
        for line in lines:
            sys.stdout.write(path + ': ' + line + '\n')
        sys.stdout.flush()
        self._paths[path][1] = buf
if __name__ == '__main__':
   pynotify.init('watcher')
   paths = sys.argv[1:]
   Watcher(paths).run()
