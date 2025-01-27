class Fat16File:
    def __init__(self, name, first_cluster, extension, filetype, size, fileToOpen):
        self.name = name
        self.first_cluster = first_cluster
        self.type = filetype
        self.extension = extension
        self.size = size
        self.fileToOpen = fileToOpen
        self.occupiedClusters = []

    def isValid(self):
        valid_types = [1, 2, 4, 8, 16, 32]
        return self.type in valid_types
    
    def print(self):
        print(f"File {self.name}.{self.extension}:")
        type_str = ""

        if self.type == 1:
            type_str = "READ_ONLY"
        elif self.type == 2:
            type_str = "HIDDEN"
        elif self.type == 4:
            type_str = "SYSTEM"
        elif self.type == 8:
            type_str = "VOLUME_ID"
        elif self.type == 16:
            type_str = "DIRECTORY"
        elif self.type == 32:
            type_str = "ARCHIVE"

        print(f"Type: {type_str}")
        print(f"First Cluster: {self.first_cluster}")
        print(f"File Size: {self.size} bytes")

    def getOccupiedClusters(self, fat_start_pos, bytes_per_sector):
        print("Occupied Clusters:")
        # print(self.first_cluster)
        self.occupiedClusters.append(self.first_cluster)
        pos = fat_start_pos * bytes_per_sector + (self.first_cluster * 2)
        canRead = True
        with open(self.fileToOpen, 'rb') as file:
            while canRead:
                file.seek(pos)
                cluster = int.from_bytes(file.read(2), byteorder='little')
                if cluster >= 65528:
                    canRead = False
                else:
                    self.occupiedClusters.append(cluster)
                    pos = fat_start_pos * bytes_per_sector + (cluster * 2)
            print(self.occupiedClusters)

    def getContent(self, data_area_start_pos, sectors_per_cluster, bytes_per_sector):
        print("Content:")
        tmp_size = self.size

        for cluster in self.occupiedClusters:
            cluster_size = sectors_per_cluster * bytes_per_sector

            if tmp_size > cluster_size:
                tmp_size -= cluster_size
            else:
                cluster_size = tmp_size

            pos = (data_area_start_pos * bytes_per_sector) + ((cluster - 2) * sectors_per_cluster * bytes_per_sector)

            with open(self.fileToOpen, 'rb') as file:
                file.seek(pos)
                print(file.read(cluster_size).decode('ascii', errors='ignore'), end='') 
        print("\n")