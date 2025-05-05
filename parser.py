import xml.etree.ElementTree as ET

class Attr:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_ 

class Clss:
    def __init__(self, name, is_root, documentation):
        self.name = name  # имя класса
        self.is_root = is_root  # флаг корневого класса
        self.documentation = documentation  # описание
        self.attribute = []  # список атрибутов
        self.children = []  # имена дочерних классов
        self.parent = None  # имя родителя
        self.min_max = ("0", "1")  # кратность по умолчанию

class ParsMod:
    def __init__(self, xml_path):
        self.xml_path = xml_path  # путь к xml

    def parse(self):
        tree = ET.parse(self.xml_path)  # чтение xml
        root = tree.getroot()  # корневой элемент

        classes = {}  # словарь классов по имени

        # обработка элементво class 
        for class_elem in root.findall("Class"):
            name = class_elem.get("name")
            is_root = class_elem.get("isRoot") == "true"
            doc = class_elem.get("documentation", "")
            class_model = Clss(name, is_root, doc)

            # добавление атрб в класс
            for attr in class_elem.findall("Attribute"):
                class_model.attribute.append(Attr(attr.get("name"), attr.get("type")))

            classes[name] = class_model

        # обработка связей
        for agg in root.findall("Aggregation"):
            source = agg.get("source")
            target = agg.get("target")
            source_mult = agg.get("sourceMultiplicity", "0..1")

            # установка связи 
            if target in classes and source in classes:
                classes[target].children.append(source)
                classes[source].parent = target
                classes[source].min_max = self._parse_multiplicity(source_mult)

        return classes  

    def _parse_multiplicity(self, mult):
        # разбил кратность по ..
        return tuple(mult.split("..")) if ".." in mult else (mult, mult)
