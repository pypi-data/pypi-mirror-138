import logging
import os
import time


class DailyFileHandler(logging.FileHandler):
    def __init__(self, *args, dirname, filename, suffix='', date_fmt=None, **kwargs):
        self._dirname = dirname
        self._filename_no_path = filename
        self._suffix = suffix
        self._date_fmt = date_fmt or '%Y-%m-%d'
        self._day = self.format_today()
        filename = self.filename_on_day(self._day)
        self._filename = filename
        self.mkdir(self._filename)
        super(DailyFileHandler, self).__init__(filename, *args, **kwargs)

    def format_today(self):
        return time.strftime(self._date_fmt, time.localtime())

    def filename_on_day(self, day):
        # get full path filename with datefmt folder and datefmt filename suffix
        filename_without_suffix = self._dirname + f'/{day}/' + self._filename_no_path
        filename = '%s%s' % (filename_without_suffix, self._suffix)
        return filename

    @staticmethod
    def mkdir(filename):
        folder = os.path.dirname(filename)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def emit(self, record):
        day = self.format_today()
        # if self._day != day:
        self._day = day
        super(DailyFileHandler, self).close()
        self.baseFilename = self.filename_on_day(self._day)
        try:
            self.mkdir(self.baseFilename)
        except OSError:
            pass
        self.stream = open(self.baseFilename, "w")
        super(DailyFileHandler, self).emit(record)

