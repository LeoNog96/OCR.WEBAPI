import xml.dom.minidom as minidom

def iterate(list, collect):
    for item in list.childNodes:

        if item.nodeType == 1:
            collect = iterate(item, collect)

        if item.nodeType == 3:
            collect += str(item.nodeValue)
            collect += " "
            collect = iterate(item, collect)
    return collect


# all items data
def xmlParser(source):
    doc = minidom.parse(source)
    for elem in doc.childNodes:
        collector = ""
        collector = iterate(elem, collector)
        print("terminou o iterate")
    
    return collector
