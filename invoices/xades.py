import os
import base64
import subprocess
import logging
import xml.etree.ElementTree as ET
from OpenSSL import crypto
from signxml import XMLSigner, XMLVerifier

from invoices.firmado import firmar_xml

class Xades(object):

    def apply_digital_signature(self, access_key, password):
        OPT_PATH = os.path.join(os.path.abspath(os.curdir),'invElect/')
        name = '%s%s.xml' % (OPT_PATH, access_key)
        JAVA_CMD = 'java'
        JAR_PATH = 'firma/firmaXadesBes.jar'
        firma_path = os.path.join(os.path.dirname(__file__), JAR_PATH)
        file_pk12 = os.path.join(os.path.dirname(__file__), 'firma/5760703_identity.p12')
        pathServerKey = bytes(file_pk12, "utf-8")

        clave = bytes(password,"utf-8")
        tree = ET.parse(name)
        root = tree.getroot()
        xmlstr = ET.tostring(root, encoding='utf8', method='xml')
        p = subprocess.Popen([JAVA_CMD, '-jar', firma_path, xmlstr, base64.b64encode(pathServerKey), base64.b64encode(clave)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        resultado = p.communicate()[0]
        return resultado