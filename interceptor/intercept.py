import os
import shutil
import sys

import pkg_resources
from satella.files import write_to_file, read_in_file

from interceptor.config import load_config_for
from interceptor.whereis import filter_whereis


DEFAULT_CONFIG = b'''{
  "args_to_take_away": [],
  "args_to_append": [],
  "args_to_append_before": [],
  "args_to_replace": []
}
'''

def run():
    source_file = pkg_resources.resource_filename(__name__, 'templates/cmdline.py')

    if not os.path.exists('/etc/interceptor.d'):
        print('/etc/interceptor.d does not exist, creating...')
        os.mkdir('/etc/interceptor.d')

    tool_name = sys.argv[1]
    try:
        load_config_for(tool_name)
    except KeyError:
        print('No configuration found for %s, creating a default one' % (tool_name, ))
        write_to_file(os.path.join('/etc/interceptor.d', tool_name), DEFAULT_CONFIG)
    source = filter_whereis(sys.argv[1])
    shutil.copy(source, source+'-intercepted')
    os.unlink(source)
    source_content = read_in_file(source_file, 'utf-8')
    source_content = source_content.format(EXECUTABLE=sys.executable)
    write_to_file(source, source_content, 'utf-8')
    os.chmod(source, 0o555)
    print('Successfully intercepted %s' % (tool_name, ))
