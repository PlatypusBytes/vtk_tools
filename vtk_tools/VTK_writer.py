import os
import sys


class Write:
    def __init__(self, output_folder, file_name="result"):
        """
        Initialises paraview VTK writer

        :param output_folder: location to save VTK files
        :param file_name: VTK file name
        """

        # output folder
        self.output_folder = output_folder  # output folder to save vtk file
        # check if output exists: if not creates
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)

        # VTK file
        self.file = open(os.path.join(self.output_folder, file_name + ".vtk"), "w")

        # nb of nodes
        self.nb_nodes = []
        # cell type according to VTK manual. ToDo: only these two cell types are supported
        self.cell_types = ["5","22", "9","12", "25", "10", "24"]

        # coordinates
        self.coordinates = []

        # data
        self.data = []

        # nodes
        self.nodes = []

        # nb nodes y direction
        self.nb_nodes_y = []

        # elements
        self.elements = []

        # write identifier
        self.file.write("# vtk DataFile Version 2.0\n")
        # write header
        self.file.write(file_name + "\n")
        # write format
        self.file.write("ASCII\n")
        self.structure = []
        self.attributes = []
        return

    def add_mesh(self, nodes, elements, element_type: str):
        """
        Writes mesh: nodes and elements

        :param nodes: node list
        :param elements: element list
        :param element_type: element type, either: tri3, tri6, quad4, hexa8, hexa20
        """

        # writes header
        self.file.write("DATASET UNSTRUCTURED_GRID\n")

        # nodes and elements
        self.nodes = nodes
        self.elements = elements

        # checks element type
        if element_type == "tri3":
            nb_nodes = 3
            typ = self.cell_types[0]
        elif element_type == "tri6":
            nb_nodes = 6
            typ = self.cell_types[1]
        elif element_type == "quad4":
            nb_nodes = 4
            typ = self.cell_types[2]
        elif element_type == "hexa8":
            nb_nodes = 8
            typ = self.cell_types[3]
        elif element_type == "hexa20":
            nb_nodes = 20
            typ = self.cell_types[4]
        elif element_type == "tetra4":
            nb_nodes = 4
            typ = self.cell_types[5]
        elif element_type == "tetra10":
            nb_nodes = 10
            typ = self.cell_types[6]
        else:
            sys.exit("Error: type of element not supported")

        # write POINTS
        self.file.write("POINTS " + str(len(self.nodes)) + " float\n")
        for i in range(len(self.nodes)):
            self.file.write(" ".join(list(map(str, self.nodes[i]))) + "\n")

        # write CELLS
        self.file.write("CELLS " + str(len(self.elements)) + " " + str((nb_nodes + 1) * len(self.elements)) + "\n")
        for i in range(len(self.elements)):
            self.file.write(f"{str(nb_nodes)} {' '.join(list(map(str, self.elements[i])))}\n")

        # write CELL types
        self.file.write("CELL_TYPES " + str(len(self.elements)) + "\n")
        for i in range(len(self.elements)):
            self.file.write(str(typ) + "\n")

        return

    def add_vector(self, key, data, header=True):
        """
        Writes node vector data into VTK

        :param key: name of the vector
        :param data: vector data
        :param header: (optional) Header needs to be true for the first vector
        """

        # write vector
        if header:  # if first scalar needs header
            self.file.write(f"POINT_DATA {str(len(self.nodes))}\n")
        self.file.write(f"VECTORS {key} double\n")

        # write vector data for each node
        for i in range(len(self.nodes)):
            self.file.write(f'{" ".join(map(str, data[i]))}\n')

        return

    def add_scalar(self, key, data, header=True):
        """
        Writes element scalar data into VTK

        :param key: name of the scalar
        :param data: scalar data
        :param header: (optional) Header needs to be true for the first vector
        """

        # write scalar
        if header:  # if first scalar needs header
            self.file.write(f"CELL_DATA {str(len(self.elements))}\n")
        self.file.write(f"SCALARS {key} double\n")
        self.file.write("LOOKUP_TABLE default\n")

        # write scalar data for each element
        for i in range(len(self.elements)):
            self.file.write(f"{str(data[i])}\n")

        return

    def save(self):
        """
        Saves and closes VTK file
        """
        self.file.close()
        return
