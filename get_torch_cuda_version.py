import sys

support_cuda_versions = {
    "2.0": [117, 118],
    "2.1": [118, 121],
    "2.2": [118, 121],
    "2.3": [118, 121],
    "2.4": [118, 121, 124],
    "2.5": [118, 121, 124],
    "2.6": [118, 124, 126],
    "2.7": [118, 126, 128],
    "2.8": [126, 128, 129],
    "2.9": [126, 128, 130],
    "2.10": [126, 128, 130],
}

cuda_version = int(sys.argv[1])
matrix_torch_version = sys.argv[2]

target_cuda_versions = support_cuda_versions[matrix_torch_version]
target_cuda_versions = [
    v for v in target_cuda_versions if str(v)[:2] == str(cuda_version)[:2]
]
if len(target_cuda_versions) == 0:
    closest_version = support_cuda_versions[matrix_torch_version][-1]
else:
    closest_version = min(target_cuda_versions, key=lambda x: abs(x - cuda_version))
print(closest_version)
