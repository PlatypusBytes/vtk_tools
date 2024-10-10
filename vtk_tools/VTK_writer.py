import os
import sys
import struct

ELEMENT_TYPES = ("tri3", "tri6", "quad4", "hexa8", "hexa20", "tetra4", "tetra10")

class Write:
    def __init__(self, output_folder, file_name="result", write_binary=True):
        """
        Initialises paraview VTK writer

        :param output_folder: location to save VTK files
        :param file_name: VTK file name
        :param write_binary: Boolean to write binary (big endian) format. If False, writes in ASCII format.
        """
        os.makedirs(output_folder, exist_ok=True)
        self.output_folder = output_folder

        self.write_binary = write_binary
        self.file_mode = "wb" if write_binary else "w"
        self.file = open(os.path.join(self.output_folder, file_name + ".vtk"), self.file_mode)

        # self.cell_types = [5, 22, 9, 12, 25, 10, 24]

        # nb_nodes and cell type according to VTK manual.
        self.element_type_map = {"tri3": (3, 5),
                                 "tri6": (6, 22),
                                 "quad4": (4, 9),
                                 "hexa8": (8, 12),
                                 "hexa20": (20, 25),
                                 "tetra4": (4, 10),
                                 "tetra10": (10, 24)
                                 }

        # variables
        self.coordinates = []
        self.data = []
        self.nodes = []
        self.nb_nodes_y = []
        self.elements = []
        self.structure = []
        self.attributes = []

        # Write header
        self._write_strings("# vtk DataFile Version 2.0\n")
        self._write_strings(file_name + "\n")
        self._write_strings("BINARY\n" if write_binary else "ASCII\n")


    def _write_strings(self, data):
        """Helper method to write data in either ASCII or binary format

        :param data: data to write
        """
        if self.write_binary:
            self.file.write(data.encode() if isinstance(data, str) else data)
        else:
            self.file.write(data)

    def _write_data_to_file(self, format_string, *args):
        """
        Helper method to write to file.
        In case of binary writes big-endian binary data

        :param format_string: format string
        :param args: data to write
        """
        if self.write_binary:
            self.file.write(struct.pack('>' + format_string, *args))
        else:
            self.file.write(' '.join(map(str, args)) + '\n')

    def add_mesh(self, nodes, elements, element_type):
        """
        Writes mesh: nodes and elements

        :param nodes: node list
        :param elements: element list
        :param element_type: element type
        """
        self._write_strings("DATASET UNSTRUCTURED_GRID\n")
        self.nodes = nodes
        self.elements = elements

        if element_type not in self.element_type_map:
            sys.exit("Error: type of element not supported")

        nb_nodes, typ = self.element_type_map[element_type]

        # Write POINTS
        self._write_strings(f"POINTS {len(self.nodes)} float\n")
        for node in self.nodes:
            self._write_data_to_file('fff', *node)

        # Write CELLS
        self._write_strings(f"CELLS {len(self.elements)} {(nb_nodes + 1) * len(self.elements)}\n")
        for element in self.elements:
            self._write_data_to_file('i' * (nb_nodes + 1), nb_nodes, *element)

        # Write CELL_TYPES
        self._write_strings(f"CELL_TYPES {len(self.elements)}\n")
        for i in self.elements:
            self._write_data_to_file('i', typ)

        # if self.write_binary:
        #     self._write_data_to_file('i' * len(self.elements), *([typ] * len(self.elements)))
        # else:
        #     for _ in range(len(self.elements)):
        #         self._write_strings(f"{typ}\n")

    def add_vector(self, key, data, header=True):
        """
        Writes node vector data into VTK

        :param key: name of the vector
        :param data: vector data
        :param header: (optional) Header needs to be true for the first vector
        """
        if header:
            self._write_strings(f"POINT_DATA {len(self.nodes)}\n")
        self._write_strings(f"VECTORS {key} double\n")

        for vector in data:
            self._write_data_to_file('ddd', *vector)

    def add_scalar(self, key, data, header=True):
        """
        Writes element scalar data into VTK

        :param key: name of the scalar
        :param data: scalar data
        :param header: (optional) Header needs to be true for the first vector
        """
        if header:
            self._write_strings(f"CELL_DATA {len(self.elements)}\n")
        self._write_strings(f"SCALARS {key} double\n")
        self._write_strings("LOOKUP_TABLE default\n")

        if self.write_binary:
            self._write_data_to_file('d' * len(data), *data)
        else:
            for value in data:
                self._write_strings(f"{value}\n")

    def save(self):
        """
        Saves and closes VTK file
        """
        self.file.close()