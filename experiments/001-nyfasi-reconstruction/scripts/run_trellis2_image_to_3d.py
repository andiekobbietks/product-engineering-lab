"""Optional Microsoft TRELLIS.2 single-image inference on a supported CUDA host.

Run inside the official microsoft/TRELLIS.2 environment. This is an AI-generated
visual hypothesis, not a dimensionally faithful CAD model. Do not use its scale
or hidden geometry as measured product evidence.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import torch
from PIL import Image
from trellis2.pipelines import Trellis2ImageTo3DPipeline
import o_voxel

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("image",type=Path)
    parser.add_argument("--output",type=Path,default=Path("nyfasi_trellis2_hypothesis.glb"))
    parser.add_argument("--resolution",type=int,choices=(512,1024,1536),default=1024)
    args=parser.parse_args()
    if not torch.cuda.is_available():
        raise SystemExit("TRELLIS.2 inference requires a supported NVIDIA CUDA GPU; use the hosted demo or a GPU runner.")
    pipeline=Trellis2ImageTo3DPipeline.from_pretrained("microsoft/TRELLIS.2-4B")
    pipeline.cuda()
    image=Image.open(args.image).convert("RGBA")
    mesh=pipeline.run(image)[0]
    mesh.simplify(16777216)
    glb=o_voxel.postprocess.to_glb(
        vertices=mesh.vertices,faces=mesh.faces,attr_volume=mesh.attrs,
        coords=mesh.coords,attr_layout=mesh.layout,voxel_size=mesh.voxel_size,
        aabb=[[-0.5,-0.5,-0.5],[0.5,0.5,0.5]],
        decimation_target=500000,texture_size=2048,remesh=True,
        remesh_band=1,remesh_project=0,verbose=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    glb.export(str(args.output),extension_webp=True)
    print(f"Generated visual hypothesis: {args.output}")
if __name__=="__main__": main()
