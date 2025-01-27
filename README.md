# FAT16 Image Reader

This repository contains a Python program that reads a FAT16 disk image file and extracts metadata, file structure, and file content. It is designed for educational purposes, demonstrating how to interpret FAT16 file systems.

## Features
- Extracts key metadata from the FAT16 disk image:
  - Number of FATs
  - Starting positions of FAT1, FAT2, root directory, and data area
- Lists files and directories in the root directory (in 8.3 format), displaying:
  - File names
  - First cluster
  - File size
- Displays the clusters occupied by a file.
- Prints the content of files stored in the FAT16 image.

## Requirements
- Python 3.8 or higher

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fat16-image-reader.git
   cd fat16-image-reader
   ```

2. Ensure you have a valid FAT16 disk image file (e.g., `testfat.img`) in the same directory.

3. Run the program:
   ```bash
   python fat16_reader.py
   ```

4. The program will:
   - Parse and display metadata about the FAT16 structure.
   - List files and directories in the root directory.
   - Show the clusters occupied by each file.
   - Display the content of each file.

## File Structure
```
.
├── fat16_reader.py        # Main program
├── fat16file.py           # Class to handle FAT16 files
├── testfat.img            # Example FAT16 image (provide your own)
└── README.md              # Project documentation
```

## Example Output
```
Bytes per sector: 512
Sectors per cluster: 8
Reserved sectors: 1
Number of FATs: 2
Number of root entries: 512
Sectors per FAT: 9

Starting Positions:
Boot Record: [0, 0]
FAT1: [1, 9]
FAT2: [10, 18]
Root Directory: [19, 50]
Data Area: [51, )

Listing files:
File README   .TXT:
Type: ARCHIVE
First Cluster: 2
File Size: 1024 bytes
Occupied Clusters:
[2]
Content:
Hello, FAT16!
```

## Implementation Details
The program uses:
- **Bytes per sector** and **sectors per cluster** to calculate the data layout.
- FAT chains to track clusters occupied by files.
- Basic decoding of ASCII content from clusters.

### Class `Fat16File`
Handles:
- File metadata (name, type, size, etc.)
- Cluster chain traversal
- File content extraction

## Limitations
- Only supports FAT16 disk images.
- Assumes the input image file is valid.
- Does not handle advanced FAT features like long file names.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

## Authors
- Eric Klaus
- Matheus Rogério
