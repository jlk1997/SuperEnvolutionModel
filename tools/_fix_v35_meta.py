import json
from pathlib import Path
p=Path('evo/office/fixtures/vision_images_v35/manifest.json')
m=json.loads(p.read_text(encoding='utf-8'))
m['version']='v35'
m['theme']='jade_granite_suede_bronze_opal_hinge_citrine_basalt_pewter_vellum_fleece_null_burlap_porcelain_twine_mulberry_nickel_folio'
m['harder_than']='v34_bamboo_slate_denim'
m['note']='fixtures only; claim deferred to C315 VL smoke'
# fix lesson already says V35
p.write_text(json.dumps(m, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
# also patch c314 script defaults for future regen
sp=Path('scripts/c314_vision_v35_design_and_batch.py')
t=sp.read_text(encoding='utf-8')
t2=t.replace('"version": "v33"', '"version": "v35"', 1)
t2=t2.replace(
    '"theme": "parchment_cork_canvas_rivet_holo_zip_filament_honey_marble_copper_acetate_perf_waxseal_magnet_crepe_satin_spiral"',
    '"theme": "jade_granite_suede_bronze_opal_hinge_citrine_basalt_pewter_vellum_fleece_null_burlap_porcelain_twine_mulberry_nickel_folio"',
    1,
)
t2=t2.replace('"harder_than": "v27_hlx_magclip_c266"', '"harder_than": "v34_bamboo_slate_denim"', 1)
t2=t2.replace('claim deferred to C303 VL smoke', 'claim deferred to C315 VL smoke', 1)
t2=t2.replace('hash(fid + "_v33c272")', 'hash(fid + "_v35c314")')
if t2!=t:
    sp.write_text(t2, encoding='utf-8')
    print('patched c314')
else:
    print('c314 unchanged')
print('manifest version', json.loads(p.read_text(encoding='utf-8'))['version'])
