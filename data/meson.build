gnome = import('gnome')

build_dir = get_option('prefix') + '/' + get_option('datadir')
po_dir = get_option('prefix') + '/' + get_option('datadir') + '/locale'
message('TODO: Compiling resources')
gnome.compile_resources(
     'icon-requests', 'icon-requests.gresource.xml',
     gresource_bundle: true,
     source_dir : '.',
     install_dir : build_dir + '/IconRequests',
     install: true)


message('Compiling schemas')
gnome.compile_schemas()
install_data(
    'org.gnome.IconRequests.gschema.xml',
    install_dir : 'share/glib-2.0/schemas')

message('TODO: Making a .desktop file')
custom_target('icon-requests.desktop',
	output : 'icon-requests.desktop',
	input : 'icon-requests.desktop.in',
	command : [intltool_merge, '--desktop-style', po_dir, '@INPUT@', '@OUTPUT@'],
	install : true,
	install_dir : get_option('datadir') + '/applications'
	)

message('TODO: Preparing appdata')
custom_target('icon-requests.appdata.xml',
    output : 'icon-requests.appdata.xml',
    input : 'icon-requests.appdata.xml.in',
    command : [intltool_merge, '--xml-style', po_dir, '@INPUT@', '@OUTPUT@'],
    install : true,
    install_dir : get_option('datadir') + '/appdata'
    )

message('TODO: Making a list of icons')
subdir('icons')
