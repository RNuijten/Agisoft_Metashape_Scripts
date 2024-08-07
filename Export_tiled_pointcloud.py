
import Metashape
def export_point_cloud_with_buffer(project_path, export_path, chunk_name, tile_size, buffer_size):   
    # Open the project
    doc = Metashape.Document()
    doc.open(project_path, read_only=False)  # Ensure the document is not opened in read-only mode
    
    # Find the chunk by name
    chunk = None
    for c in doc.chunks:
        if c.label == chunk_name:
            chunk = c
            break
    
    if not chunk:
        raise ValueError(f"Chunk with name '{chunk_name}' not found")
    
    # Define the bounding box of the point cloud
    region = chunk.region
    min_corner = region.center - region.size / 2
    max_corner = region.center + region.size / 2
    
    # Calculate number of tiles
    x_tiles = int((max_corner.x - min_corner.x) / tile_size) + 1
    y_tiles = int((max_corner.y - min_corner.y) / tile_size) + 1
    
    # Iterate through the tiles
    for i in range(x_tiles):
        for j in range(y_tiles):
            # Calculate tile boundaries with buffer
            x_min = min_corner.x + i * tile_size - buffer_size
            x_max = min_corner.x + (i + 1) * tile_size + buffer_size
            y_min = min_corner.y + j * tile_size - buffer_size
            y_max = min_corner.y + (j + 1) * tile_size + buffer_size
            
            # Ensure boundaries are within the original point cloud limits
            x_min = max(x_min, min_corner.x)
            x_max = min(x_max, max_corner.x)
            y_min = max(y_min, min_corner.y)
            y_max = min(y_max, max_corner.y)
            
            # Create a boundary shape for the tile
            boundary = chunk.shapes.addShape()
            boundary.label = f"Boundary_{i}_{j}"
            boundary.geometry = Metashape.Geometry.Polygon([
                Metashape.Vector([x_min, y_min, min_corner.z]),
                Metashape.Vector([x_max, y_min, min_corner.z]),
                Metashape.Vector([x_max, y_max, min_corner.z]),
                Metashape.Vector([x_min, y_max, min_corner.z]),
                Metashape.Vector([x_min, y_min, min_corner.z])
            ])
            #boundary.type = Metashape.Shape.Type.Polygon
            boundary.boundary_type = Metashape.Shape.BoundaryType.OuterBoundary
            
            # Export the point cloud for the tile
            tile_filename = f"{export_path}/tile_{i}_{j}.las"
            chunk.exportPointCloud(path=tile_filename,
                                   source_data=Metashape.DataSource.PointCloudData,
                                   clip_to_boundary=True)
            print(f"Exported {tile_filename}")
            
            # Remove the boundary shape after export to avoid overlap
            chunk.shapes.remove(boundary)

# Define the parameters
project_path = "D:/Projects/Cowichan_2023/_cowichan_jen/Agisoft/RGB_only.psx"
export_path = "D:/Repos/_point_cloud_tiling_and_normalization/_point_cloud_tiling_and_normalization/data/tiles/agisoft_test"
chunk_name = "RGB_May28"
tile_size = 25  # Size of each tile in the desired units
buffer_size = 5  # Buffer size in the same units

# Run the function
export_point_cloud_with_buffer(project_path, export_path, chunk_name, tile_size, buffer_size)