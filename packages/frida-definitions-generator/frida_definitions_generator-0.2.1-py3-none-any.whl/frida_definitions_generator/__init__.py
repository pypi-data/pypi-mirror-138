import contextlib
import os
import tempfile
import zipfile
from typing import Dict, Generator, Iterable, Optional, Sequence, Tuple

import lief

from frida_definitions_generator import _identifier

__version__ = "0.2.1"


class APKDexFiles:
    """
    Given an apk file, represent an iterable object over its dex files
    """

    def __init__(self, apk_path: str):
        self._tmpdir = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(apk_path, "r") as apk_file:
            files = apk_file.namelist()
            for file_name in files:
                if file_name.endswith(".dex"):
                    apk_file.extract(file_name, self._tmpdir.name)
        self.files = [os.path.join(self._tmpdir.name, file) for file in os.listdir(self._tmpdir.name)]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self.files):
            raise StopIteration
        return self.files[self._index - 1]


def get_dex_files(path: str) -> Iterable:
    if os.path.isdir(path):
        files = os.listdir(path)
        return [os.path.join(path, file) for file in files if file.endswith(".dex")]

    return APKDexFiles(path)


@contextlib.contextmanager
def declare_namespace(name: Optional[str]) -> Generator[str, None, None]:
    indent = ""
    if name is not None:
        escaped_prefix = _identifier.get_legal_pretty_name(name)
        print(f"declare namespace {escaped_prefix} {{")
        indent = "\t"

    yield indent

    if name is not None:
        print("}\n")


def java_type_to_typescript(type: lief.DEX.Type) -> Optional[str]:
    if type.type == lief.DEX.Type.TYPES.PRIMITIVE:
        if type.value in (
            lief.DEX.Type.PRIMITIVES.FLOAT,
            lief.DEX.Type.PRIMITIVES.DOUBLE,
            lief.DEX.Type.PRIMITIVES.SHORT,
            lief.DEX.Type.PRIMITIVES.INT,
            lief.DEX.Type.PRIMITIVES.LONG,
            lief.DEX.Type.PRIMITIVES.BYTE,
        ):
            return "number"
        elif type.value == lief.DEX.Type.PRIMITIVES.BOOLEAN:
            return "boolean"
        elif type.value == lief.DEX.Type.PRIMITIVES.CHAR:
            return "string"
    elif type.type == lief.DEX.Type.TYPES.CLASS:
        legal_name = _identifier.get_legal_pretty_name(type.value.pretty_name)
        return f"Java.Wrapper<{legal_name}>"
    elif type.type == lief.DEX.Type.TYPES.ARRAY:
        underlying_type = type.underlying_array_type
        return f"Array<{underlying_type}>"

    # should never happen unless LIEF have another type that we don't know about
    return None


def generate_choose_definitions(classes: lief.DEX.Class):
    print("declare namespace Java {")
    for cls in classes:
        escaped_pretty_name = _identifier.get_legal_pretty_name(cls.pretty_name)
        print(
            f'\tfunction choose(className: "{cls.pretty_name}", callbacks: ChooseCallbacks<{escaped_pretty_name}>): void;'
        )
        print(f'\tfunction use(className: "{cls.pretty_name}"): Java.Wrapper<{escaped_pretty_name}>;')
    print("}")


def generate_type_definitions(d, prefix: Optional[str] = None):
    indent = ""
    contains_classes = any(isinstance(i, lief.DEX.Class) for i in d.values())
    if contains_classes:
        with declare_namespace(prefix) as indent:
            for k, v in d.items():
                if isinstance(v, lief.DEX.Class):
                    name = v.pretty_name.split(".")[-1]
                    legal_name = _identifier.get_legal_name(name)
                    print(f"{indent}interface {legal_name} extends Java.Wrapper {{")
                    method_names = set(map(lambda m: m.name, v.methods))
                    for method_name in method_names:
                        # TODO: what does Frida do here?
                        if _identifier.get_legal_name(method_name) != method_name:
                            continue
                        holder_legal_name = _identifier.get_legal_pretty_name(v.pretty_name)
                        print(f"{indent}\t{method_name}: Java.MethodDispatcher<{holder_legal_name}>;")
                    for field in v.fields:
                        field_name = field.name
                        # TODO: what does Frida do here?
                        if _identifier.get_legal_name(field_name) != field_name:
                            continue
                        if field.name in method_names:
                            field_name = "_" + field_name
                        typescript_type = java_type_to_typescript(field.type)
                        if typescript_type is not None:
                            print(f"{indent}\t{field_name}: Java.Field<{typescript_type}>;")
                        else:
                            print(f"{indent}\t{field_name}: Java.Field;")
                    print(f"{indent}}}\n")

    for k, v in d.items():
        if isinstance(v, dict):
            if prefix is None:
                generate_type_definitions(v, prefix=k)
            else:
                generate_type_definitions(v, prefix=prefix + "." + k)


def insert_class_to_dict(classes: Dict, path: Sequence[str], cls: lief.DEX.Class):
    curr = classes
    for key in path[:-1]:
        if key not in curr:
            curr[key] = {}
        curr = curr[key]

    curr[path[-1]] = cls


def classes_list_from_paths(paths: Sequence[str]) -> Tuple[Sequence[lief.DEX.File], Sequence[lief.DEX.Class]]:
    # lief is a bit broken so we need to keep a reference to the Dex instance
    # otherwise our classes will be freed before we are done with them
    dexes = list()
    classes = list()
    for path in paths:
        for file in get_dex_files(path):
            dex = lief.DEX.parse(file)
            dexes.append(dex)
            classes.extend(dex.classes)
    return dexes, classes


def classes_list_to_dict(classes_list: Sequence[lief.DEX.Class]):
    classes_dict = dict()
    for cls in classes_list:
        path = cls.pretty_name.split(".")
        insert_class_to_dict(classes_dict, path, cls)
    return classes_dict


def starts_with_any(s: str, prefixes: Sequence[str]) -> bool:
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
    return False


def filter_classes_list(classes: Sequence[lief.DEX.Class], exclusions: Sequence[str]) -> Sequence[lief.DEX.Class]:
    return [cls for cls in classes if not starts_with_any(cls.pretty_name, exclusions)]


def generate(args):
    dexes_list, classes_list = classes_list_from_paths(args.paths)
    filtered_classes_list = filter_classes_list(classes_list, args.exclusions)
    classes_dict = classes_list_to_dict(filtered_classes_list)

    generate_type_definitions(classes_dict)
    generate_choose_definitions(filtered_classes_list)
