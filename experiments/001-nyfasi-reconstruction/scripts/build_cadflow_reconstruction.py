"""Deterministic B-rep reconstruction using CadFlow and the shared parameter ledger."""
from __future__ import annotations
import json, math
from pathlib import Path
import cadflow as cad
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PARAMS=json.loads((ROOT/"models/cad-parameters.json").read_text(encoding="utf-8"))["parameters"]
P={k:v["value"] for k,v in PARAMS.items()}
OUT=ROOT/"output"/"cadflow"

def box_at(m,w,d,h,x=0,y=0,z=0):
    s=m.box(width=w,depth=d,height=h)
    return m.translate(s,x=x-w/2,y=y-d/2,z=z-h/2)

def cylinder_x(m,r,length,x=0,y=0,z=0):
    s=m.cylinder(radius=r,height=length)
    s=m.rotate(s,degrees=90,axis=(0,1,0),origin=(0,0,0))
    return m.translate(s,x=x-length/2,y=y,z=z)

def hollow_box(m,w,d,h,wall,floor,open_top=True):
    outer=box_at(m,w,d,h)
    inner_h=h-floor+1 if open_top else h-2*floor
    inner_z=-h/2+floor+inner_h/2 if open_top else 0
    inner=box_at(m,w-2*wall,d-2*wall,inner_h,z=inner_z)
    return m.cut(outer,inner)

def curved_wall(m):
    seat=P["roller_d"]/2+P["roller_seat_clearance"]
    outer=seat+P["wall_thickness"]
    points=[]
    for i in range(65):
        a=math.radians(-90+180*i/64)
        points.append((0,outer*math.cos(a),outer*math.sin(a)))
    for i in range(64,-1,-1):
        a=math.radians(-90+180*i/64)
        points.append((0,seat*math.cos(a),seat*math.sin(a)))
    wall=m.extrude(m.face(m.polyline(tuple(points),closed=True)),x=P["wall_len"],y=0,z=0)
    wall=m.translate(wall,x=-P["wall_len"]/2,y=0,z=0)
    for i in range(P["tooth_count"]-1):
        x=(i-(P["tooth_count"]-2)/2)*P["tooth_pitch"]
        tool=box_at(m,P["slot_w"],outer*2+2,outer*2+2,x=x,y=outer/2)
        wall=m.cut(wall,tool)
    return wall

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    parts={}
    cy=P["housing_d"]/2
    cz=-P["lower_shell_h"]/2
    with cad.Model() as m:
        parts["housing_lower"]=hollow_box(m,P["housing_w"],P["housing_d"],P["lower_shell_h"],2,1.5,True)
        parts["housing_upper"]=hollow_box(m,P["housing_w"],P["housing_d"],P["upper_shell_h"],2,1.5,False)
        parts["reservoir"]=hollow_box(m,P["reservoir_w"],P["reservoir_d"],P["reservoir_h"],1.5,1,True)
        parts["roller_core"]=cylinder_x(m,P["roller_core_d"]/2,P["roller_len"],y=cy,z=cz)
        for i in range(P["roller_band_count"]):
            x=(i-(P["roller_band_count"]-1)/2)*P["tooth_pitch"]
            a=cylinder_x(m,P["roller_d"]/2,P["roller_band_width"],x,cy,cz)
            b=cylinder_x(m,(P["roller_core_d"]-.2)/2,P["roller_band_width"]+.4,x,cy,cz)
            parts[f"roller_band_{i+1:02d}"]=m.cut(a,b)
        for side,sign in (("left",-1),("right",1)):
            ex=sign*(P["roller_len"]/2-P["roller_endwall_t"]/2)
            px=sign*(P["roller_len"]/2+P["spindle_pin_len"]/2)
            parts[f"roller_endwall_{side}"]=cylinder_x(m,P["roller_endwall_d"]/2,P["roller_endwall_t"],ex,cy,cz)
            parts[f"spindle_pin_{side}"]=cylinder_x(m,P["spindle_pin_d"]/2,P["spindle_pin_len"],px,cy,cz)
            bx=sign*(P["roller_len"]/2+P["spindle_pin_len"]/2)
            bearing=box_at(m,P["bearing_block_w"],P["bearing_block_d"],P["bearing_block_h"],bx,cy,cz)
            bore=cylinder_x(m,(P["spindle_pin_d"]+2*P["bearing_bore_clearance"])/2,P["bearing_block_w"]+1,bx,cy,cz)
            parts[f"bearing_support_{side}"]=m.cut(bearing,bore)
        parts["curved_slotted_wall"]=curved_wall(m)
        for i in range(P["tooth_count"]):
            x=(i-(P["tooth_count"]-1)/2)*P["tooth_pitch"]
            parts[f"comb_tooth_{i+1:02d}"]=box_at(m,P["tooth_width"],P["tooth_length"],P["tooth_height"],x,cy,cz-P["roller_d"]/2-P["wall_thickness"]-P["tooth_height"]/2)
        for i in range(P["snap_tab_count"]):
            x=(i-(P["snap_tab_count"]-1)/2)*(P["housing_w"]-24)
            parts[f"housing_snap_tab_{i+1:02d}"]=box_at(m,P["snap_tab_w"],P["snap_tab_d"],P["snap_tab_h"],x,0,P["lower_shell_h"]/2+P["snap_tab_h"]/2)
        manifest={"schema_version":"1.0.0","engine":"CadFlow","engine_version":getattr(cad,"__version__","unknown"),"units":"mm","model_status":"research_only","source_parameter_file":"models/cad-parameters.json","component_count":len(parts),"components":{},"limitations":["No authorised physical sample or native supplier CAD was used.","Assumed dimensions remain assumptions; no tolerance or fit certification.","Separate STEP files preserve component identity; assembly constraints are not solved.","Not a manufacturing release or verified digital twin."]}
        for name,shape in parts.items():
            report=shape.validate()
            if not report.ok:
                raise RuntimeError(f"CadFlow validation failed for {name}: {report}")
            stem=OUT/name
            shape.export_step(str(stem.with_suffix(".step")))
            shape.export_stl(str(stem.with_suffix(".stl")),binary=True)
            shape.export_preview_glb(str(stem.with_suffix(".glb")))
            manifest["components"][name]={"kind":shape.kind,"volume_mm3":shape.volume,"bbox_mm":list(shape.bbox),"topology":shape.topology,"validation":report.to_dict(),"step":stem.with_suffix(".step").name,"stl":stem.with_suffix(".stl").name,"glb":stem.with_suffix(".glb").name}
    (OUT/"cadflow-build-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return manifest

if __name__=="__main__":
    result=build()
    print(f"CadFlow built {result['component_count']} separately validated components")
