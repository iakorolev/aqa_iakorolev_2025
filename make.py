import xml.etree.ElementTree as ET
import json
from xml.dom import minidom

class ConfigGen:
    def __init__(self, model):
        self.model = model

    def generate(self, output_path):
        # корневой класс
        root_class = next(cls for cls in self.model.values() if cls.is_root)
        # xml из корневого класса
        root_elem = self._build_element(root_class)
        # форматирирую исходя из шаблона
        pretty_xml = minidom.parseString(ET.tostring(root_elem, 'utf-8')).toprettyxml(indent="   ")
        pretty_xml = '\n'.join(pretty_xml.split('\n')[1:])  # убираю первую строку, т.к в примере нет с xml декларацией, поэтому решил убрать.

        # ещё заметил, что все пустые теги были <CPLANE></CPLANE> вместо </CPLANE>. 
        # т.к. эти записи полностью эквиваленты друг другу, я решил оставить свой результато, но при необходимости, можно расскоментировать код написанный ниже,
        # который с помощью регулярных выражений открывает и закрывает пустые теги.

        # import re
        # pretty_xml = re.sub(r'<(\w+?)/>', r'<\1></\1>', pretty_xml)

        # сохранение 
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

    def _build_element(self, class_model):
        # элемент с именем класса
        elem = ET.Element(class_model.name)

        # атрибуты
        for attr in class_model.attribute:
            attr_elem = ET.SubElement(elem, attr.name)
            attr_elem.text = attr.type

        # дочерние классы
        for child_name in class_model.children:
            elem.append(self._build_element(self.model[child_name]))

        return elem

class MetaGen:
    def __init__(self, model):
        self.model = model 

    def generate(self, output_path):
        sorted_classes = self._topological_sort()  # сортировка классов

        result = []
        for cls in sorted_classes:
            # параметры 
            # атрб + доч. классы
            params = [{"name": attr.name, "type": attr.type} for attr in cls.attribute]
            params += [{"name": child, "type": "class"} for child in cls.children]

            # описание класса
            obj = {
                "class": cls.name,
                "documentation": cls.documentation,
                "isRoot": cls.is_root,
                "parameters": params
            }
            
            # Добавляем min и max сразу после isRoot, если класс не корень
            if not cls.is_root:
                obj["max"] = cls.min_max[1]
                obj["min"] = cls.min_max[0]

            result.append(obj)

        # json в файл
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

    def _topological_sort(self):
        visited, result = set(), []

        def visit(cls):
            if cls.name in visited:
                return
            visited.add(cls.name)
            # дочерние классы
            for child in cls.children:
                visit(self.model[child])
            result.append(cls)

        # разбор для всех классов
        for cls in self.model.values():
            visit(cls)

        return result
