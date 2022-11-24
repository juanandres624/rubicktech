"""FIRMADO DE ARCHIVOS XML"""
"""ESTADO: FALTA COMPROBAR CON WS DE SRI"""

from signxml import XMLSigner, XMLVerifier
import xml.etree.ElementTree
from OpenSSL import crypto


def firmar_xml(xml_filename):
    """ RETORNA XML STRING FIRMADO """
    # clave = "sf3LnaMZMz"
    clave = ""
    with open("invoices/firma/5760703_identity.p12", "rb") as file:
        p12 = crypto.load_pkcs12(file.read(), clave.encode())
        print(p12)

    # test
    # print (crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))

    # test
    # print (crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))

    # no usar
    # cert = open("example.pem").read()
    # key = open("example.key").read()

    key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    cert = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())

    # archivod de prueba
    filename = xml_filename

    """
    MAL:  
    <ns0:CanonicalizationMethod Algorithm="http://www.w3.org/2006/12/xml-c14n11" />
    <ns0:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1" />

    BIEN : 
    <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></ds:CanonicalizationMethod>
    <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></ds:SignatureMethod>
    """

    root = xml.etree.ElementTree.parse(filename).getroot()

    # sha1 por defecto
    final_firmado = XMLSigner().sign(root, key=key, cert=cert)

    # verified_data = XMLVerifier().verify(signed_root).signed_xml
    # print (final_firmado.values)

    # xml_str = xml.etree.ElementTree.tostring(signed_root, encoding='utf-8')
    xml_str = xml.etree.ElementTree.tostring(final_firmado)
    # print (xml_str.decode())
    final = str(xml_str.decode())
    final2 = final.replace('ns0', 'ds')
    return final2


"""abre un xml,lo firma y guarda en otro xml"""


def save_xml_firmado(xml_firmado_name, xml_origen):
    """name : xxxxx.xml"""
    file1 = open(xml_origen, "w")
    # file1.write(str(xml_str))
    file1.write(firmar_xml(xml_origen))
    file1.close()  # to change file access modes
    pass

# print (firmar_xml("new.xml"))
