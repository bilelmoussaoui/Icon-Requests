project(
  'icon-requests',
  version: '0.1.2'
)

message('Looking for dependencies')
python = find_program('python3')
glib = dependency('glib-2.0')
gobject = dependency('gobject-2.0')
gir = dependency('gobject-introspection-1.0')
gtk = dependency('gtk+-3.0', version : '>=3.16')

message('Getting python install dir')
r = run_command(python, '-c', 'from distutils.sysconfig import get_python_lib; print(get_python_lib())')
if r.returncode() != 0
    error('Cannot find python install dir')
endif
python_dir = r.stdout().strip()
data_dir = join_paths(get_option('prefix'), get_option('datadir'))


# Configuration params
conf = configuration_data()
conf.set('DATA_DIR', join_paths(data_dir, 'IconRequests'))
conf.set('LOCALE_DIR', join_paths(data_dir, 'locale'))
conf.set('PYTHON_DIR', python_dir)

subdir('data')
subdir('po')

run_command(python, '-m', 'compileall', join_paths(meson.current_source_dir(), 'IconRequests'))

install_subdir(
  'IconRequests',
  install_dir: python_dir
)

message('Preparing init file')
configure_file(
  input: 'icon-requests.in',
  output: 'icon-requests',
  configuration: conf,
  install_dir: 'bin'
)

meson.add_install_script('meson_post_install.py')
