from pathlib import Path
from parser import ParsMod
from make import ConfigGen, MetaGen

def main():
    # путь к входному xml-файлу
    input_file = Path("C:/Users/User/Downloads/Стажировка AQA Python 2025. телеком/Стажировка AQA Python 2025/input/test_input.xml")
    
    # создаю папку для вывода, если нет
    output_dir = Path("out")
    output_dir.mkdir(exist_ok=True)

    # парсинг xml
    parser = ParsMod(input_file)
    model = parser.parse()

    # создание xml-конфигурацию
    config_make = ConfigGen(model)
    config_make.generate(output_dir / "config.xml")

    # создание json-описание модели
    meta_make = MetaGen(model)
    meta_make.generate(output_dir / "meta.json")

    print("complete")

if __name__ == "__main__":
    main()
