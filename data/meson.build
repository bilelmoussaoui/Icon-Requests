gnome = import('gnome')

build_dir = get_option('prefix') + '/' + get_option('datadir')
po_dir = get_option('prefix') + '/' + get_option('datadir') + '/locale'
message('TODO: Compiling resources')
gnome.compile_resources(
     'numix-icon-report', 'numix-icon-report.gresource.xml',
     gresource_bundle: true,
     source_dir : '.',
     install_dir : build_dir + '/IconReport',
     install: true)


message('Compiling schemas')
gnome.compile_schemas()
install_data(
    'org.Numix.IconReport.gschema.xml',
    install_dir : 'share/glib-2.0/schemas')

message('TODO: Making a .desktop file')
custom_target('numix-icon-report.desktop',
	output : 'numix-icon-report.desktop',
	input : 'numix-icon-report.desktop.in',
	command : [intltool_merge, '--desktop-style', po_dir, '@INPUT@', '@OUTPUT@'],
	install : true,
	install_dir : get_option('datadir') + '/applications'
	)

message('TODO: Preparing appdata')
custom_target('numix-icon-report.appdata.xml',
    output : 'numix-icon-report.appdata.xml',
    input : 'numix-icon-report.appdata.xml.in',
    command : [intltool_merge, '--xml-style', po_dir, '@INPUT@', '@OUTPUT@'],
    install : true,
    install_dir : get_option('datadir') + '/appdata'
    )

message('TODO: Making a list of icons')
subdir('icons')
