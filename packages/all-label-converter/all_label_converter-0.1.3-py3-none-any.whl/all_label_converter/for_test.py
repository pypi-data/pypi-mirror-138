import all_label_converter as alc

obj = alc.import_dataset(r"C:\Users\Dati\Desktop\Jobs\Github\all_label_converter\all_label_converter\data" +
                         r"\HelmetDataCoco", "coco")

alc.export_dataset(obj, "yolodarknet", r"C:\Users\Dati\Desktop\Jobs\Github\all_label_converter\all_label_converter" +
                  r"\output")