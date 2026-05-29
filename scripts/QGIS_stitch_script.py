import os
import math
from qgis.PyQt.QtCore import QSize
from qgis.core import QgsMapSettings, QgsMapRendererSequentialJob, QgsRectangle
from qgis.utils import iface

# --- CONFIGURATION ---
OUTPUT_FOLDER = "/Users/atakan/Downloads/QGIS_Geotiff_Tiles"
MAP_UNITS_PER_PIXEL = 0.3  # Optimize edilmiş gerçekçi netlik
TILE_SIZE = 1024           # 1024x1024 piksel

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Mevcut harita ekranını ve ayarlarını al
canvas = iface.mapCanvas()
full_extent = canvas.extent()
settings = canvas.mapSettings()

# Çıktı boyutu ve netliğini zorla
settings.setOutputSize(QSize(TILE_SIZE, TILE_SIZE))
# Çözünürlük ölçeklemesini (DPI) ekran standardına sabitle
settings.setOutputDpi(96) 

# Gerçek dünyadaki adım miktarını hesapla (Örn: 1024 * 0.3 = 307.2 metre)
step = TILE_SIZE * MAP_UNITS_PER_PIXEL
cols = math.ceil(full_extent.width() / step)
rows = math.ceil(full_extent.height() / step)

print(f"Grid Layout: {rows} rows x {cols} columns.")
print("Starting rendering engine. Properly waiting for Bing network tiles...")

for row in range(rows):
    for col in range(cols):
        # Her bir karenin koordinatlarını hesapla
        xmin = full_extent.xMinimum() + (col * step)
        xmax = xmin + step
        ymax = full_extent.yMaximum() - (row * step)
        ymin = ymax - step

        tile_extent = QgsRectangle(xmin, ymin, xmax, ymax)
        settings.setExtent(tile_extent)

        # Render motorunu başlat (İnternetten haritanın inmesini bekler)
        job = QgsMapRendererSequentialJob(settings)
        job.start()
        job.waitForFinished()

        image = job.renderedImage()

        # Dosya yolları
        base_filename = f"tile_r{row}_c{col}"
        tif_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}.tif")
        tfw_path = os.path.join(OUTPUT_FOLDER, f"{base_filename}.tfw")

        # Görseli TIF olarak kaydet
        image.save(tif_path, "TIFF")

        # --- WORLD FILE (.tfw) OLUŞTURMA ---
        # Bu dosya, düz .tif görselini bir GeoTIFF (Koordinatlı Harita) yapar
        with open(tfw_path, "w") as tfw:
            tfw.write(f"{MAP_UNITS_PER_PIXEL}\n")             # 1: X pixel size
            tfw.write("0.0\n")                                # 2: X rotation
            tfw.write("0.0\n")                                # 3: Y rotation
            tfw.write(f"-{MAP_UNITS_PER_PIXEL}\n")            # 4: Y pixel size (Y ekseni QGIS'te terstir)
            tfw.write(f"{xmin + (MAP_UNITS_PER_PIXEL/2)}\n")  # 5: Upper-left X coordinate
            tfw.write(f"{ymax - (MAP_UNITS_PER_PIXEL/2)}\n")  # 6: Upper-left Y coordinate

        print(f"Saved: {base_filename}.tif and corresponding .tfw")

print(f"Success! {rows * cols} Georeferenced tiles saved to {OUTPUT_FOLDER}")