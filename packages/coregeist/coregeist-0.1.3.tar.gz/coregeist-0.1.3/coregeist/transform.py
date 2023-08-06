"""C converter for deep neural network models (like pytorch)

This script provides a toolkit to convert deepl learning models to c.

This file can also be imported as a module and contains the following
functions:

To build the layer route:

    * entry - returns a list with the input builder as initial element.
    * relu - returns a builder to add the relu function to the c model.
    * dense - returns a builder to add a dense layer to the c model.
    * activation_binarization - returns a builder to add binarization of the activation vector.
    * argmax - returns a builder to add the argmax function.

To transform the list of layers to c code:
    * model_transform - transforms the list of layer objects to _C_ source code.


"""

from string import Template
from typing import Callable, NamedTuple, Protocol

import itertools


def map_to_carray(name: str, ctype: str, parameters: list):
    return f"{ctype} {name}[] = {{{', '.join([str(cint) for cint in parameters])}}}"


def map_to_carray2d(name: str, ctype: str, parameters: list[str], columns: int):
    return f"{ctype} {name}[][{columns}] = {{{', '.join([str(cint) for cint in parameters])}}}"


def map_to_binarray1d(parameters: list[int], int_bytes: int, reverse: bool = True):
    """Maps a list of binary values (1,0) to an integer of size 'int_bytes'
    Only the set bit (1) will be checked and the unset bit will automatically be set to 0.
    This allows to map lists of type (1,0) and (1,-1)
    """
    # checks only if '1' is set; the '0' value will be ignored and just set to 0
    binvalues = [1 if x == 1 else 0 for x in parameters]
    values = list(itertools.zip_longest(*[iter(binvalues)] * int_bytes, fillvalue=None))
    # add leading zeros to the last element if length is != int_bytes
    nones = sum(x is None for x in values[-1])
    cleaned = list(filter(lambda ele: ele is not None, values[-1]))
    values[-1] = [0] * nones + cleaned
    return [int("".join(str(x) for x in (reversed(lst) if reverse else lst)), 2) for lst in values]


def map_to_int2d(parameters: list[list[int]], int_bytes: int, reverse: bool = True):
    ints = [map_to_binarray1d(row, int_bytes, reverse=reverse) for row in parameters]
    return ints


def map_to_binarray(parameters: list[list[int]], int_bytes: int, reverse: bool = True):
    result = []
    ints = map_to_int2d(parameters, int_bytes, reverse=reverse)
    for values in ints:
        result.append(f"{{{', '.join([str(cint) for cint in values])}}}")
    return result, len(ints[0])


def build_bin_2darray(name: str, ctype: str, byte_size: int, values: list[list[int]]):
    return map_to_carray2d(name, ctype, *map_to_binarray(values, byte_size))


def build_bin_array(name: str, ctype: str, byte_size: int, values: list[int]):
    return map_to_carray(name, ctype, map_to_binarray1d(values, byte_size))


def build_carray(name: str, ctype: str, values: list[int]):
    return map_to_carray(name, ctype, values)


class MetaObjects(NamedTuple):
    name: str
    size: int
    ctype: str
    declaration: list[str]
    definition: str


class MetaInfo(NamedTuple):
    ctype: str = "int"
    binary_type: str = "unsigned int"
    byte_size: int = 32

    def enrich(
            self, meta_info: Callable[["MetaInfo"], Callable[[str, str, int], MetaObjects]]
    ):
        return meta_info(self)

    def enrich_all(
            self,
            meta_infos: list[
                Callable[["MetaInfo"], Callable[[str, str, int], MetaObjects]]
            ],
    ):
        return [self(x) for x in meta_infos]

    def __call__(
            self, meta_info: Callable[["MetaInfo"], Callable[[str, str, int], MetaObjects]]
    ):
        return meta_info(self)


class Builder(Protocol):
    def __call__(self, name: str, prev_name: str, prev_size: int) -> MetaObjects:
        pass


def entry(
        input_type: str = "uint8_t", input_name: str = "input"
) -> Callable[[MetaInfo], Callable[[str, str, int], MetaObjects]]:
    """Initializes the deep neural net layer builder

    Parameters
    ----------
    size : int
        The size of the input array

    Returns
    -------
    list
        a list with an input builder layer element.
    """

    def with_meta_info(info: MetaInfo) -> Callable[[str, str, int], MetaObjects]:
        def build_layer(
                name: str,
                prev_name: str,
                prev_size: int,
        ) -> MetaObjects:
            declaration = [
                build_carray(input_name, input_type, [0] * prev_size),
                build_bin_array(
                    name, info.binary_type, info.byte_size, [0] * prev_size
                ),
            ]

            build = ""

            return MetaObjects(input_name, prev_size, info.ctype, declaration, build)

        return build_layer

    return with_meta_info


def dense(
        size: int, weights: list[list[int]], byte_size: int = 32
) -> Callable[[MetaInfo], Callable[[str, str, int], MetaObjects]]:
    """Dense layer builder

    Parameters
    ----------
    size : int
        The size of the output array
    weights : list[int]
        The weights array

    Returns
    -------
    Callable[[str, str, int], CodePart]
        a dense builder function.
    """

    def with_meta_info(info: MetaInfo) -> Callable[[str, str, int], MetaObjects]:
        def build_layer(name: str, prev_name: str, prev_size: int) -> MetaObjects:
            weight_name = name + "_weights"

            build = f"linear2d({prev_size}, {size}, {weight_name}, {prev_name}, {name})"

            declaration: list[str] = [
                build_bin_2darray(
                    weight_name, "const " + info.binary_type, byte_size, weights
                ),
                build_carray(name, info.ctype, [0] * size),
            ]

            return MetaObjects(name, size, info.ctype, declaration, build)

        return build_layer

    return with_meta_info


def relu(scaled_prelu: list[int], resolution: int = 1) -> Callable[[MetaInfo], Callable[[str, str, int], MetaObjects]]:
    """Dense layer builder

    Returns
    -------
    Callable[[str, str, int], CodePart]
        a relu function layer builder function.
    """

    def with_meta_info(info: MetaInfo) -> Callable[[str, str, int], MetaObjects]:
        def build_layer(name: str, prev_name: str, prev_size: int) -> MetaObjects:
            prelu_level_name = name + "_bias"
            build = f"prelu2d({prev_size}, {prev_name}, {resolution}, {prelu_level_name}, {prev_name})"

            declaration: list[str] = [
                map_to_carray(prelu_level_name, info.ctype, scaled_prelu),
            ]

            return MetaObjects(prev_name, prev_size, info.ctype, declaration, build)

        return build_layer

    return with_meta_info


def activation_binarization(
        threshold: list[int], input_scaling_factor: int = 0
) -> Callable[[MetaInfo], Callable[[str, str, int], MetaObjects]]:
    """Activation binarization builder

    Returns
    -------
    Callable[[str, str, int], CodePart]
        an activation binarization builder function.
    """

    def with_meta_info(info: MetaInfo) -> Callable[[str, str, int], MetaObjects]:
        def build_layer(name: str, prev_name: str, prev_size: int) -> MetaObjects:
            threshold_name = name + "_bias"
            if input_scaling_factor > 1:
                build = f"binarize_scaled_activation({prev_size}, {prev_name}, {input_scaling_factor}, {threshold_name}, {name})"
            else:
                build = f"binarize_activation({prev_size}, {prev_name}, {threshold_name}, {name})"

            declaration: list[str] = [
                map_to_carray(threshold_name, info.ctype, threshold),
                map_to_carray(
                    name,
                    info.binary_type,
                    map_to_binarray1d([0] * prev_size, info.byte_size),
                ),
            ]
            return MetaObjects(name, prev_size, info.ctype, declaration, build)

        return build_layer

    return with_meta_info


def argmax() -> Callable[[MetaInfo], Callable[[str, str, int], MetaObjects]]:
    """argmax function layer builder

    The argmax function returns the position of the max element within an array

    Returns
    -------
    Callable[[str, str, int], CodePart]
        a argmax function builder function.
    """

    def with_meta_info(info: MetaInfo):
        def build_layer(
                name: str,
                prev_name: str,
                prev_size: int,
        ) -> MetaObjects:
            build = f"{name}[0] = argmax({prev_size}, {prev_name})"

            declaration: list[str] = [map_to_carray(name, info.binary_type, [0])]

            return MetaObjects(name, 1, info.ctype, declaration, build)

        return build_layer

    return with_meta_info


def create_layers(definitions):
    def write_tab(elements: list):
        return ";\n\t".join(elements) + ";"

    return write_tab(definitions)


def model_extract(
        layers: list[Callable[[str, str, int], MetaObjects]],
        input_size: int,
        binary_type: str = "unsigned int",
) -> list[MetaObjects]:
    name = "input"
    size = input_size
    ctype = "int"
    res: list[MetaObjects] = []
    for i, layer in enumerate(layers, start=0):
        prev_name = name
        name = "layer_" + str(i)
        name, size, ctype, declaration, definition = layer(name, prev_name, size)
        res.append(MetaObjects(name, size, ctype, declaration, definition))
    return res


def model_transform(
        layers: list[Callable[[str, str, int], MetaObjects]],
        input_size: int,
        template: str,
        binary_type: str = "unsigned int",
):
    """model transformator

    Transforms the model (list of builder functions) to C code (string)

    Parameters
    ----------
    layers : list[Callable[[str, str, int], CodePart]]
        list of builder functions
    template : str
        path of a text template

    Returns
    -------
    str
        The generated C source code.
    """

    code_parts = model_extract(layers, input_size, binary_type=binary_type)

    def write(elements: list):
        return ";\n".join(elements) + ";"

    with open(template) as f:
        s = Template(f.read())
    definitions = [d for _, _, _, _, d in code_parts]
    declarations = [d for _, _, _, d, _ in code_parts]
    declarations = list(itertools.chain.from_iterable(declarations))  # type: ignore
    # declarations = [
    #    item for sublist in declarations for item in sublist
    # ]  # list(itertools.chain(*declarations))
    return s.substitute(
        {
            "input_name": code_parts[0].name,
            "input_type": code_parts[0].ctype,
            "input_size": input_size,
            "binary_type": binary_type,
            "declaration": write(declarations),
            "layers": create_layers(definitions),
            "output_value": code_parts[-1].name,
        }
    )
