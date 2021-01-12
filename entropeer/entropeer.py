import logging

from os import path, listdir, walk
from multiprocessing import Process, JoinableQueue, cpu_count
from sys import exit, stdout

from colorama import Fore, Style

from entropeer.entropy import FileEntropy

def handle_failure(f):
    """
    This decorator provide an exception catcher for keyboard
    stopping in any function (especially in case of multiprocessing/
    multithreading locking)
    """
    def func_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt:
            exit(0)
        except SystemExit:
            exit(0)

    return func_wrapper

def format_line(file, line_num, content, found_string, match=True):
    logger = logging.getLogger('results')
    if not isinstance(found_string, str):
        found_string = found_string.decode()
    if not isinstance(content, str):
        content = content.decode()

    if match:
        content = found_string

    # put red highlighting around the matched string
    content = content.replace(found_string, Style.BRIGHT + Fore.RED + found_string + Style.RESET_ALL)

    # print the informations
    templ = "{}{}:{}:{}{}".format(Style.BRIGHT, file, line_num, Style.RESET_ALL, content)
    logger.info(templ)


class FileConsumer(Process):
    """
    The consumer class that will entropy calculation for each file
    """

    def __init__(self, queue, entropy=True, match=True, binary=False):
        Process.__init__(self)
        self.queue = queue
        self.entropy = entropy
        self.match = match
        self.binary = binary

    @handle_failure
    def run(self):
        while True:
            file = self.queue.get()[0]

            fe = FileEntropy(file)
            try:
                if self.entropy:
                    for result in fe.find_entropy(binary=self.binary):
                        format_line(*result, match=self.match)
                else:
                    for result in fe.find_regex(binary=self.binary):
                        format_line(*result, match=self.match)
            except UnicodeDecodeError:
                pass

            self.queue.task_done()
            if self.queue.empty():
                return

class EntropyDigger(object):  # 🦾
    """
    The producer class that will dispatch work for the consumers
    """
    THREADS = cpu_count() * 2
    VERBOSE = 25

    def __init__(self, file=None, directory=None, recurse=False, entropy=True, conf={}):
        if file is None and directory is None:
            raise Exception('Select at least a file or a directory to scan')

        self.file = file
        self.directory = directory
        self.recurse = recurse
        self.entropy = entropy
        self.match = conf.get('match')
        self.binary = conf.get('binary')
        self.thread = EntropyDigger.THREADS if conf.get('threads') == 0 else conf.get('threads')

        logging.info("Starting {} scan".format('entropy' if self.entropy else 'regex'))
        logging.info("Current mode: {} {}".format('file' if self.file else 'directory', 'recursive' if self.recurse else ''))
        logging.info("Using {} threads".format(self.thread))

        if self.entropy is False:
            default_rulefile = path.join(path.realpath(path.dirname(__file__)), 'rules.json')
            FileEntropy.load_rules_from_file(default_rulefile)
            if conf.get('rulefile') is not None:
                FileEntropy.load_rules_from_file(conf.get('rulefile'))
            logging.info("Loaded {} regex rules".format(len(FileEntropy.rules)))

        logger = logging.getLogger('results')
        loghandler = logging.StreamHandler(stdout)
        formatter = logging.Formatter('%(message)s')
        loghandler.setFormatter(formatter)
        logger.addHandler(loghandler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        self.queue = JoinableQueue()
        self.work()

        logging.info("Scan finished successfully")

    def work(self):
        # create workers
        for x in range(self.thread):
            worker = FileConsumer(self.queue, self.entropy, self.match, self.binary)
            worker.daemon = True
            worker.start()

        # only supplied file
        if self.file:
            self.queue.put((self.file,))

        # recursive directory scan
        elif self.recurse:
            for root, dir, files in walk(self.directory):
                for file in files:
                    self.queue.put((path.join(root, file),))

        # all files in current dir
        elif not self.recurse:
            for file in listdir(self.directory):
                file = path.join(self.directory, file)
                if path.isfile(file):
                    self.queue.put((file,))

        # wait for all the results
        self.queue.join()
