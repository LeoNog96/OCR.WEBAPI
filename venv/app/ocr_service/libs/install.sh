#!/bin/bash

ACCEPT_EULA=Y apt-get install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

ACCEPT_EULA=Y apt-get install libpulse-dev

ACCEPT_EULA=Y apt install python3-pip

ACCEPT_EULA=Y apt install tesseract-ocr tesseract-ocr-por

ACCEPT_EULA=Y apt install libtesseract-dev

pip3 install textract

pip3 install elasticsearch

apt install curl

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update

ACCEPT_EULA=Y apt-get install msodbcsql17

# optional: for bcp and sqlcmd
 ACCEPT_EULA=Y apt-get install mssql-tools

echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc

source ~/.bashrc
# optional: for unixODBC development headers

ACCEPT_EULA=Y apt-get install unixodbc-dev

pip3 install azure-storage

pip3 install pyodbc

pip3 install https://github.com/mattgwwalker/msg-extractor/zipball/master

sudo apt -y install libreoffice-base

pip3 install beautifulsoup4


