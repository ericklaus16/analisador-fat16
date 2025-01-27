# Alunos: Eric Klaus e Matheus Rogério

from fat16file import Fat16File

def main():
    fileToOpen = "testfat.img"

    with open(fileToOpen, "rb") as file:
        data = file.read(512)

    bytes_per_sector = int.from_bytes(data[11:13], byteorder="little")
    sectors_per_cluster = int.from_bytes(data[13:14], byteorder="little")
    reserved_sectors = int.from_bytes(data[14:16], byteorder="little")
    number_of_fats = int.from_bytes(data[16:17], byteorder="little")
    number_of_root_entries = (int.from_bytes(data[17:19], byteorder="little") * 32) // bytes_per_sector
    sectors_per_fat = int.from_bytes(data[22:24], byteorder="little")

    fat1_start_pos = reserved_sectors
    fat2_start_pos = reserved_sectors + sectors_per_fat
    root_dir_start_pos = reserved_sectors + 2 * sectors_per_fat
    data_area_start_pos = reserved_sectors + 2 * sectors_per_fat + number_of_root_entries

    print("Bytes per sector:", bytes_per_sector)
    print("Sectors per cluster:", sectors_per_cluster)
    print("Reserved sectors:", reserved_sectors)
    print("Number of FATs:", number_of_fats)
    print("Number of root entries:", number_of_root_entries)
    print("Sectors per FAT:", sectors_per_fat)
    print("\nStarting Positions:")
    print("Boot Record:", [0, reserved_sectors - 1])
    print("FAT1:", [reserved_sectors, reserved_sectors + sectors_per_fat - 1])
    print("FAT2:", [reserved_sectors + sectors_per_fat, reserved_sectors + 2 * sectors_per_fat - 1])
    print("Root Directory:", [reserved_sectors + 2 * sectors_per_fat, reserved_sectors + 2 * sectors_per_fat + number_of_root_entries - 1])
    print(f"Data Area: [{reserved_sectors + 2 * sectors_per_fat + number_of_root_entries}, )")

    print("\nListing files:")
    with open(fileToOpen, "rb") as file:
        file.seek(root_dir_start_pos * bytes_per_sector)
        for i in range(number_of_root_entries):
            entry = file.read(32)
            removed = entry[0] == 0xe5

            if(removed):
                continue

            filename = entry[:8].decode('ascii', errors='ignore').strip()
            extension = entry[8:11].decode('ascii', errors='ignore').strip()
            filetype = entry[11]
            first_cluster = int.from_bytes(entry[26:27], byteorder="little")
            size = int.from_bytes(entry[28:31], byteorder="little")

            temp = Fat16File(filename, first_cluster, extension, filetype, size, fileToOpen)

            if temp.isValid():
                temp.print()
                temp.getOccupiedClusters(fat1_start_pos, bytes_per_sector)
                temp.getContent(data_area_start_pos, sectors_per_cluster, bytes_per_sector)

if __name__ == "__main__":
    main()