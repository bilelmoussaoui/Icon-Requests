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

# Configuration params
conf = configuration_data()
conf.set('PACKAGE_URL', 'https://github.com/bil-elmoussaoui/Icon-Requests')
conf.set('LIBDIR', join_paths(get_option('prefix'), get_option('libdir')))
conf.set('DATADIR', join_paths(get_option('prefix'), get_option('datadir'), 'IconRequests/'))
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('datadir'), 'locale/'))
conf.set('PACKAGE_NAME', 'Icon Requests')
conf.set('PACKAGE', 'icon-requests')
conf.set('VERSION', meson.project_version())
conf.set('BUILDDIR', meson.current_build_dir())
conf.set('PYTHONDIR', python_dir)

subdir('data')
subdir('po')


run_command(python, '-m', 'compileall', meson.current_source_dir() + '/IconRequests')
install_subdir('IconRequests', install_dir: python_dir)

message('Preparing init file')
configure_file(
  input: 'icon-requests.in',
  output: 'icon-requests',
  configuration: conf,
  install_dir: 'bin'
)

meson.add_install_script('meson_post_install.py')
