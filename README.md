# OSINT-ONLY USE — USE STRICTLY WITHIN APPLICABLE LAWS AND TERMS.

# QGIS Bing Satellite Grid Harvester

Download Bing Satellite imagery from QGIS by slicing a large area into a clean grid of tiles, then (optionally) merge those tiles into a smaller set of files for easier handling.

Think of it as: **set extent -> render tiles -> keep it georeferenced -> (optional) stitch**.

---

## What this repo does

- Splits the current QGIS canvas extent into a grid of tiles.
- Renders Bing Satellite imagery per tile with a fixed output size.
- Saves tiles as PNG or TIFF + TFW (world file) for georeferencing.
- Gives you a simple, repeatable pipeline for large area downloads.

---

## Scripts

- `scripts/QGIS_large_area_imagery.py`
  - Exports **PNG** tiles (lossless), great for ML/object detection datasets.
  - Grid size and resolution are controlled by `TILE_SIZE` and `MAP_UNITS_PER_PIXEL`.

- `scripts/QGIS_stitch_script.py`
  - Exports **TIFF** tiles plus `.tfw` world files (georeferenced).
  - Suited for GIS workflows and later stitching with GDAL.

---

## Quick start (QGIS)

1. Open QGIS and load **Bing Satellite** layer.
2. Zoom to the area you want and set the canvas extent.
3. Open **Python Console** (Plugins -> Python Console).
4. Run one script:

```python
exec(open("/ABS/PATH/QGIS_satellite_imagery/scripts/QGIS_large_area_imagery.py").read())
# or
exec(open("/ABS/PATH/QGIS_satellite_imagery/scripts/QGIS_stitch_script.py").read())
```

Tiles will be written to the `OUTPUT_FOLDER` defined in the script.

---

## Configuration knobs

Edit the top of the script you use:

- `OUTPUT_FOLDER`: where tiles are saved
- `TILE_SIZE`: tile size in pixels (default 1024)
- `MAP_UNITS_PER_PIXEL`: spatial resolution (e.g. 0.3 = 0.3 map units per pixel)

In a meter-based CRS, `MAP_UNITS_PER_PIXEL = 0.30` targets ~0.30 m (30 cm) per pixel detail.

The **step size** is:

$$
\text{step} = \text{TILE\_SIZE} \times \text{MAP\_UNITS\_PER\_PIXEL}
$$

This determines how many rows/cols your grid will have.

---

## Optional: stitch tiles into fewer files

If you export **TIFF + TFW**, you can merge tiles with GDAL:

```bash
gdal_merge.py -o merged.tif /path/to/QGIS_Geotiff_Tiles/*.tif
```

For very large areas, use a VRT first:

```bash
gdalbuildvrt merged.vrt /path/to/QGIS_Geotiff_Tiles/*.tif
gdal_translate merged.vrt merged.tif
```

---

## Tips

- Keep QGIS visible while rendering so Bing tiles can load.
- Start with a small area to validate resolution and output.
- Reduce `MAP_UNITS_PER_PIXEL` for higher detail (more tiles).
- If you need fewer tiles, increase `MAP_UNITS_PER_PIXEL`.

---

## Notes and limits

- Bing Satellite usage is subject to Microsoft terms and tile limits.
- This is a QGIS render pipeline; output depends on current layer styling and zoom.

---

## Structure

```
QGIS_satellite_imagery/
  scripts/
    QGIS_large_area_imagery.py
    QGIS_stitch_script.py
```

---

## License

Add a license if you plan to share or publish this repo.
