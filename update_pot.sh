#!/bin/sh
# A modified code from the Terminix project<https://github.com/gnunn1/terminix/>. 
DOMAIN=icon-requests
BASEDIR=$(dirname $0)
OUTPUT_FILE=${BASEDIR}/po/${DOMAIN}.pot

echo "Extracting translatable strings... "

find ${BASEDIR}/ -name '*.py' | xgettext \
  --output $OUTPUT_FILE \
  --files-from=- \
  --directory=$BASEDIR \
  --language=Python \
  --keyword=C_:1c,2 \
  --from-code=utf-8

find ${BASEDIR}/ -name '*.ui' | xgettext \
  --output $OUTPUT_FILE \
  --join-existing \
  --files-from=- \
  --directory=$BASEDIR \
  --language=ui \
  --foreign-user \
  --keyword=C_:1c,2 \
  --from-code=utf-8

xgettext \
  --join-existing \
  --output $OUTPUT_FILE \
  --default-domain=$DOMAIN \
  --package-name=$DOMAIN \
  --directory=$BASEDIR \
  --foreign-user \
  --language=Desktop \
  ${BASEDIR}/data/icon-requests.desktop.in


xgettext \
  --join-existing \
  --output $OUTPUT_FILE \
  --default-domain=$DOMAIN \
  --package-name=$DOMAIN \
  --directory=$BASEDIR \
  --foreign-user \
  --language=appdata \
  ${BASEDIR}/data/icon-requests.appdata.xml.in

# Merge the messages with existing po files
echo "Merging with existing translations... "
for file in ${BASEDIR}/po/*.po
do
  echo -n $file
  msgmerge --update $file $OUTPUT_FILE
done
