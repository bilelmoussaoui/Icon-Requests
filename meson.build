project(
  'icon-requests',
  version: '0.1.2',
  license: 'GPL-3.0',
  default_options: ['prefix=/usr']
)

python = import('python3')

message('Looking for dependencies')
glib = dependency('glib-2.0')
gobject = dependency('gobject-2.0')
gir = dependency('gobject-introspection-1.0')
gtk = dependency('gtk+-3.0', version : '>=3.16')

if not python.find_python().found()
	error('Couldnt find an executable python')
endif


data_dir = join_paths(get_option('prefix'), get_option('datadir'))
python_dir = join_paths(get_option('prefix'), python.sysconfig_path('purelib'))


# Configuration params
conf = configuration_data()
conf.set('DATA_DIR', join_paths(data_dir, 'IconRequests'))
conf.set('LOCALE_DIR', join_paths(data_dir, 'locale'))
conf.set('PYTHON_DIR', python_dir)

subdir('data')
subdir('po')

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
