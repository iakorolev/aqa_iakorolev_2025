import xml.etree.ElementTree as ET

class Attribute:
    def __init__(self, name, type_):
        self.name = name
        self.type = type_

class ClassModel:
    def __init__(self, name, is_root, documentation):
        self.name = name
        self.is_root = is_root
        self.documentation = documentation
        self.attributes = []
        self.children = []  # список имен дочерних классов
        self.parent = None
        self.multiplicity = ("0", "1")  # по умолчанию

class ModelParser:
    def __init__(self, xml_path):
        self.xml_path = xml_path

    def parse(self):
        tree = ET.parse(self.xml_path)
        root = tree.getroot()

        classes = {}
        aggregations = []

        for class_elem in root.findall("Class"):
            name = class_elem.get("name")
            is_root = class_elem.get("isRoot") == "true"
            doc = class_elem.get("documentation", "")
            class_model = ClassModel(name, is_root, doc)

            for attr in class_elem.findall("Attribute"):
                class_model.attributes.append(Attribute(attr.get("name"), attr.get("type")))

            classes[name] = class_model

        for agg in root.findall("Aggregation"):
            source = agg.get("source")
            target = agg.get("target")
            source_mult = agg.get("sourceMultiplicity")
            # Установка связи
            classes[target].children.append(source)
            classes[source].parent = target
            classes[source].multiplicity = self._parse_multiplicity(source_mult)

        return classes

    def _parse_multiplicity(self, mult):
        if ".." in mult:
            return tuple(mult.split(".."))
        return (mult, mult)
