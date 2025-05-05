import xml.etree.ElementTree as ET
import json
from abc import ABC, abstractmethod
from xml.dom import minidom

class ArtifactGenerator(ABC):
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def generate(self, output_path):
        pass

class ConfigGenerator(ArtifactGenerator):
    def generate(self, output_path):
        root_class = next(cls for cls in self.model.values() if cls.is_root)
        root_elem = self._build_element(root_class)
        rough_string = ET.tostring(root_elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="    ")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def _build_element(self, class_model):
        elem = ET.Element(class_model.name)
        for attr in class_model.attributes:
            attr_elem = ET.SubElement(elem, attr.name)
            attr_elem.text = attr.type
        for child_name in class_model.children:
            child_elem = self._build_element(self.model[child_name])
            elem.append(child_elem)
        return elem

class MetaGenerator(ArtifactGenerator):
    def generate(self, output_path):
        sorted_classes = self._topological_sort()

        result = []
        for cls in sorted_classes:
            params = [
                {"name": attr.name, "type": attr.type}
                for attr in cls.attributes
            ]
            for child in cls.children:
                params.append({"name": child, "type": "class"})

            obj = {
                "class": cls.name,
                "documentation": cls.documentation,
                "isRoot": cls.is_root,
            }
            if cls.multiplicity != ("0", "1"):  # по желанию
                obj["min"] = cls.multiplicity[0]
                obj["max"] = cls.multiplicity[1]
            else:
                obj["min"] = cls.multiplicity[0]
                obj["max"] = cls.multiplicity[1]

            obj["parameters"] = params
            result.append(obj)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    def _topological_sort(self):
        visited = set()
        result = []

        def visit(cls):
            if cls.name in visited:
                return
            visited.add(cls.name)
            for child in cls.children:
                visit(self.model[child])
            result.append(cls)

        for cls in self.model.values():
            visit(cls)

        return result
