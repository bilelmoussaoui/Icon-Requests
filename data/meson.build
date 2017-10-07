gnome = import('gnome')
i18n = import('i18n')

message('Compiling resources')
gnome.compile_resources(
  'com.github.bilelmoussaoui.IconRequests',
  'com.github.bilelmoussaoui.IconRequests.gresource.xml',
  gresource_bundle: true,
  source_dir: '.',
  install_dir: join_paths(data_dir, 'IconRequests'),
  install: true
)

message('Compiling schemas')
gnome.compile_schemas()
install_data(
  'com.github.bilelmoussaoui.IconRequests.gschema.xml',
  install_dir: join_paths(get_option('prefix'), 'share/glib-2.0/schemas')
)

message('Making a .desktop file')
i18n.merge_file(
  output: 'com.github.bilelmoussaoui.IconRequests.desktop',
  input: 'com.github.bilelmoussaoui.IconRequests.desktop.in',
  po_dir: '../po',
  type: 'desktop',
  install: true,
  install_dir: join_paths(data_dir, 'applications')
)

message('Preparing appdata')
i18n.merge_file(
  output: 'com.github.bilelmoussaoui.IconRequests.appdata.xml',
  input: 'com.github.bilelmoussaoui.IconRequests.appdata.xml.in',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(data_dir, 'appdata')
)

message('Making a list of icons')
subdir('icons')
