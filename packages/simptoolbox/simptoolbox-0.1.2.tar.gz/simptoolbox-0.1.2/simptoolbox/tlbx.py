from simplogger import simplog
import unittest, random

class toolbox():

    toolboxes = {}

    __slost__ = ('log', 'allow_overwrite', 'tools', 'tb_name')

    def __new__(cls, *args, **kargs):
        tbkey = args[0]
        # If already exists, return it
        if tbkey in cls.toolboxes:
            return cls.toolboxes[tbkey]
        else:
            new_tb = super(toolbox, cls).__new__(cls)
            new_tb.log = simplog(kargs.get('log_name',__name__))
            new_tb.allow_overwrite = kargs.get('allow_overwrite', False)
            new_tb.tools = {}
            new_tb.tb_name = tbkey
            cls.toolboxes[tbkey] = new_tb
            return cls.toolboxes[tbkey]

    def __init__(self, *args, **kargs):
        return

    def get_toolbox_name(self):
        return self.tb_name

    # Registers a tool to the tool box
    def register(self, tool_name, tool_obj):
        # If already exists, handle overwrite policy
        if tool_name in self.tools:
            if tool_obj == self.get(tool_name):
                self.log.debug(f'Registered same obj twice for {tool_name}')
                self.tools.__setitem__(tool_name, tool_obj)
            elif self.allow_overwrite:
                self.log.debug(f'{tool_name} overwritten')
                self.tools.__setitem__(tool_name, tool_obj)
            else:
                self.log.exception(f'Attempted to overwrite {tool_name}',\
                                        err=KeyError)
        else: # Otherwise simply register
            self.log.debug(f'Registered {tool_name}')
            self.tools.__setitem__(tool_name, tool_obj)
        return

    # Sets an item to the toolbox
    def __setitem__(self, tool_name, tool_obj):
        self.register(tool_name, tool_obj)

    def __getitem__(self, tool_name):
        self.log.debug(f'Retrieved {tool_name}')
        return self.tools.__getitem__(tool_name)

    # Generates an object as stored in toolbox, any argument after the toolbox
    #   name are parameters for that object
    def generate(self, *args, **kargs):
        if len(args) == 0:
            self.log.exception('Expected at least 1 argument for tool_name',\
                                    err=ValueError)
        if len(args) > 1:
            self.log.debug(f'Generating {args[0]} with following args:\n'+\
                                f'{args},{kargs}')

            return self.get(args[0])(*args[1:], **kargs)
        else:
            self.log.debug(f'Generating {args[0]} with following args:\n'+\
                                f'{kargs}')
            return self.get(args[0])(**kargs)

    # Generates an object as stored in toolbox, any argument after the toolbox
    #   name are parameters for that object
    def generate_n(self, *args, **kargs):
        if len(args) < 2:
            self.log.exception('Expected at least 2 arguments for tool_name '+\
                                    'and quantity', err=ValueError)
        if len(args) > 2:
            self.log.debug(f'Generating {args[1]} of {args[0]} with '+\
                            f'following args:\n {args}, {kargs}')
            return [self.get(args[0])(*args[2:], **kargs) for x in range(args[1])]
        else:
            self.log.debug(f'Generating {args[1]} of {args[0]} with '+\
                            f'following args:\n {kargs}')
            return [self.get(args[0])(**kargs) for x in range(args[1])]

    # Clears the toolbox
    def clear(self):
        self.log.debug('Cleared tools')
        self.tools = {}

    # Searches for the key of the object stored
    def index(self, item):
        for key, tool in self.tools.items():
            if item == tool:
                return key
        self.log.exception('Used index with an item that does not exist in '+\
                            'the toolbox.')

    # Returns names of tools
    def keys(self):
        return self.tools.keys()

    def __len__(self):
        return self.tools.__len__()

    # Returns whether or not they're equal
    def __eq__(self, other):
        if isinstance(other, str):
            return (self.get_toolbox_name() == other)
        elif isinstance(other, toolbox):
            return (self.get_toolbox_name() == other.get_toolbox_name())
        else:
            return False

    def load_dict(self, dct):
        self.log.debug('Loaded new dictionary with following tools:\n'+\
                        f'{dct.keys()}')
        if len(self.tools) == 0:
            self.tools = dct.copy()
        else:
            for key, item in self.tools:
                self.register(key, item)

    def export_dict(self, return_copy=True):
        if return_copy:
            return self.tools.copy()
        return self.tools

class toolbox_unittest(unittest.TestCase):

    def test_AAA_init(self):
        _ = toolbox('test')

    def test_AAB_same_name_init(self):
        tb1 = toolbox('toolbox')
        self.assertEqual(tb1,'toolbox', msg='Str equality failed')

        tb2 = toolbox('toolbox')
        self.assertEqual(tb2,'toolbox', msg='Str equality failed')
        self.assertEqual(tb1,tb2, msg='Toolbox equality failed')

    def test_AAC_test_adding(self):
        tb1 = toolbox('toolbox')
        tb2 = toolbox('toolbox')
        tb1['toolA'] = 3
        self.assertEqual(tb1['toolA'], 3, msg='Failed to set or retrieve')
        self.assertEqual(tb1.export_dict(), tb2.export_dict(), \
                msg='Either exported incorrectly or did not access same tb')

    def test_AAD_test_generating(self):
        tb1 = toolbox('toolbox')
        tb1['list'] = list
        tb1['dict'] = dict
        self.assertEqual(tb1.generate('list'), [], msg='Failed to generate')

        self.assertEqual(tb1.generate('dict', test=3), {'test':3},\
                                        msg='Failed to generate')

    def test_AAE_test_generating_multiple(self):
        tb1 = toolbox('toolbox')
        tb1['list'] = list

        self.assertEqual(len(tb1.generate_n('list',10)), 10)

if __name__ == '__main__':
    unittest.main()
