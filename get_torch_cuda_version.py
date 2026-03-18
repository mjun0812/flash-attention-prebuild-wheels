import sys

from scripts.coverage_matrix import TORCH_SUPPORT_CUDA_VERSIONS

cuda_version = int(sys.argv[1])
matrix_torch_version = sys.argv[2]

# Convert string CUDA versions (e.g., "12.8") to int format (e.g., 128)
support_versions = [
    int(v.replace(".", "")) for v in TORCH_SUPPORT_CUDA_VERSIONS[matrix_torch_version]
]

target_cuda_versions = [
    v for v in support_versions if str(v)[:2] == str(cuda_version)[:2]
]
if len(target_cuda_versions) == 0:
    closest_version = support_versions[-1]
else:
    closest_version = min(target_cuda_versions, key=lambda x: abs(x - cuda_version))
print(closest_version)
