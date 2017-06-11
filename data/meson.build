gnome = import('gnome')
i18n = import('i18n')

build_dir = join_paths(get_option('prefix'), get_option('datadir'))
message('Compiling resources')
gnome.compile_resources(
  'icon-requests',
  'icon-requests.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: join_paths(build_dir, 'IconRequests'),
  install: true
)

message('Compiling schemas')
gnome.compile_schemas()
install_data(
  'org.gnome.IconRequests.gschema.xml',
  install_dir: 'share/glib-2.0/schemas'
)

message('Making a .desktop file')
i18n.merge_file(
  output: 'icon-requests.desktop',
  input: 'icon-requests.desktop.in',
  po_dir: '../po',
  type: 'desktop',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

message('Preparing appdata')
i18n.merge_file(
  output: 'icon-requests.appdata.xml',
  input: 'icon-requests.appdata.xml.in',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

message('Making a list of icons')
subdir('icons')
